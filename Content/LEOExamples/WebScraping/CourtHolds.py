##################################################################
# Scraping Data on Holds
# Author: bb
# Date: 8-9-2019
##################################################################

# Step 1: Imports
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
from datetime import date, timedelta
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import re

# Web Options
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')

# File Name
today = date.today()
file_name = today.strftime('%A, %B %d, %Y')
chrome_location = 'C:/Users/rbrough/Desktop/chromedriver_win32/chromedriver.exe'
# Step 2: Create a list of booking Numbers from SMC Court Calendar

driver = webdriver.Chrome(chrome_options=options,executable_path=chrome_location)
url = "https://web6.seattle.gov/courts/ECFPortal/default.aspx"
driver.get(url)

# Find Courtroom Calendar element
element_calendar = driver.find_element_by_xpath("//span[@class='rtsTxt' and text()='Courtroom Calendar']")

# Navigate to Courtroom Calendar
element_calendar.click()

# "ContentPlaceHolder1_CourtSession1_ddlCourtrooms"
wait = WebDriverWait(driver, 200)
element = wait.until(EC.visibility_of_element_located((By.XPATH, "//option[@value='KCJ2']")))
element.click()

# Wait for page to load
time.sleep(5)

# Count Number of Rows (set loop to number of rows)
count1 = driver.find_elements_by_class_name("rgRow")
count2 = driver.find_elements_by_class_name("rgAltRow")
c = int(len(count1))+int(len(count2))

my_df = []
bookings =[]

for x in range(c):
    print(x)
    try:
        x = str(x)
        time.sleep(5)
        element = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_CourtSession1_CourtSessionView1_rgCourtSession_ctl00__' + x + '"]')
        driver.execute_script("arguments[0].click();", element)
        time.sleep(5)

        # Name
        xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_CaseDetails1_lblDefendantName"]'
        name = driver.find_element_by_xpath(xpath)
        name = name.text

        # Case Number
        xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_CaseDetails1_lblCaseNumber"]'
        case_number = driver.find_element_by_xpath(xpath)
        case_number = case_number.text

        # Click onto Events
        element = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_rtsCaseSpecifics"]/div/ul/li[4]/a/span/span/span')
        driver.execute_script("arguments[0].click();", element)

        time.sleep(5)

        # Store Page, Look for Booking Number
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        booking = soup.find_all(text=re.compile("BA#(.*)|BA #(.*)"))
        rel_booking = booking[0]
        rel_booking = rel_booking[-9:]


        d = {'Case_Number': case_number,
            'Defendant': name,
            'BA': rel_booking
             }

        bookings.append(rel_booking)
        my_df.append(d)
    except:
        pass

driver.quit()
my_df = pd.DataFrame(my_df)

# Step 3: Pull Hold Info From JILS
driver = webdriver.Chrome(chrome_options=options,executable_path=chrome_location)
url = "https://ingress.kingcounty.gov/Public/JILS/default.aspx?"
driver.get(url)

holds_df = []
x = 1
for case in bookings:
    print(case)
    print(x)
    # Populate Search Bar
    button = driver.find_element_by_xpath('//*[@id="txtBa"]')
    button.clear()
    button.send_keys(case)

    # Click Enter
    element = driver.find_element_by_xpath('//*[@id="btnsearchba"]')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(5)
    # Click on to Def Name
    element = driver.find_element_by_xpath('//*[@id="tableResults"]/tbody/tr/td[1]/a')
    driver.execute_script("arguments[0].click();", element)

    # Wait a long time; if errors outs, make this longer.
    time.sleep(25)

    # Copy All Holds Info
    xpath = '//*[@id="resultsaccordion"]'
    holds = driver.find_element_by_xpath(xpath)
    holds = holds.text
    print(holds)

    # Click Done
    element = driver.find_element_by_xpath('// *[ @ id = "badetails"] / div / div / div[3] / button')
    driver.execute_script("arguments[0].click();", element)

    h = {'BA': case,
         'Hold_Info': holds}

    holds_df.append(h)

    # Counting Loop
    x = x + 1

holds_df = pd.DataFrame(holds_df)

# Matching Holds Data to Identifiers
holds_df['Obs'] = holds_df.reset_index().index
my_df['Obs'] = my_df.reset_index().index

# Testing Merges
df = pd.merge(my_df, holds_df, on=['Obs', 'BA'])

# Save to CSV
df.to_csv('G:/My Drive/LEO/Projects/ORCA LIFT Court/7. Research/4. Data Collection/Daily_Scraped_Data/Holds/'+file_name+'_Holds.csv')
