import pandas as pd

# Load the uploaded Excel file
file_path = '/mnt/data/ScanCarrefour5-29-2024Analisis.xlsx'
excel_data = pd.ExcelFile(file_path)

# Display sheet names to understand the structure of the file
excel_data.sheet_names

# Load the data from the sheet
df = pd.read_excel(file_path, sheet_name='29-05-24 scan data')

# Display the first few rows of the dataframe to understand its structure
df.head()

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Sort the dataframe by Date
df = df.sort_values(by='Date')

# Calculate the time difference between consecutive records
df['Time_Diff'] = df['Date'].diff().dt.total_seconds() / 60.0

# Identify the cycles based on the time difference
df['Cycle'] = (df['Time_Diff'] > 40).cumsum()

# Group by Cycle and Fixture, and count the number of commands in each group
result = df.groupby(['Cycle', 'Fixture']).size().reset_index(name='Command_Count')

# Filter the results to only include fixtures with command counts between 22 and 32
filtered_result = result[(result['Command_Count'] >= 22) & (result['Command_Count'] <= 32)]

import ace_tools as tools; tools.display_dataframe_to_user(name="Filtered Cycle Fixture Command Counts", dataframe=filtered_result)

filtered_result
