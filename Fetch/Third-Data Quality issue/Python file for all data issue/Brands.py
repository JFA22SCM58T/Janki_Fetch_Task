import pandas as pd
import matplotlib.pyplot as plt
import seaborn as s
import numpy as np
import json

users = pd.read_json('C:\\Users\\thaka\\OneDrive\\Desktop\\Fetch\\Dataset\\brands.json', lines=True)
users.info()
null_counts = users.isnull().sum()
print(null_counts)
percentage_null_values = users.isnull().mean()

for key, value in percentage_null_values.items():
    if value > 0:
        print(key, ":", value * 100)

# Specify the subset of columns excluding columns containing dictionaries
subset_columns = [col for col in users.columns if not isinstance(users[col].iloc[0], dict)]

# # Use the subset_columns for duplicate detection
duplicateRowsDF = users[users.duplicated(subset=subset_columns, keep=False)]
print("Duplicate Rows except first occurrence based on selected columns are:")
print(duplicateRowsDF)
unique_categories = users["category"].unique()
print(unique_categories)

# Calculate the frequencies of each category
# Calculate the frequencies of each category
freq_category = 100 * (users['category'].value_counts() / len(users))

# Format the frequencies as percentages with two decimal places
formatted_freq = freq_category.map('{:,.2f}%'.format)

# Print the formatted frequencies
print(formatted_freq)
