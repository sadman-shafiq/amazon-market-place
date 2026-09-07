import pandas as pd
import requests

df = pd.read_csv("../../data/output/product_details.csv")


for index, row in df.iterrows():

    asin = row["URL"][-10:]
    image_url = row["Image_URL"]

    response = requests.get(image_url)

    if response.status_code == 200:
        filename = f"../../data/images/{asin}.jpg"

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"Downloaded {filename}")