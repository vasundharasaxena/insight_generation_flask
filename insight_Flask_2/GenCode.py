import pandas as pd
import numpy as np

csv_file_path = 'Retail.csv'
df = pd.read_csv(csv_file_path)

for column in df.columns:
    if df[column].dtype == 'object':
        df[column] = df[column].apply(lambda x: x.strip() if isinstance(x, str) else x)

if 'DateKey' in df.columns:
    df['DateKey'] = pd.to_datetime(df['DateKey'], errors='coerce')

# Query: monthwise sales trend
import pandas as pd

# Assuming the DataFrame 'df' is already loaded
df['DateKey'] = pd.to_datetime(df['DateKey'])

# Extract year and month
df['Year'] = df['DateKey'].dt.year
df['Month'] = df['DateKey'].dt.month

# Group by Year and Month and calculate the sum of SalesAmount
result = df.groupby(['Year', 'Month'])['SalesAmount'].sum().reset_index()

# If needed, add relevant information columns back to the result
# For here we're focusing on year, month, and sales amount as the primary insights

# Save result to a temporary CSV file
result.to_csv('result.csv', index=False)
