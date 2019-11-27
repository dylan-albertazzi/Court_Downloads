#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import requests

# response = requests.get("https://publicaccess.courts.oregon.gov/PublicAccessLogin/Login.aspx?ReturnUrl=%2fPublicAccessLogin%2fdefault.aspx")
# soup = BeautifulSoup(response.text, 'html.parser')



desired_date = "11/20/19"
county = "Deschutes"
username = 'AVADES01'
password = "avades01"

##Set up Selenium Driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "/usr/bin/chromium"
driver = webdriver.Chrome("/Users/dylanalbertazzi/Desktop/Court-Download/chromedriver")
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



date_early = driver.find_element_by_id("DateFiledOnAfter")
date_early.send_keys(desired_date)
date_old = driver.find_element_by_id("DateFiledOnBefore")
date_old.send_keys(desired_date)

submit_button2 = driver.find_element_by_id("SearchSubmit") #Form to get list of filed cases
submit_button2.click()

##Download desired data



##Save



##Send Email?