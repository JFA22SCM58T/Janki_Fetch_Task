import pandas as pd
import matplotlib.pyplot as plt
import seaborn as s
import numpy as np
import json

users = pd.read_json('C:\\Users\\thaka\\OneDrive\\Desktop\\Fetch\\Dataset\\users.json', lines=True)
users.info()
# make lists of variable types
# Define variables to categorize columns

# Convert lastLoginDate column to string type
users["lastLogin"] = users["lastLogin"].astype(str)

# # Display the first few rows of the DataFrame
users.head()

temporal = [var for var in users.columns if 'date' in var.lower() or 'date' in var.lower()]
discrete = [var for var in users.columns if users[var].dtype != 'O' and len(users[var].unique()) < 20 and var not in temporal]
continuous = [var for var in users.columns if users[var].dtype != 'O' and var not in discrete and var != '_id' and var not in temporal]
categorical = [var for var in users.columns if users[var].dtype == 'O' and var not in temporal and var not in discrete]

# Print the number of variables in each category
print(f'There are {len(continuous)} continuous variables')
print(f'There are {len(discrete)} discrete variables')
print(f'There are {len(temporal)} temporal variables')
print(f'There are {len(categorical)} categorical variables')

print(discrete)
print(temporal)
print(categorical)

# Check for missing values in the DataFrame
missing_values = users.isnull().sum()

# # Display the number of missing values for each column
print("Missing Values:")
print(missing_values)
# Calculate the percentage of missing values for each variable
percentage_null_values = users.isnull().mean()

# # Print the percentage of missing values for variables with missing values
for key, value in percentage_null_values.items():
    if value > 0:
        print(key, ":", value * 100)

# Identify duplicate rows in the DataFrame
users_no_dicts = users.select_dtypes(exclude=['object'])

# # Identify duplicate rows in the DataFrame
duplicateRowsDF = users_no_dicts[users_no_dicts.duplicated()]

# # Print duplicate rows except the first occurrence based on all columns
print("Duplicate Rows except first occurrence based on all columns are:")
print(duplicateRowsDF)

# Retrieve the unique values from the "signUpSource" column
unique_signUpSource = users["signUpSource"].unique()

# # Print the unique values for "signUpSource"
print("Unique values in the 'signUpSource' column:")
print(unique_signUpSource)

# # Retrieve the unique values from the "state" column
unique_state = users["state"].unique()

# # Print the unique values for "state"
print("\nUnique values in the 'state' column:")
print(unique_state)

# Calculate the frequency of each unique value in the "signUpSource" column as a percentage
freq_source = 100 * (users['signUpSource'].value_counts() / len(users))

# Format the percentages for "signUpSource"
formatted_freq_source = freq_source.map('{:,.2f}%'.format)

# Print the formatted percentages for "signUpSource"
print("Frequency of each unique value in the 'signUpSource' column:")
print(formatted_freq_source)

# Calculate the frequency of each unique value in the "state" column as a percentage
freq_state = 100 * (users['state'].value_counts() / len(users))

# Format the percentages for "state"
formatted_freq_state = freq_state.map('{:,.2f}%'.format)

# Print the formatted percentages for "state"
print("\nFrequency of each unique value in the 'state' column:")
print(formatted_freq_state)
