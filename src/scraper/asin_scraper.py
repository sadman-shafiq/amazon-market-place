from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import pandas as pd
import csv
import os

df = pd.read_excel("../../data/input/SearchKeywordLists.xlsx")

with open("../../data/output/products.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["keyword", "asin"])

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

    products = driver.find_elements(By.CSS_SELECTOR, 'div[data-asin]')
    with open("../../data/output/products.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        for product in products:
                asin = product.get_attribute("data-asin")
                print(asin)
                writer.writerow([keyword, asin])

    time.sleep(5)




driver.quit()