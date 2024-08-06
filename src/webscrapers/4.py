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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import PyPDF2
import fitz
import pdfplumber

base_wait_time = 1
data = pd.read_csv('walthamUsage.csv')
page_to_scrape = webdriver.Chrome()

time.sleep(random.uniform(1, 1) * base_wait_time)
for i in range (19, data.shape[0]):
    try:
        print(i,data.iloc[i]['Location'])
        page_to_scrape.get("https://web-server.city.waltham.ma.us/GovernEComponents/WebUserInterfaceUB")
        time.sleep(2)
        parcelIdButton=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_rdblStyles_1').click()
        time.sleep(1)
        select=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_cmdLoadStyleContent').click()
        time.sleep(1)

        id_value = data.iloc[i]['Parcel ID']
        ids = id_value.split()
        input1=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_0')
        input1.send_keys(ids[0])
        input2=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_1')
        input2.send_keys(ids[1])
        input3=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_2')
        input3.send_keys(ids[2])

        time.sleep(0.5)

        page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_btnGo').click()
        time.sleep(0.5)
        page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_cmdFinish').click()
        time.sleep(2)

        page_to_scrape.switch_to.frame(0)
        pmdates1_elements = page_to_scrape.find_elements(By.ID, 'PMDATE1')
        ret= ""
        for i in range(len(pmdates1_elements)):
            ret+=pmdates1_elements[i].text
        data.at[i,'permit dates']=ret
        time.sleep(2)

        page_to_scrape.find_element(By.XPATH,'//*[@id="Text5"]').click()
        time.sleep(1)
        page_to_scrape.switch_to.frame(0)
        usage=page_to_scrape.find_element(By.XPATH,'//*[@id="CONSUMPTION1"]/table/tbody/tr/td/table/tbody/tr/td/span')
        data.at[i,'usage']=usage.text
        print(usage.text)
        if i%10==0:
            print("downloaded")
            data.to_csv('walthamUsage.csv')
    except:
        print('wtf')

    #objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_1


    
    
