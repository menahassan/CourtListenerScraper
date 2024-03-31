from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import time
from selenium.webdriver.chrome.options import Options

total = []
#set executable path
options = Options()
options.add_argument("--headless=new")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options)
pages = 250
cols = ['Name','Court Level','Last Updated', 'Assigned To', 'Citation', 'Date Filed', 'Date of Last Known Filing', 'Jury Demand', 'Main Doc Link', 'Cause', 'Nature of Suit', 'Jurisdiction Type', 'Date Terminated', 'Referred To']
df = pd.DataFrame(columns=cols)
url = "https://www.courtlistener.com/?type=r&type=r&q=artificial+intelligence&order_by=score+desc&page=100"
driver.get(url)
for page in range(100, pages+1):
    #set url
    driver.implicitly_wait(30)

    cases = driver.find_elements(By.TAG_NAME, "article")
    total = len(cases)
    print('page', page)
    for i in range(total):
        j = len(df)
        cases = driver.find_elements(By.TAG_NAME, "article")
        print(len(cases))
        if(i < len(cases)):
            case = cases[i]
            case.find_elements(By.TAG_NAME,'h3')[0].find_elements(By.TAG_NAME,'a')[0].click()

            df.at[j,'Name'] = driver.find_elements(By.CSS_SELECTOR,'div h1')[0].text
            #print(df.at[j,'Name'], len(driver.find_elements(By.CSS_SELECTOR,'div h2')))
            df.at[j,'Court Level'] = driver.find_elements(By.CSS_SELECTOR,'div h2')[2].text

            items = driver.find_elements(By.CSS_SELECTOR,'p.bottom')
            for count in range(len(items)):
                try:
                    colName = items[count].find_element(By.CLASS_NAME, 'meta-data-header').text.replace(':','')
                    if(colName in cols):
                        df.at[j,colName] = items[count].find_element(By.CLASS_NAME, 'meta-data-value').text
                except:
                    print('error')

            df.at[j,'Main Doc Link'] = driver.find_elements(By.XPATH,"//*[contains(text(), 'Main Doc')]")[0].get_attribute('href')
            #go back to the original screen
            driver.execute_script("window.history.go(-1)")
            driver.implicitly_wait(3)
    driver.find_element(By.CLASS_NAME, 'fa-caret-right').click()
    driver.implicitly_wait(2)

driver.quit()
df.replace(np.nan, '')
df.to_csv('ai_cases_all_3.csv')