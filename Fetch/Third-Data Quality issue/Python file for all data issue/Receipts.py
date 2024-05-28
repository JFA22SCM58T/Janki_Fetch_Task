import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json

receipts = pd.read_json('C:\\Users\\thaka\\OneDrive\\Desktop\\Fetch\\Dataset\\receipts.json', lines=True)
# users.info()
import pandas as pd

def get_temporal_vars(dataframe):
    return [var for var in dataframe.columns if 'date' in var.lower() or 'date' in var.lower()]

def get_discrete_vars(dataframe, temporal_vars):
    return [var for var in dataframe.columns if dataframe[var].dtype != 'O' and len(dataframe[var].unique()) < 20 and var not in temporal_vars]

def get_continuous_vars(dataframe, temporal_vars, discrete_vars):
    return [var for var in dataframe.columns if dataframe[var].dtype != 'O' and var not in discrete_vars and var != '_id' and var not in temporal_vars]

def get_categorical_vars(dataframe, temporal_vars, discrete_vars):
    return [var for var in dataframe.columns if dataframe[var].dtype == 'O' and var not in temporal_vars and var not in discrete_vars]

# Assuming you have already loaded your data into the receipts DataFrame

temporal_vars = get_temporal_vars(receipts)
discrete_vars = get_discrete_vars(receipts, temporal_vars)
continuous_vars = get_continuous_vars(receipts, temporal_vars, discrete_vars)
categorical_vars = get_categorical_vars(receipts, temporal_vars, discrete_vars)

# print(f'There are {len(continuous_vars)} continuous variables')
# print(f'There are {len(discrete_vars)} discrete variables')
# print(f'There are {len(temporal_vars)} temporal variables')
# print(f'There are {len(categorical_vars)} categorical variables')

# print(continuous_vars)

# print(discrete_vars)

# print(temporal_vars)

# print(categorical_vars)

# null_counts = receipts.isnull().sum()
# print(null_counts)

# Calculate the percentage of null values for each column
# percentage_null_values = receipts.isnull().mean()

# # Iterate through the dictionary of column names and their corresponding null percentages
# for key, value in percentage_null_values.items():
#     # Check if the null percentage is greater than 0
#     if value > 0:
#         # Print the column name and its null percentage
#         print(key, ":", value * 100)
# unique_points_earned = receipts["pointsEarned"].unique()
# print(unique_points_earned)

# Check for duplicates based on all columns except "_id/$oid"
# subset_columns = [col for col in receipts.columns if receipts[col].dtype != 'O']

# # Check for duplicates based on the subset of columns
# duplicateRowsDF = receipts[receipts.duplicated(subset=subset_columns, keep=False)]
# print("Duplicate Rows except first occurrence based on selected columns are:")
# print(duplicateRowsDF)
# Calculate the frequency of reasons and convert to percentages
# freq_reasons = 100 * (receipts['bonusPointsEarnedReason'].value_counts() / len(receipts))

# # Print the percentages formatted to two decimal places
# print(freq_reasons.map('{:,.2f}%'.format))

# fig, axs = plt.subplots(ncols=3, nrows=1, figsize=(15, 5))

# # Flatten the axs array for easier iteration
# axs = axs.flatten()
# Define temporal variables
temporal = [
    var for var in receipts.columns
    if 'date' in var.lower() or 'time' in var.lower()
]

# Define discrete variables
discrete = [
    var for var in receipts.columns
    if receipts[var].dtype != 'O' and len(receipts[var].unique()) < 20
]

# Define categorical variables
categorical = [
    var for var in receipts.columns
    if receipts[var].dtype == 'O' and var not in temporal and var not in discrete
]

# Define the list of continuous variables
continuous = [
    var for var in receipts.columns
    if var not in temporal + discrete + categorical
]

# Iterate through each continuous variable
# for i, var in enumerate(continuous):
#     # Filter out non-null values for the variable and create a boxplot
#     sns.boxplot(receipts[var].dropna(), ax=axs[i], orient='h')

# # # Show the plot
# # plt.show()
# fig, axs = plt.subplots(ncols=3, nrows=1, figsize=(15, 5))

# # Flatten the axs array for easier iteration
# axs = axs.flatten()

# # Iterate through each continuous variable
# for i, var in enumerate(continuous):
#     # Filter out non-null values for the variable and create a distribution plot
#     sns.distplot(receipts[var].dropna(), ax=axs[i])

# # Show the plot
# plt.show()
# Create subplots
# Drop non-numeric columns
numeric_columns = receipts.select_dtypes(include=np.number).columns
receipts_numeric = receipts[numeric_columns]

# Create subplots
f, ax = plt.subplots(figsize=(10, 10))

# Calculate the correlation matrix
corr = receipts_numeric.corr()

# Create heatmap
sns.heatmap(
    corr,
    mask=np.zeros_like(corr, dtype=bool),  # Change np.bool to bool
    square=True,
    ax=ax
)

# Show the plot
plt.show()