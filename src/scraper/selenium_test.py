from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import pandas as pd


df = pd.read_excel("../../data/input/SearchKeywordLists.xlsx")

#print(df)

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.amazon.com")

time.sleep(3)

for keyword in df["Search Keywords"]:
    print(keyword)
    input_element = driver.find_element(By.ID, "twotabsearchtextbox")
    input_element.clear()
    input_element.send_keys(keyword + Keys.ENTER)
    time.sleep(5)








driver.quit()