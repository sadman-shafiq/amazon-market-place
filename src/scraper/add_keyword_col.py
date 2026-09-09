import pandas as pd

products = pd.read_csv("products.csv")
details = pd.read_csv("product_details.csv")

details["asin"] = details["URL"].str[-10:]

details["keyword"] = details["asin"].map(products.set_index("asin")["keyword"])

details.to_csv("2_product_details.csv", index=False)

print("successful")