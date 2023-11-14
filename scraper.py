from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import time

total = []
#set executable path
driver=webdriver.Chrome()
pages = 7
df = pd.DataFrame()

for page in range(1, pages+1):
    #set url
    url = "https://www.courtlistener.com/?q=artificial%20intelligence&type=r&order_by=score%20desc&filed_after=01%2F01%2F2023&filed_before=01%2F31%2F2023"
    driver.get(url)
    driver.implicitly_wait(30)

    cases = driver.find_elements(By.TAG_NAME, "article")
    total = len(cases)
    print(len(cases))
    for i in range(total):
        j = len(df)
        cases = driver.find_elements(By.TAG_NAME, "article")
        case = cases[i]
        case.find_elements(By.TAG_NAME,'h3')[0].find_elements(By.TAG_NAME,'a')[0].click()

        df.at[j,'Name'] = driver.find_elements(By.CSS_SELECTOR,'div h1')[0].text
        df.at[j,'Court Level'] = driver.find_elements(By.CSS_SELECTOR,'div h2')[2].text

        items = driver.find_elements(By.CSS_SELECTOR,'p.bottom')
        print(len(items))
        for count in range(len(items)):
            try:
                df.at[j,items[count].find_element(By.CLASS_NAME, 'meta-data-header').text.replace(':','')] = items[count].find_element(By.CLASS_NAME, 'meta-data-value').text
            except:
                print('error')

        df.at[j,'Main Doc Link'] = driver.find_elements(By.XPATH,"//*[contains(text(), 'Main Doc')]")[0].get_attribute('href')
        #go back to the original screen
        driver.execute_script("window.history.go(-1)")
        driver.implicitly_wait(2)
    #driver.find_element(By.CLASS_NAME, 'fa-caret-right').click()

driver.quit()
df.replace(np.nan, '')
df.to_csv('ai_cases_jan_2023_1.csv')