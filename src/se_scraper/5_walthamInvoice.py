import time
import random
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import traceback
import pdfplumber
import os



base_wait_time = 1
data = pd.read_csv('walthamInvoice.csv')

#anti detection systems from undetectable chrome
download_dir = f"{os.getcwd()}/pdfHolder"

options = uc.ChromeOptions()
# options.add_arxgument("--headless")  # Enable headless mode
options.add_argument("--disable-gpu")  # Optional, for better compatibility
options.add_argument("--disable-blink-features=AutomationControlled")  # Evade detection



options.add_argument("--no-sandbox")  # Optional: Disable sandboxing
options.add_argument(f"--download-dir={download_dir}")
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,  # Prevents Chrome's PDF viewer from opening
    "safebrowsing.enabled": True
})
options.add_argument("--disable-use_subprocess")


page_to_scrape = uc.Chrome(options=options)

def human_delay(min_wait=0.5, max_wait=1.5):
    time.sleep(random.uniform(min_wait, max_wait))


for houseNumber in range (4840, 10000):
    if houseNumber%10==0:
        print("downloaded")
        data.to_csv('walthamInvoice.csv')
    print("Row: ", houseNumber)
    if True:
        print("not null")
        try:
            print(houseNumber,data.iloc[houseNumber]['Location'])
            page_to_scrape.get("https://web-server.city.waltham.ma.us/GovernEComponents/WebUserInterfaceUB")
            human_delay(0.25, 0.5)
            parcelIdButton=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_rdblStyles_1').click()
            human_delay(0.25, 0.5)
            select=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_cmdLoadStyleContent').click()
            human_delay()

            id_value = data.iloc[houseNumber]['Parcel ID']
            ids = id_value.split()
            input1=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_0')
            input1.send_keys(ids[0])
            input2=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_1')
            input2.send_keys(ids[1])
            input3=page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_2')
            input3.send_keys(ids[2])

            human_delay()

            page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_btnGo').click()
            page_to_scrape.find_element(By.ID,'objWP_reportparameterstyle_ESearchManager1_cmdFinish').click()
            human_delay()

            page_to_scrape.switch_to.frame(0)
            pmdates1_elements = page_to_scrape.find_elements(By.ID, 'PMDATE1')
            ret= ""
            for i in range(len(pmdates1_elements)):
                ret+=pmdates1_elements[i].text
            data.at[houseNumber,'permit dates']=ret
            human_delay()

            #to invoicecloud
            page_to_scrape.find_element(By.XPATH, '//*[@id="Text23"]/p/span/a/span').click()
            human_delay()
            
            page_html = page_to_scrape.page_source

# Save the HTML to a text file
            with open("page_source.txt", "w", encoding="utf-8") as file:
                file.write(page_html)

            view_invoice_link = page_to_scrape.find_element(By.XPATH, "/html/body/div[2]/form/table/tbody/tr/td[1]/div[4]/div[1]/table/tbody/tr/td[10]/div[2]/a")
            view_invoice_link.click() #ctl00_ctl00_cphBody_cphBodyLeft_ctl01_outerRepeater_ctl01_Repeater1_ctl01_lnkInvoicePDF
            human_delay()

            folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pdfHolder')

# List all files in the folder
            files_in_folder = os.listdir(folder_path)

# Filter for PDF files
            pdf_file = [file for file in files_in_folder if file.endswith('.pdf')][0]
            pdf_path=f"pdfHolder/{pdf_file}"
            

            import re


            def getLines(pdf_path):
                with pdfplumber.open(pdf_path) as pdf:
                # Iterate through pages
                    for page in pdf.pages:
                        text = page.extract_text()
                        lines = text.split('\n')
                        return lines
                    # print(lines)
            lines = getLines(pdf_path)
            output=None
            current_usage = 0.1
            for i in range(0, len(lines)):
                if lines[i] == "Current Bill Detail Usage/Unit AMOUNT" and lines[i+1] == "Current":
                    splitline = lines[i+3].split()
                    current_usage = float(splitline[4].strip())
            os.remove(pdf_path)
            print(current_usage)
            data.at[houseNumber,'usage_invoice'] = 0.001
            data.at[houseNumber,'usage_invoice'] = float(current_usage)
            print("inputted",data.iloc[houseNumber]['usage_invoice'])
            data.to_csv('walthamInvoice.csv')
            with open("progress.txt", "a") as file:
                file.write(f"{houseNumber}, {data.iloc[houseNumber]['Location']}, {current_usage}\n")
        except Exception as e:
            print("downloaded")
            data.to_csv('walthamInvoice.csv')
            print(e)
            human_delay()
            traceback.print_exc()
            try:
                print("removed unneeded files")
                pdf_file = [file for file in files_in_folder if file.endswith('.pdf')][0]
                pdf_path=f"pdfHolder/{pdf_file}"
                os.remove(pdf_path)
            except:
               aa = 1 


    #objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_1


    
    
