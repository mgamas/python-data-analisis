import pandas as pd

# Load the uploaded Excel file
file_path = '/mnt/data/ScanCarrefour5-29-2024Analisis.xlsx'
data = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
data.head()

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Sort the data by 'Date' to ensure chronological order
data = data.sort_values(by='Date').reset_index(drop=True)

# Calculate the time difference between consecutive records
data['TimeDiff'] = data['Date'].diff().dt.total_seconds() / 60  # Time difference in minutes

# Identify cycles where the time difference between consecutive records is greater than 40 minutes
cycle_indices = data[data['TimeDiff'] > 40].index.tolist()

# Initialize lists to hold the new table data
horaminima = []
horamaxima = []
tiempotranscurrido = []
comandosEnviados = []

# Process the data to create cycles
previous_index = 0

for index in cycle_indices:
    cycle_data = data.iloc[previous_index:index]
    if not cycle_data.empty:
        horaminima.append(cycle_data['Date'].min())
        horamaxima.append(cycle_data['Date'].max())
        tiempotranscurrido.append((cycle_data['Date'].max() - cycle_data['Date'].min()).total_seconds() / 60)  # Time elapsed in minutes
        comandosEnviados.append(len(cycle_data))
    previous_index = index

# Handle the last cycle after the last identified gap
cycle_data = data.iloc[previous_index:]
if not cycle_data.empty:
    horaminima.append(cycle_data['Date'].min())
    horamaxima.append(cycle_data['Date'].max())
    tiempotranscurrido.append((cycle_data['Date'].max() - cycle_data['Date'].min()).total_seconds() / 60)  # Time elapsed in minutes
    comandosEnviados.append(len(cycle_data))

# Create the new table as a DataFrame
cycles_df = pd.DataFrame({
    'horaminima': horaminima,
    'horamaxima': horamaxima,
    'tiempotranscurrido': tiempotranscurrido,
    'comandosEnviados': comandosEnviados
})

import ace_tools as tools; tools.display_dataframe_to_user(name="Cycles DataFrame", dataframe=cycles_df)

# Display the new cycles DataFrame
cycles_df
