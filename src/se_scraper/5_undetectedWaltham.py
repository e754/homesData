import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc

# Constants
base_wait_time = 1
data = pd.read_csv('walthamUsage.csv')

# Setup Chrome Options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-popup-blocking")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Initialize WebDriver
page_to_scrape = Chrome(options=options)

# Patch Navigator and WebDriver detection
page_to_scrape.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    """
})

# Helper Functions
def random_delay(multiplier=1):
    """Introduce a random delay to mimic human behavior."""
    time.sleep(random.uniform(0.5, 2.0) * multiplier)

# Main Loop
for i in range(4, data.shape[0]):
    print(i)
    try:
        print(i, data.iloc[i]['Location'])
        
        # Load page
        page_to_scrape.get("https://web-server.city.waltham.ma.us/GovernEComponents/WebUserInterfaceUB")
        random_delay()

        # Click on Parcel ID Button
        page_to_scrape.find_element(By.ID, 'objWP_reportparameterstyle_ESearchManager1_rdblStyles_1').click()
        random_delay()

        # Load Parcel Style
        page_to_scrape.find_element(By.ID, 'objWP_reportparameterstyle_ESearchManager1_cmdLoadStyleContent').click()
        random_delay()

        # Fill in Parcel ID
        id_value = data.iloc[i]['Parcel ID']
        ids = id_value.split()
        
        input1 = page_to_scrape.find_element(By.ID, 'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_0')
        input1.send_keys(ids[0])
        input2 = page_to_scrape.find_element(By.ID, 'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_1')
        input2.send_keys(ids[1])
        input3 = page_to_scrape.find_element(By.ID, 'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_2')
        input3.send_keys(ids[2])
        
        random_delay()

        # Submit and finish
        page_to_scrape.find_element(By.ID, 'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_btnGo').click()
        random_delay()
        page_to_scrape.find_element(By.ID, 'objWP_reportparameterstyle_ESearchManager1_cmdFinish').click()
        random_delay()

        # Switch to Frame and Collect Permit Dates
        page_to_scrape.switch_to.frame(0)
        pmdates1_elements = page_to_scrape.find_elements(By.ID, 'PMDATE1')
        ret = " ".join([elem.text for elem in pmdates1_elements])
        data.at[i, 'permit dates'] = ret
        random_delay()

        # Extract Usage
        page_to_scrape.find_element(By.XPATH, '//*[@id="Text5"]').click()
        random_delay()
        page_to_scrape.switch_to.frame(0)
        usage = page_to_scrape.find_element(By.XPATH, '//*[@id="CONSUMPTION1"]/table/tbody/tr/td/table/tbody/tr/td/span')
        data.at[i, 'usage'] = usage.text
        print(usage.text)

        # Save Progress
        if i % 10 == 0:
            print("Downloaded data up to index", i)
            data.to_csv('walthamUsage.csv', index=False)

    except Exception as e:
        print(f"Error at index {i}: {str(e)}")
        random_delay(100)

# Quit Browser
page_to_scrape.quit()
