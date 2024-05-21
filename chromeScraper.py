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

# Install the appropriate WebDriver if needed
# Ensure your WebDriver executable is in the system PATH or specify the path to it

# Set up the WebDriver
page_to_scrape = webdriver.Chrome()  # Update path if necessary

# Open the initial webpage
page_to_scrape.get("https://unipaygold.unibank.com/transactioninfo.aspx?TID=3154")

print("website scraper")

time.sleep(1)

# Locate and click the close button on the modal
button = page_to_scrape.find_element(By.ID, 'js-modal-close')
button.click()
print("popup closed")



# Wait for the modal to close
time.sleep(1)

# Locate and click the bill search link
link_element = page_to_scrape.find_element(By.LINK_TEXT, 'To search for your bill - click here')
link_element.click()
print("hyper clicked")

time.sleep(1)

Fulladdress="16          WICKHAM ROAD"

 
cleaned_address = re.sub(r'^\d+\s*', '', Fulladdress)

adressInput = page_to_scrape.find_element(By.NAME, "ctl00$ctl00$LayoutArea$MainContent$Transaction1$BillSearch1$23990")
print("username found")
adressInput.send_keys(cleaned_address)
page_to_scrape.find_element(By.ID, "ctl00_ctl00_LayoutArea_MainContent_Transaction1_BillSearch1_lbtnSearch").click()
time.sleep(2)

xpath = f"//div[contains(text(), '{Fulladdress.strip()}')]"

selectThing=page_to_scrape.find_element(By.XPATH,xpath).click()
time.sleep(2)

page_to_scrape.find_element(By.ID,"ctl00_ctl00_LayoutArea_MainContent_Transaction1_lbtnContinue").click()

time.sleep(1)

page_to_scrape.find_element(By.ID,"ctl00_ctl00_LayoutArea_MainContent_Transaction1_lbtnContinue").click()





# Wait for the bi
