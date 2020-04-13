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

# Set things Ups
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
file_location = 'G:/My Drive/LEO/Projects/ORCA LIFT Court/7. Research/4. Data Collection/Daily_Scraped_Data/'
chrome_location = 'C:/Users/rbrough/Desktop/chromedriver_win32/chromedriver.exe'

#Option For Choosing a Range of dates
yesterday = date.today() - timedelta(days=1)
yesterday.strftime('%A, %B %d, %Y')

df = pd.DataFrame(pd.period_range(yesterday, freq='B', periods=1))
#df = pd.DataFrame(pd.period_range(yesterday, freq='D', periods=1))
df.columns = ['DOB']
df = df['DOB'].dt.strftime('%A, %B %d, %Y')
dates = df
file_name = dates[0]
nas = ["NA", "NA", "NA", "NA", "NA", "NA", "NA"]
# Choose Yesterday

my_df= []

for i in dates:
    print("Starting this loop")
    y = datetime.datetime.strptime(i, '%A, %B %d, %Y')
    y = y.month
    m = datetime.date.today()
    m = m.month

    driver = webdriver.Chrome(chrome_options=options,
                              executable_path=chrome_location)
    #driver = webdriver.Chrome(chrome_options= options, executable_path='C:/Users/rbrough/AppData/Local/Temp/Temp2_chromedriver_win32.zip/chromedriver.exe')
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

    ## Try to find date on today's calendar; if not, click one month back
    ## Calculating # of Months
    # Last Year Click: p = m + (12-y)
    # This Year Click
    p = m - y

    ## Click Back to Month
    for x in range(p):
        print(x)
        element = driver.find_element_by_xpath(
            '// *[ @ id = "ctl00_ContentPlaceHolder1_CourtSession1_DateNavigationBar2_rdtPicker_calendar_NP"]')
        driver.execute_script("arguments[0].click();", element)

    # Count Number of Rows (set loop to number of rows)
    count1 = driver.find_elements_by_class_name("rgRow")
    count2 = driver.find_elements_by_class_name("rgAltRow")
    c = int(len(count1))+int(len(count2))
    print(c)
    

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

            # Scrape All Obligations
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_CaseDetails1_lblTotalDue"]'
            total_obligations = driver.find_element_by_xpath(xpath)
            total_obligations = total_obligations.text

            ob = []
            #l = driver.find_elements_by_class_name("rgRow")
            #l2 = driver.find_elements_by_class_name("rgAltRow")
            list = ["0", "1", "2", "3", "4"]

            for y in list:
                try:
                    xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_ObligationList1_rgObls_ctl00__' + y + '"] / td[1]'
                    ob_type = driver.find_element_by_xpath(xpath)
                    ob_type = ob_type.text
                    print(ob_type)

                    xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_ObligationList1_rgObls_ctl00__' + y + '"] / td[2]'
                    ob_og_amount = driver.find_element_by_xpath(xpath)
                    ob_og_amount = ob_og_amount.text
                    print(ob_og_amount)

                    xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_ObligationList1_rgObls_ctl00__' + y + '"] / td[3]'
                    ob_balance = driver.find_element_by_xpath(xpath)
                    ob_balance = ob_balance.text
                    xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_ObligationList1_rgObls_ctl00__' + y + '"] / td[4]'
                    ob_duedate = driver.find_element_by_xpath(xpath)
                    ob_duedate = ob_duedate.text
                    xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_ObligationList1_rgObls_ctl00__' + y + '"] / td[5]'
                    ob_enddate = driver.find_element_by_xpath(xpath)
                    ob_enddate = ob_enddate.text
                    xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_ObligationList1_rgObls_ctl00__' + y + '"] / td[8]'
                    ob_endreas = driver.find_element_by_xpath(xpath)
                    ob_endreas = ob_endreas.text
                    xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_ObligationList1_rgObls_ctl00__' + y + '"] / td[11]'
                    ob_remarks = driver.find_element_by_xpath(xpath)
                    ob_remarks = ob_remarks.text
                    ob.append(ob_type)
                    ob.append(ob_og_amount)
                    ob.append(ob_balance)
                    ob.append(ob_duedate)
                    ob.append(ob_enddate)
                    ob.append(ob_endreas)
                    ob.append(ob_remarks)
                except:
                    pass

            # Click onto Events
            element = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_rtsCaseSpecifics"]/div/ul/li[4]/a/span/span/span')
            driver.execute_script("arguments[0].click();", element)

            time.sleep(10)

            # Scrape Event History
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_CaseInfo1_rpbCaseInfo_i0_CaseEventList1_rgCaseEvents_ctl00"]/tbody'
            events = driver.find_element_by_xpath(xpath)
            print(events)
            events = events.text

            d ={'Defendant': name,
                'Attorney': attorney,
                'Case_Number': case_number,
                'Bail_Due': obligation,
                'hearing_date': i,
                'Case_Type': case_type,
                'OB_Type_1': ob[0],
                'OB_Original_Amount_1': ob[1],
                'OB_Balance_1': ob[2],
                'OB_DueDate_1': ob[3],
                'OB_EndDate_1': ob[4],
                'OB_EndReason_1': ob[5],
                'OB_Remarks_1': ob[6],
                'Events': events,
                'Total_Obligations':total_obligations
                }

            try:
                g = {'OB_Type_2': ob[7],
                     'OB_Original_Amount_2': ob[8],
                     'OB_Balance_2': ob[9],
                     'OB_DueDate_2': ob[10],
                     'OB_EndDate_2': ob[11],
                     'OB_EndReason_2': ob[12],
                     'OB_Remarks_2': ob[13]
                     }
            except:
                ob.extend(nas)
                g = {'OB_Type_2': ob[7],
                     'OB_Original_Amount_2': ob[8],
                     'OB_Balance_2': ob[9],
                     'OB_DueDate_2': ob[10],
                     'OB_EndDate_2': ob[11],
                     'OB_EndReason_2': ob[12],
                     'OB_Remarks_2': ob[13]
                     }
            try:
                a = {'OB_Type_3': ob[14],
                    'OB_Original_Amount_3': ob[15],
                    'OB_Balance_3': ob[16],
                    'OB_DueDate_3': ob[17],
                    'OB_EndDate_3': ob[18],
                    'OB_EndReason_3': ob[19],
                    'OB_Remarks_3': ob[20]
                     }
            except:
                ob.extend(nas)
                a = {'OB_Type_3': ob[14],
                     'OB_Original_Amount_3': ob[15],
                     'OB_Balance_3': ob[16],
                     'OB_DueDate_3': ob[17],
                     'OB_EndDate_3': ob[18],
                     'OB_EndReason_3': ob[19],
                     'OB_Remarks_3': ob[20]
                     }
            try:
                b = {'OB_Type_4': ob[21],
                     'OB_Original_Amount_4': ob[22],
                     'OB_Balance_4': ob[23],
                     'OB_DueDate_4': ob[24],
                     'OB_EndDate_4': ob[25],
                     'OB_EndReason_4': ob[26],
                     'OB_Remarks_4': ob[27]
                     }
            except:
                ob.extend(nas)
                b = {'OB_Type_4': ob[21],
                     'OB_Original_Amount_4': ob[22],
                     'OB_Balance_4': ob[23],
                     'OB_DueDate_4': ob[24],
                     'OB_EndDate_4': ob[25],
                     'OB_EndReason_4': ob[26],
                     'OB_Remarks_4': ob[27]
                     }
            try:
                f = {'OB_Type_5': ob[28],
                     'OB_Original_Amount_5': ob[29],
                     'OB_Balance_5': ob[30],
                     'OB_DueDate_5': ob[31],
                     'OB_EndDate_5': ob[32],
                     'OB_EndReason_5': ob[33],
                     'OB_Remarks_5': ob[34]
                     }
            except:
                ob.extend(nas)
                f = {'OB_Type_5': ob[28],
                     'OB_Original_Amount_5': ob[29],
                     'OB_Balance_5': ob[30],
                     'OB_DueDate_5': ob[31],
                     'OB_EndDate_5': ob[32],
                     'OB_EndReason_5': ob[33],
                     'OB_Remarks_5': ob[34]
                     }
            print("loop")
            d.update(a)
            d.update(b)
            d.update(f)
            d.update(g)
            my_df.append(d)
        except:
            pass

driver.quit()
my_df = pd.DataFrame(my_df)

# Identifying Eligibility
my_df= my_df.join(my_df['Events'].str.split('\n', expand=True).add_prefix('Event'))
print(my_df)

# Save
my_df.to_csv(file_location+file_name+'.csv')

# Done
print("finished!")
