import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import random
import numpy as np

# Set up the WebDriver
def is_element_present(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except NoSuchElementException:
        return False
def getBill(address):
    try:
        base_wait_time = 1
        parts = address.split()
        number = int(parts[0])
        name = parts[1]    
        page_to_scrape = webdriver.Chrome()  # Update path if necessary
        #access the webpage
        page_to_scrape.get("https://unipaygold.unibank.com/transactioninfo.aspx?TID=3154")
        time.sleep(random.uniform(0.5, 1.5) * base_wait_time)

        # Locate and click the close button on the modal
        button = page_to_scrape.find_element(By.ID, 'js-modal-close')
        button.click()
        print("popup closed")
        time.sleep(random.uniform(0.5, 1.5) * base_wait_time)

        # Locate and click the bill search link
        link_element = page_to_scrape.find_element(By.LINK_TEXT, 'To search for your bill - click here')
        link_element.click()
        time.sleep(random.uniform(0.5, 1.5) * base_wait_time)

        #search road name
        Fulladdress=f"{number}          {name}"
        adressInput = page_to_scrape.find_element(By.NAME, "ctl00$ctl00$LayoutArea$MainContent$Transaction1$BillSearch1$23990")
        adressInput.send_keys(name)
        page_to_scrape.find_element(By.ID, "ctl00_ctl00_LayoutArea_MainContent_Transaction1_BillSearch1_lbtnSearch").click()
        time.sleep(random.uniform(1, 2.0) * base_wait_time)

        #reformat roadname in order to find information
        addressFound=True
        xpath0 = f"//div[contains(text(), '{Fulladdress.strip()}')]"
        addressMinus=Fulladdress=f"{number-2}     {number}   {name}"
        addressPlus=Fulladdress=f"{number}     {number+2}   {name}"
        xpath1 = f"//div[contains(text(), '{addressMinus.strip()}')]"
        xpath2 = f"//div[contains(text(), '{addressPlus.strip()}')]"

        #check for the three formats
        if is_element_present(page_to_scrape,'xpath',xpath0):
            print("thing clciked")
            selectThing=page_to_scrape.find_element(By.XPATH,xpath0)
            selectThing.click()
        elif is_element_present(page_to_scrape,'xpath',xpath1):
            selectThing=page_to_scrape.find_element(By.XPATH,xpath1)
            selectThing.click()
        elif is_element_present(page_to_scrape,'xpath',xpath2):
            selectThing=page_to_scrape.find_element(By.XPATH,xpath2)
            selectThing.click()
        else:
            addressFound=False

        #if we sucessfulyl found informati9on
        if addressFound:
            time.sleep(random.uniform(0.5, 1.5) * base_wait_time)
            page_to_scrape.find_element(By.ID,"ctl00_ctl00_LayoutArea_MainContent_Transaction1_lbtnContinue").click()
            time.sleep(random.uniform(0.5, 1.5) * base_wait_time)
            label = page_to_scrape.find_element(By.ID, 'ctl00_ctl00_LayoutArea_MainContent_Transaction1_lblAmountDue')
            full_text = label.text
            amount_due = re.search(r'\$([0-9]+\.[0-9]+)', full_text).group(1)
            print(amount_due)
            return(amount_due) 

        else:
            return "NID"
            print(name, number, "can't find address in database")
    except:

        df.to_csv("waterBill.csv")

df = pd.read_csv('waterBill.csv')

for i in range(320,df.shape[0]):
    if pd.isna(df.at[i, 'bill']):
        print(i)
        address=df.iloc[i]['Location']
        cost=getBill(address)
        print(cost)
        df.at[i,'bill']=cost
        if i%20==0:
            df.to_csv("waterBill.csv")
            print("downloaded")




# df.loc[df['bill'].isnull(), 'bill'] = df.loc[df['bill'].isnull(), 'location'].apply(getBill)

