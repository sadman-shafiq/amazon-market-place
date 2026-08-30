import csv
from datetime import datetime
import os

def log_request_result(url):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("../../logs/request_log.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, url])