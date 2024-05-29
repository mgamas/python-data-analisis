import pandas as pd

# Load the provided Excel file
file_path = '/mnt/data/ScanCarrefour5-29-2024Analisis.xlsx'
excel_data = pd.ExcelFile(file_path)

# Display sheet names to understand the structure of the file
sheet_names = excel_data.sheet_names
sheet_names


# Load the data from the specified sheet
sheet_name = '29-05-24 scan data'
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Display the first few rows to understand the structure of the data
data.head()


# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Sort the data by 'Date'
data = data.sort_values(by='Date')

# Initialize variables to track cycles and fixtures
cycle_num = 1
previous_time = data['Date'].iloc[0]
cycle_info = []

# Iterate through the data to determine cycles and count fixtures per cycle
for i, row in data.iterrows():
    current_time = row['Date']
    time_diff = (current_time - previous_time).total_seconds() / 60.0  # difference in minutes
    
    if time_diff > 40:
        cycle_num += 1
    
    fixture = row['Fixture']
    cycle_info.append({'Cycle': cycle_num, 'Fixture': fixture, 'Command': row['Command']})
    
    previous_time = current_time

# Create a DataFrame from the cycle information
cycle_df = pd.DataFrame(cycle_info)

# Group by cycle and fixture to count the number of commands
result = cycle_df.groupby(['Cycle', 'Fixture']).size().reset_index(name='Command Count')

# Filter the result to include only fixtures with command count between 11 and 22
filtered_result = result[(result['Command Count'] >= 11) & (result['Command Count'] <= 22)]

import ace_tools as tools; tools.display_dataframe_to_user(name="Cycle Fixture Command Count", dataframe=filtered_result)

filtered_result
