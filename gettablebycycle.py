import pandas as pd

# Load the uploaded Excel file
file_path = '/mnt/data/ScanCarrefour5-28-2024.xlsx'
data = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
data.head()

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Sort data by 'Date'
data = data.sort_values(by='Date').reset_index(drop=True)

# Initialize variables to store cycles
cycles = []
current_cycle = {'horaminima': None, 'horamaxima': None, 'tiempotranscurrido': None, 'comandosEnviados': 0}
last_time = None

# Iterate through the data to create cycles
for index, row in data.iterrows():
    current_time = row['Date']
    if last_time is not None and (current_time - last_time).total_seconds() / 60 > 40:
        current_cycle['horamaxima'] = last_time
        current_cycle['tiempotranscurrido'] = (current_cycle['horamaxima'] - current_cycle['horaminima']).total_seconds() / 60
        cycles.append(current_cycle)
        current_cycle = {'horaminima': current_time, 'horamaxima': None, 'tiempotranscurrido': None, 'comandosEnviados': 1}
    else:
        if current_cycle['horaminima'] is None:
            current_cycle['horaminima'] = current_time
        current_cycle['comandosEnviados'] += 1
    last_time = current_time

# Add the last cycle if it exists
if current_cycle['horaminima'] is not None:
    current_cycle['horamaxima'] = last_time
    current_cycle['tiempotranscurrido'] = (current_cycle['horamaxima'] - current_cycle['horaminima']).total_seconds() / 60
    cycles.append(current_cycle)

# Convert cycles to a DataFrame
cycles_df = pd.DataFrame(cycles)

import ace_tools as tools; tools.display_dataframe_to_user(name="Ciclos de comandos", dataframe=cycles_df)

# Display the cycles DataFrame
cycles_df
