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
        reviewer_name  =  review_element.find_element(By.CSS_SELECTOR, ".a-profile-name").text
        review_title  = review_element.find_element(By.CSS_SELECTOR, "[data-hook='reviewTitle']").text
        review_text  = review_element.find_element(By.CSS_SELECTOR, "[data-hook='reviewRichContentContainer']").text
        review_rating  = review_element.find_element(By.CSS_SELECTOR, "[data-hook='review-star-rating'] .a-icon-alt").text 
        review_rating = review_rating.replace(" out of 5 stars", "")
        #print(f"Reviewer: {reviewer_name}, Title: {review_title}, Text: {review_text}, Rating: {review_rating}")

        reviews.append({
            "reviewer_name": reviewer_name,
            "review_title": review_title,
            "review_text": review_text,
            "review_rating": review_rating
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
        return res.text
    except NoSuchElementException:
        return ""


def scrape_individual_product(driver, asin):
    url = "https://www.amazon.com/dp/" + asin
    driver.get(url)

    title = scrape_columns(driver, By.CSS_SELECTOR, "#productTitle")
    brand = scrape_columns(driver, By.CSS_SELECTOR, "#bylineInfo")
    if not brand:
        brand = scrape_columns(driver, By.CSS_SELECTOR, "#visitStoreDesktopUrl")

    brand = brand.replace("Visit the ", "")
    brand = brand.replace(" Store", "")

    rating = scrape_columns(driver, By.CSS_SELECTOR, "span[data-hook='rating-out-of-text']")
    rating = rating.replace(" out of 5", "")

    review_count = scrape_columns(driver, By.CSS_SELECTOR, "#acrCustomerReviewText")
    image_url = scrape_image_url(driver)
    description = scrape_columns(driver, By.CSS_SELECTOR, "#feature-bullets li span.a-list-item")
    category = ""
    for category_element in driver.find_elements(By.CSS_SELECTOR, "#wayfinding-breadcrumbs_feature_div ul li a"):
        category_text = get_text_from_element(category_element)
        category = category + "," + category_text

    if category:
        category = category[1:]

    reviews = get_reviews(driver)
    with open("../../data/output/product_details.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([asin, title, brand, rating, review_count, image_url, description, category, json.dumps(reviews)])
    if title and brand and rating and review_count and image_url and description and category and reviews:
        log_request_result(url, "Success", 200)
        return True
    else:
        log_request_result(url, "Failed", 404)
        return False




    # print(f"ASIN: {asin}")
    # print(f"Title: {title}")    
    # print(f"Brand: {brand}")
    # print(f"Rating: {rating}")
    # print(f"Review Count: {review_count}")
    # print(f"Image URL: {image_url}")
    # print(f"Description: {description}")
    # print(f"Category: {category}")
    # print(reviews)



def main():
    with open("../../data/output/product_details.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ASIN", "Title", "Brand", "Rating", "Review_Count", "Image_URL", "Description", "Category", "Reviews"])
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
        flag = scrape_individual_product(driver, asin)
        count = 0
        while not flag and count < 3:
            flag = scrape_individual_product(driver, asin)
            count += 1

        already_scraped_asins.add(asin)


        time.sleep(3)



    



if __name__ == "__main__":
    main()