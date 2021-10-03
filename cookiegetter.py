import selenium
from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time

load_dotenv()

driver = webdriver.Firefox()
driver.get("https://outlook.office.com/")

def get_element(by_type, flag):
    try:
        return WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((by_type, flag)))
    except:
        raise
   
emailfield = get_element(By.ID, "i0116")
emailfield.send_keys(os.environ.get("email"))
emailfield.send_keys(Keys.RETURN)

passfield = get_element(By.ID, "i0118")
passfield.send_keys(os.environ.get("password"))

confirmbut = WebDriverWait(driver, 20).until(
EC.element_to_be_clickable((By.ID, "idSIButton9")))
confirmbut.click()

input()
