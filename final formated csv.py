import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('combined_file.csv')

# Filter for only 'pink morsel' products
df_pink = df[df['product'] == 'pink morsel'].copy()

# Clean and convert price (remove $ and convert to float)
df_pink['price'] = df_pink['price'].str.replace('$', '').astype(float)

# Calculate sales = quantity * price
df_pink['Sales'] = df_pink['quantity'] * df_pink['price']

# Select and rename required columns
output_df = df_pink[['Sales', 'date', 'region', 'product']].copy()
output_df = output_df.rename(columns={'date': 'Date', 'region': 'Region'})

# Save the formatted output file to output directory
output_df.to_csv('soul_foods_pink_morsels.csv', index=False)
print("Formatted output file 'soul_foods_pink_morsels.csv' created successfully!")
print(f"Shape: {output_df.shape}")
print("\nFirst few rows:")
print(output_df.head())