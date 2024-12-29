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




# Set up the WebDriver
def is_element_present(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except NoSuchElementException:
        return False

base_wait_time = 1

# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (optional)

# Initialize WebDriver
page_to_scrape = webdriver.Chrome()

page_to_scrape.get("https://www2.invoicecloud.com/portal/(S(xpf5wlmn1ic0bk10nirogzfn))/2/customerlocatorresults.aspx?iti=42&bg=5e51c1b1-f981-4a8c-ad97-3ffd74eacb9b&vsii=182")
time.sleep(random.uniform(1, 1) * base_wait_time)

# script_dir = os.path.dirname(__file__)
# csv_path = os.path.join(script_dir, '..', 'data', 'PatriotArlington.csv')
data = pd.read_csv('waterUsage.csv')

for i in range (2300,3300):
    print(i)
    address=data.iloc[i]['Location']
    if i%10==0:
        data.to_csv("waterUsage.csv")
        print("downloaded")
    try:
        page_to_scrape.get("https://www2.invoicecloud.com/portal/(S(xpf5wlmn1ic0bk10nirogzfn))/2/customerlocatorresults.aspx?iti=42&bg=5e51c1b1-f981-4a8c-ad97-3ffd74eacb9b&vsii=182")
        address = address.replace("  ", " ")
        time.sleep(2)
        inputAddress =page_to_scrape.find_element(By.ID, 'ctl00_ctl00_cphBody_cphBodyLeft_ctrlVSInputs_rptInputs_ctl02_txtValue') #ctl00_ctl00_cphBody_cphBodyLeft_ctrlVSInputs_rptInputs_ctl02_txtValue
        inputAddress.send_keys(address)
        searchButton =page_to_scrape.find_element(By.ID, 'ctl00_ctl00_cphBody_cphBodyLeft_btnSearch').click()
        time.sleep(random.uniform(2, 2) * base_wait_time)
        try:
            WebDriverWait(page_to_scrape, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
            )

        except TimeoutException:
            print("Loading took too much time!")
            page_to_scrape.quit()

        tbody = page_to_scrape.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        row=rows[0]
        view_invoice_link = row.find_element(By.PARTIAL_LINK_TEXT, "View Invoice")
        view_invoice_link.click()
        time.sleep(2)

        time.sleep(random.uniform(2, 3) * base_wait_time)
        page_to_scrape.switch_to.window(page_to_scrape.window_handles[1])


        pdf_url = page_to_scrape.current_url
        import requests
        response = requests.get(pdf_url)
        with open('document.pdf', 'wb') as f:
            f.write(response.content)

    # Extract text from the downloaded PDF
        pdf_document = fitz.open('document.pdf')
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        # print(text)

        import pdfplumber

        def getLines(pdf_path):
            with pdfplumber.open(pdf_path) as pdf:
                # Iterate through pages
                for page in pdf.pages:
                    text = page.extract_text()
                    lines = text.split('\n')
                    return lines
                    # print(lines)
        pdf_path = 'document.pdf'  # Update with the path to your PDF
        lines = getLines(pdf_path)
        output=None
        for a in lines:
            splitLine=a.split()
            if splitLine[0]=='TIER1' and splitLine[1]=='0' and splitLine[2]=='-' and splitLine[3]=='15':
                output=splitLine[5]
            

        page_to_scrape.close()

        page_to_scrape.switch_to.window(page_to_scrape.window_handles[0])
        data.at[i,'water usage']=output
        print(address,output)
    except Exception as e:
        data.at[i,'water usage']='?'
        print(address,"address issue")
        print(e)
