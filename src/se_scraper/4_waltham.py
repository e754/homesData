import time
import random
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import traceback


base_wait_time = 1
data = pd.read_csv('walthamUsage.csv')

options = uc.ChromeOptions()
# options.add_arxgument("--headless")  # Enable headless mode
options.add_argument("--disable-gpu")  # Optional, for better compatibility
options.add_argument("--disable-blink-features=AutomationControlled")  # Evade detection
options.add_argument("user-agent=" + random.choice([
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.165 Safari/537.36"
]))
options.add_argument("--disable-use_subprocess")


page_to_scrape = uc.Chrome(options=options)

def human_delay(min_wait=0.5, max_wait=2.0):
    time.sleep(random.uniform(min_wait, max_wait))


human_delay()
for i in range (8000, 20000):
    print("Row: ", i)
    if data.iloc[i]['usage'] != "":
        print("not null")
        try:
            print(i,data.iloc[i]['Location'])
            page_to_scrape.get("https://web-server.city.waltham.ma.us/GovernEComponents/WebUserInterfaceUB")
            human_delay()
            parcelIdButton=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_rdblStyles_1').click()
            human_delay()
            select=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_cmdLoadStyleContent').click()
            human_delay()

            id_value = data.iloc[i]['Parcel ID']
            ids = id_value.split()
            input1=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_0')
            input1.send_keys(ids[0])
            input2=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_1')
            input2.send_keys(ids[1])
            human_delay()
            input3=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_2')
            input3.send_keys(ids[2])

            human_delay()

            page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_btnGo').click()
            human_delay()
            page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_cmdFinish').click()
            human_delay()

            page_to_scrape.switch_to.frame(0)
            pmdates1_elements = page_to_scrape.find_elements(By.ID, 'PMDATE1')
            ret= ""
            for i in range(len(pmdates1_elements)):
                ret+=pmdates1_elements[i].text
            data.at[i,'permit dates']=ret
            human_delay()


            page_to_scrape.find_element(By.XPATH,'//*[@id="Text5"]').click()
            human_delay()
            page_to_scrape.switch_to.frame(0)          #//*[@id="CONSUMPTION1"]/table/tbody/tr/td/table/tbody/tr/td/span
            usage=page_to_scrape.find_element(By.XPATH,'//*[@id="Text4"]/p/span/span[2]')
            data.at[i,'usage']=usage.text
            print(usage.text)
            if i%10==0:
                print("downloaded")
                data.to_csv('walthamUsage.csv')
        except Exception as e:
            if i%10==0:
                print("downloaded")
                data.to_csv('walthamUsage.csv')
            print(e)
            traceback.print_exc()  # Prints the full traceback with file and line numbers
            human_delay()


    #objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_1


    
    
