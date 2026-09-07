import pandas as pd

file_path = "../../data/output/product_details.csv"

df = pd.read_csv(file_path)

df.dropna(inplace=True)


df.to_csv(file_path, index=False)

