#!/usr/local/opt/python/bin/python3.7
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import requests
from datetime import datetime, timedelta
import numpy as np
import csv

def runscript():
    week_day = datetime.today().weekday() - 1 #0- monday, 1- tuesday 
    if (week_day < 7) & (week_day > 0): ##***Change to make tues-sat

        desired_date = datetime.strftime(datetime.now() - timedelta(1), '%m/%d/%Y')
        county = "Deschutes"
        username = 'AVADES01'
        password = "avades01"

        ##Set up Selenium Driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        
        options.binary_location = "/usr/bin/chromium"
        
        driver = webdriver.Chrome(executable_path="/Users/dylanalbertazzi/Documents/Clients_SEO/ALF_Folder/Court-Download/chromedriver", chrome_options=chrome_options)
        driver.get('https://publicaccess.courts.oregon.gov/PublicAccessLogin/Login.aspx?ReturnUrl=/PublicAccessLogin/default.aspx')

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
            table_data = np.empty([table_length, 5], dtype="|U250")


            i = 0

            #Cycle through each row
            for tr in jj5.find_all('tr')[1:]:
                tds = tr.find_all('td')
                link = tds[0].a
                link = link.get('href')
                #print(link)
                #populate numpy array
                table_data[i, 0] = link
                table_data[i, 1] = tds[0].text #Case Number
                table_data[i, 2] = tds[1].text.replace('\n', ' ') #Description
                table_data[i, 3] = tds[2].contents[0].text #Filed date
                table_data[i, 4] = tds[3].contents[0].text #Type
            
                i += 1

            d_date = datetime.strftime(datetime.now() - timedelta(1), '%m_%d_%Y')
            csv_name = "/Users/dylanalbertazzi/Documents/Clients_SEO/ALF_Folder/Court-Download/case_logs/" + d_date + '.csv'
            with open(csv_name , 'w') as w:
                w = csv.writer(w)
                w.writerow(["Link","Case Number", "Description", "Filed Date", "Type"])
                w.writerows(table_data)
        else:
            print("no cases")

    else:
       
        pass
    return

runscript()


#Automated in chrontab -e runs everyday at 9
