#!/usr/local/opt/python/bin/python3.7
#This program extracts new cases off of the Oregon court file website and saves them to a csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import requests
from datetime import datetime, timedelta
import numpy as np
import csv
import pyodbc
import socket
import os
from datetime import datetime as dt
from datetime import timezone, date, timedelta
from numpy import genfromtxt


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

    if is_connected():
        print("connected")
    else:
        print("not connected")

def runscript(desired_date):

    
    county = "Deschutes"
    username = os.getenv('COURT_USER')
    password = os.getenv('COURT_PASS')

    ##Set up Selenium Driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    
    options.binary_location = "/usr/bin/chromium"
    
    # driver = webdriver.Chrome(executable_path="/Users/dylanalbertazzi/Documents/Clients_SEO/ALF_Folder/Court-Download/chromedriver", chrome_options=chrome_options)
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://publicaccess.courts.oregon.gov/PublicAccessLogin/Login.aspx?ReturnUrl=/PublicAccessLogin/default.aspx')
    # driver.quit
    ##Navigate to case data
    userID = driver.find_element_by_id("UserName")
    userID.send_keys(username)

    passBox = driver.find_element_by_id("Password")
    passBox.send_keys(password)

    submit_button = driver.find_element_by_name("SignOn")
    submit_button.click()

    select = Select(driver.find_element_by_id('sbxControlID2')) # Searching for the right county
    select.select_by_visible_text(county)

    search_civil = driver.find_element_by_link_text('Search Civil, Family, Probate and Tax Court Case Records') #searching Civil, Fam, Probate, and Tax 
    search_civil.click()

    date_organize = Select(driver.find_element_by_id('SearchBy')) #Make sure searching by date filed
    date_organize.select_by_visible_text('Date Filed')

    radio_button = driver.find_element_by_xpath("//input[@id='OpenOption']")
    radio_button.click()


    date_early = driver.find_element_by_id("DateFiledOnAfter")
    date_early.send_keys(desired_date)
    date_old = driver.find_element_by_id("DateFiledOnBefore")
    date_old.send_keys(desired_date)

    submit_button2 = driver.find_element_by_id("SearchSubmit") #Form to get list of filed cases
    submit_button2.click()
    time.sleep(5)
    current_url = driver.current_url


    ########### Get Data ################
    response = requests.get(current_url)
    #soup = BeautifulSoup(response.content, 'html.parser')
    soup = BeautifulSoup(driver.page_source, 'html.parser')


    jj = soup.find_all('table')
    jj5 = jj[5]

    column_length = len(jj5.find_all('tr')[1:])

    if column_length > 1:
        table_length = len(jj5.find_all('tr')[1:])
        table_data = np.empty([table_length, 6], dtype="|U250")


        i = 0

        #Cycle through each row
        for tr in jj5.find_all('tr')[1:]:
            tds = tr.find_all('td')
            link = tds[0].a
            link = link.get('href')
            #print(link)
            #populate numpy array
            table_data[i, 0] = link.strip() 
            table_data[i, 1] = tds[0].text.strip() #Case Number
            table_data[i, 2] = tds[1].text.strip()  #Description
            table_data[i, 3] = tds[2].contents[0].text.strip()  #Filed date
            table_data[i, 4] = tds[3].contents[0].text.strip()  #Type
            table_data[i, 5] = "Deschutes" #add to be other counties too
        
            i += 1

        d_date = datetime.strftime(datetime.now() - timedelta(1), '%m_%d_%Y')
        d_date2 = date.today() - timedelta(days=1)
        # csv_name = "/Users/dylanalbertazzi/Documents/Clients_SEO/ALF_Folder/Court-Download/case_logs/" + d_date + 'Deschutes''.csv' #add county name to name
        # with open(csv_name , 'w') as w:
        #     w = csv.writer(w)
        #     w.writerow(["Link","CaseNo", "Description", "FileDate", "County", "CaseType"])
        #     w.writerows(table_data)
        
        #Upload to server.
        
        # my_data = genfromtxt(csv_name, delimiter=',', dtype=None)
        server = 'lawdata.database.windows.net,1433'
        database = 'CourtData'
        username = os.getenv('LAW_DB_USER')
        password = os.getenv('LAW_DB_PASS')
        driver= '{ODBC Driver 17 for SQL Server}'
        auth= 'ActiveDirectoryPassword'
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';Authentication='+auth+';')
        cursor = cnxn.cursor()

        
        
        for case in table_data:
            
            with cnxn:
                cursor.execute("""
                insert into DocketRecords(CaseNo, Description, FileDate, County, CaseType, CreateDateUtc, CourtCaseId) values (?,?,?,?,?,?,?)""", case[1],case[2], d_date2 ,case[5],case[4], dt.now(timezone.utc),case[0])
                cnxn.commit()
    else:
        print("no cases")

    


def main():
    
    desired_date = datetime.strftime(datetime.now() - timedelta(1), '%m/%d/%Y')
    
    curr_day = datetime.today().weekday() #0- monday, 6 - Sunday
    check_day = curr_day - 1 #check mon - fri. Want to pull records for previous day
    

    if (check_day < 5): 
        if is_connected():
            if os.path.isfile('./cases_to_collect.npy'):
                casesForLater = np.load("cases_to_collect.npy")
                desired_date = np.asarray(desired_date) #make desired date into an numpy object
                casesForLater = np.append(casesForLater, desired_date) #append desired date to cases for later
                casesForLater = np.unique(casesForLater) #Make sure there aren't any duplicates
                if len(casesForLater) > 0: #check for days that didn't get run
                    for i in range(len(casesForLater)):
                        runscript(casesForLater[0])
                        casesForLater = np.delete(casesForLater, 0, None)
    
                    np.save("cases_to_collect.npy", casesForLater) #save updates to cases for later
            else:
                runscript(desired_date)
        else:
            #check if cases_to_collect is in directory
            if os.path.isfile('./cases_to_collect.npy'):
                casesForLater = np.load("cases_to_collect.npy")
                casesForLater = np.append(casesForLater, desired_date)
                np.save("cases_to_collect.npy", casesForLater)
            else:
                np.save("cases_to_collect.npy", desired_date)



main()

#Automated in chrontab -e runs everyday at 9
