import pandas as pd
import numpy as np

csv_file_path = 'Retail.csv'
df = pd.read_csv(csv_file_path)

for column in df.columns:
    if df[column].dtype == 'object':
        df[column] = df[column].apply(lambda x: x.strip() if isinstance(x, str) else x)

if 'DateKey' in df.columns:
    df['DateKey'] = pd.to_datetime(df['DateKey'], errors='coerce')

# Query: how all the brands have contributed towards the sales amount
import pandas as pd

# Assuming df is already loaded
# Ensure that column names match exactly

# Group by 'BrandName' and calculate the sum of 'SalesAmount'
result = df.groupby('BrandName')['SalesAmount'].sum().reset_index()

# To align with the required output format, it should contain the 'BrandName' and 'SalesAmount' columns.
result = pd.DataFrame(result, columns=['BrandName', 'SalesAmount'])

# Save result to a temporary CSV file
result.to_csv('result.csv', index=False)
