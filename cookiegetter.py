import selenium
from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import json
import re
import os
import time

load_dotenv()

f = open("geckodriver.log", "w")
f.write("")
f.close()

opt = webdriver.FirefoxOptions()
opt.add_argument("--headless")
opt.add_argument("--ignore-certificate-errors")
opt.add_argument("--test-type")
opt.add_argument("--disable-gpu")

fp = webdriver.FirefoxProfile(os.environ.get("firefox-profile"))
driver = webdriver.Firefox(fp, options=opt)
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

passfield = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.ID, "i0118")))
passfield.send_keys(os.environ.get("password"))

confirmbut = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, "idSIButton9")))
confirmbut.click()

sendbut = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "id__9")))
time.sleep(3.5)
sendbut.click()

field = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "input.ms-BasePicker-input")))

field.send_keys("100")

try:
    dirsearch = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "sug-footer-item1")))
    dirsearch.click()
except:
    pass

for request in driver.requests[::-1]:
    if "suggestions?scenario=owa.react.compose" in request.url:

        cvid = json.loads(request.body.decode("utf-8"))["Cvid"]
        print(cvid)
        os.system(f"dotenv set Cvid {cvid}")
        os.system(f"dotenv set url \"{request.url}\"")

        for header in request.headers:
            print(header)

            if header in ["client-request-id", "authorization", "x-owa-canary", "x-anchormailbox", "client-session-id", "x-owa-sessionid", "ms-cv"]:
                if header == "authorization":
                    os.system(f'dotenv set {header} "Bearer  {request.headers[header].split()[1]}"')
                else:
                    os.system(f"dotenv set {header} \"{request.headers[header]}\"")
        break

driver.close()
