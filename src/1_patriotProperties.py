import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv



# Install the appropriate WebDriver if needed
# Ensure your WebDriver executable is in the system PATH or specify the path to it

driver = webdriver.Chrome()

# Navigate to the desired web page
driver.get('https://arlington.patriotproperties.com/default.asp') #frames: top, middle, bottom

# Function to get HTML from a frame by its name or ID
def get_frame_html(frame_reference):
    driver.switch_to.frame(frame_reference)
    html = driver.execute_script("return document.documentElement.outerHTML;")
    driver.switch_to.default_content()
    return html



# Get the HTML of each frame
driver.switch_to.frame("middle")

driver.find_element(By.ID,"SearchYearBuilt").send_keys("0")
time.sleep(0.5)
driver.find_element(By.ID,"SearchYearBuiltThru").send_keys("3000")
time.sleep(0.5)


driver.find_element(By.ID,"cmdGo").click()
time.sleep(2)
driver.switch_to.default_content()
driver.switch_to.frame("bottom")


table = driver.find_element(By.ID,"T1")


# Initialize a CSV file to write the data
with open('arlingtonPatriot.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    header = [th.text for th in table.find_elements(By.XPATH,".//thead//th")]
    writer.writerow(header)

    # Find all rows in the table body
    for i in range(302):

        table = driver.find_element(By.ID,"T1")
        rows = table.find_elements(By.XPATH,".//tbody//tr")
    
    # Loop through each row
        for row in rows:
        # Extract data from each cell in the row
            data = [td.text for td in row.find_elements(By.XPATH,".//td")]
        # Write the data to CSV file
            writer.writerow(data)
        next=driver.find_element(By.LINK_TEXT,"Next Page").click()
        time.sleep(0.1)
driver.quit()
