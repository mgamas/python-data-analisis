import pandas as pd

# Load the Excel file
file_path = '/mnt/data/ScanCarrefour5-28-2024Analsis.xlsx'
excel_data = pd.ExcelFile(file_path)

# Check sheet names to understand the structure of the file
sheet_names = excel_data.sheet_names
sheet_names

# Load the data from the sheet
sheet_name = '27-05-24 scan data'
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Display the first few rows of the dataframe to understand its structure
data.head()

# Ensure the 'Date' column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Sort the data by 'Date'
data = data.sort_values(by='Date')

# Calculate the time difference between consecutive records
data['Time_Diff'] = data['Date'].diff().dt.total_seconds() / 60.0  # Convert to minutes

# Identify cycles where the time difference is greater than 40 minutes
data['Cycle'] = (data['Time_Diff'] > 40).cumsum()

# Filter cycles where fixture has 33 commands
fixture_commands_count = data.groupby(['Cycle', 'Fixture']).size().reset_index(name='Command_Count')
target_fixtures = fixture_commands_count[fixture_commands_count['Command_Count'] == 33]

# Merge to get the full cycle details
result = data.merge(target_fixtures[['Cycle', 'Fixture']], on=['Cycle', 'Fixture'])

# Create the final summary table
summary_table = result.groupby(['Cycle', 'Fixture']).size().reset_index(name='Command_Count')

import ace_tools as tools; tools.display_dataframe_to_user(name="Cycle and Command Summary Table", dataframe=summary_table)

summary_table
