from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime, timedelta
import requests
import numpy as np
import csv
import pyodbc

server_name = "tcp:lawdata.database.windows.net,1433"
db_name = "CourtData"

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=server_name;'
                      'Database=db_name;'
                      'Trusted_Connection=yes;')


desired_date = datetime.strftime(datetime.now() - timedelta(1), '%m_%d_%Y')
csv_name = desired_date + '.csv'
response = requests.get("http://localhost:8000/sample_page.html")
soup = BeautifulSoup(response.content, 'html.parser')

day = datetime.strftime(datetime.now() - timedelta(1), '%m/%d/%Y')
week_day = datetime.today().weekday() - 1 #0- monday, 1- tuesday
#time = datetime.date.today()-datetime.timedelta(1)

print(day)
#print(soup.prettify())
#print(list(soup.children))
jj = soup.find_all('table')
jj5 = jj[5]

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
    table_data[i, 2] = tds[1].text #Description
    table_data[i, 3] = tds[2].contents[0].text #Filed date
    table_data[i, 4] = tds[3].contents[0].text #Type
 
    i += 1


with open('test.csv', 'w') as f:
    w = csv.writer(f)
    w.writerow(["Link","Case Number", "Description", "Filed Date", "Type"])
    w.writerows(table_data)
  

