import csv
import json
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time
from logger import log_request_result



def get_text_from_element(element):

    text = element.get_attribute("textContent")
    return text.strip()


def get_reviews(driver):
    reviews = []
    for review_element in driver.find_elements(By.CSS_SELECTOR, "#reviewsMedley div[data-hook='review']"):
        review_title = get_text_from_element(review_element.find_element(By.CSS_SELECTOR, "a[data-hook='review-title']"))
        review_rating = get_text_from_element(review_element.find_element(By.CSS_SELECTOR, "i[data-hook='review-star-rating'] span"))
        review_rating = review_rating.replace(" out of 5 stars", "")
        review_text = get_text_from_element(review_element.find_element(By.CSS_SELECTOR, "span[data-hook='review-body'] span"))
        reviews.append({
            "title": review_title,
            "rating": review_rating,
            "text": review_text
        })
    return reviews

def scrape_image_url(driver):
    try:
        image_element = driver.find_element(By.ID, "landingImage")
        image_url = image_element.get_attribute("src")
        return image_url
    except NoSuchElementException:
        return ""
def scrape_columns(driver, by, selector):

    try:
        res = driver.find_element(by, selector)
        return res.text.strip()
    except NoSuchElementException:
        return ""


def scrape_individual_product(driver, asin):
    url = "https://www.amazon.com/dp/" + asin
    driver.get(url)

    title = scrape_columns(driver, By.ID, "productTitle")
    brand = scrape_columns(driver, By.ID, "bylineInfo")
    rating = scrape_columns(driver, By.CSS_SELECTOR, "span[data-hook='rating-out-of-text']")
    rating = rating.replace(" out of 5", "")

    review_count = scrape_columns(driver, By.ID, "acrCustomerReviewText")
    image_url = scrape_image_url(driver)
    description = scrape_columns(driver, By.CSS_SELECTOR, "#feature-bullets li span.a-list-item")
    category = ""
    for category_element in driver.find_elements(By.CSS_SELECTOR, "#wayfinding-breadcrumbs_feature_div ul li a"):
        category_text = get_text_from_element(category_element)
        category = category + "," + category_text

    if category:
        category = category[1:]

    reviews = get_reviews(driver)

    #log_request_result(url, title, brand, rating, review_count, image_url, description)


   

    print(f"ASIN: {asin}")
    print(f"Title: {title}")    
    print(f"Brand: {brand}")
    print(f"Rating: {rating}")
    print(f"Review Count: {review_count}")
    print(f"Image URL: {image_url}")
    print(f"Description: {description}")
    print(f"Category: {category}")



def main():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    #driver.get("https://www.amazon.com")
    dataframe = pd.read_csv("../../data/output/products.csv")
    asins = dataframe["asin"].dropna().tolist()
    #print(asins)
    already_scraped_asins = set()

    for asin in asins:
        if asin in already_scraped_asins:
            continue
        scrape_individual_product(driver, asin)
        already_scraped_asins.add(asin)


        time.sleep(3)



    



if __name__ == "__main__":
    main()