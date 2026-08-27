from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.amazon.com")

time.sleep(3)

input_element = driver.find_element(By.ID, "twotabsearchtextbox")
input_element.send_keys("wireless earbuds" + Keys.ENTER)

time.sleep(10)




driver.quit()