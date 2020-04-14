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

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
chrome_location = 'C:/Users/rbrough/Desktop/chromedriver_win32/chromedriver.exe'

#Option For Choosing a Range of dates
#yesterday = date.today() - timedelta(days=1)
#yesterday.strftime('%A, %B %d, %Y')
df = pd.DataFrame(pd.period_range('July, 17, 2019', freq='B', periods=8))
df.columns = ['DOB']
df = df['DOB'].dt.strftime('%A, %B %d, %Y')
dates = df
#file_name = dates[0]
nas = ["NA", "NA", "NA", "NA", "NA", "NA", "NA"]
# Choose Yesterday

for i in dates:
    m = datetime.date.today()
    y = datetime.datetime.strptime(i,'%A, %B %d, %Y')
    print(y.month)

my_df= []

for i in dates:
    my_df = []
    file_name = i
    y = datetime.datetime.strptime(i, '%A, %B %d, %Y')
    y = y.month
    m = datetime.date.today()
    m = m.month
    print("Starting this loop")
    driver = webdriver.Chrome(chrome_options= options,
                              executable_path= chrome_location)
    url = "https://web6.seattle.gov/courts/ECFPortal/default.aspx"
    driver.get(url)

    ## Find Courtroom Calendar element
    element_calendar = driver.find_element_by_xpath("//span[@class='rtsTxt' and text()='Courtroom Calendar']")

    ## Navigate to Courtroom Calendar
    element_calendar.click()
    # "ContentPlaceHolder1_CourtSession1_ddlCourtrooms"
    wait = WebDriverWait(driver, 200)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "//option[@value='KCJ2']")))
    element.click()

    ## Wait for page to load
    time.sleep(5)

    ## Click to choose date on calendar popup
    driver.find_element_by_class_name("rcCalPopup").click()

    ## Calculating # of Months
     Last Year Click: p = m + (12-y)
    # This Year Click
    # p = m - y

    ## Click Back to Month
    for x in range(p):
        print(x)
        element = driver.find_element_by_xpath(
               '// *[ @ id = "ctl00_ContentPlaceHolder1_CourtSession1_DateNavigationBar2_rdtPicker_calendar_NP"]')
        driver.execute_script("arguments[0].click();", element)

    # Click Date
    driver.find_element_by_xpath("//*[@title='" + i + "']").click()

    # Count Number of Rows (set loop to number of rows)
    count1 = driver.find_elements_by_class_name("rgRow")
    count2 = driver.find_elements_by_class_name("rgAltRow")
    c = int(len(count1))+int(len(count2))

    for x in range(c):
        print(x)
        try:
            x = str(x)
            time.sleep(8)
            element = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_CourtSession1_CourtSessionView1_rgCourtSession_ctl00__' + x + '"]')
            driver.execute_script("arguments[0].click();", element)
            time.sleep(5)

            #Name
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_CaseDetails1_lblDefendantName"]'
            name = driver.find_element_by_xpath(xpath)
            name = name.text
            print(name)

            # Case Number
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_CaseDetails1_lblCaseNumber"]'
            case_number = driver.find_element_by_xpath(xpath)
            case_number = case_number.text
            print(case_number)

            #Case Type
            try:
                xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_CaseDetails1_lblCaseType"]'
                case_type = driver.find_element_by_xpath(xpath)
                case_type = case_type.text
                print(case_type)
            except:
                case_type = "NA"

            # Obligation for the Defendant
            try:
                xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_CaseDetails1_lblTotalDue"]'
                obligation = driver.find_element_by_xpath(xpath)
                obligation = obligation.text
                print(obligation)
            except:
                obligation = "NA"

            # Attorney
            try:
                xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_CaseDetails1_lbDefenseAttorney"]'
                attorney = driver.find_element_by_xpath(xpath)
                attorney = attorney.text
                print(attorney)
            except:
                attorney = "NA"

            # Click onto obligations
            element = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_rtsCaseSpecifics"]/div/ul/li[5]')
            driver.execute_script("arguments[0].click();", element)

            time.sleep(10)

            # Scrape Ob History
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_ObligationList1_rgObls_ctl00"]/tbody'
            all_obligations = driver.find_element_by_xpath(xpath)
            all_obligations = all_obligations.text

            # Click onto Events
            element = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_rtsCaseSpecifics"]/div/ul/li[4]/a/span/span/span')
            driver.execute_script("arguments[0].click();", element)

            time.sleep(10)

            # Scrape Event History
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_CaseEventList1_rgCaseEvents_ctl00"]/tbody'
            events = driver.find_element_by_xpath(xpath)
            events = events.text

            d ={'Defendant': name,
                'Attorney': attorney,
                'Case_Number': case_number,
                'Bail_Due': obligation,
                'hearing_date': i,
                'Case_Type': case_type,
                'Events': events,
                'Obligations_total': all_obligations
                }

            my_df.append(d)

        except:
            pass

    driver.quit()
    my_df = pd.DataFrame(my_df)
        #my_df = my_df.join(my_df['Events'].str.split('\n', expand=True).add_prefix('Event'))
    my_df.to_csv('G:/My Drive/LEO/Projects/ORCA LIFT Court/7. Research/4. Data Collection/Raw Data/' + file_name + '.csv')
