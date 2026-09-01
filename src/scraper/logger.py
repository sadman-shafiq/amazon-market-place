import csv
from datetime import datetime

def log_request_result(url, request_status, http_status_code):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    with open("../../logs/request_log.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([ url, timestamp, request_status, http_status_code])     



