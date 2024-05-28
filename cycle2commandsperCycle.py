import pandas as pd

# Load the Excel file
file_path = '/mnt/data/ScanCarrefour5-28-2024Analsis.xlsx'
excel_data = pd.ExcelFile(file_path)

# Display sheet names to understand the structure of the file
sheet_names = excel_data.sheet_names
sheet_names

# Load the data from the first sheet
sheet_name = '27-05-24 scan data'
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Display the first few rows of the dataframe to understand its structure
data.head()

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Calculate the time difference between consecutive records
data['Time_Diff'] = data['Date'].diff().dt.total_seconds()

# Define cycles where the difference between consecutive records is greater than 40 minutes (2400 seconds)
data['Cycle'] = (data['Time_Diff'] > 2400).cumsum()

# Filter records to include only fixtures with commands between 22 and 32
fixture_command_counts = data.groupby('Fixture')['Command'].transform('count')
filtered_data = data[(fixture_command_counts >= 22) & (fixture_command_counts <= 32)]

# Group by cycle and fixture to get the count of commands
result = filtered_data.groupby(['Cycle', 'Fixture']).size().reset_index(name='Command_Count')

import ace_tools as tools; tools.display_dataframe_to_user(name="Cycle, Fixture and Command Count Table", dataframe=result)

result
