import pandas as pd

# Load the uploaded Excel file
file_path = '/mnt/data/ScanCarrefour5-29-2024Analisis.xlsx'
df = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
df.head()

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Sort the dataframe by 'Date'
df = df.sort_values(by='Date')

# Identify the cycles
df['Time_Diff'] = df['Date'].diff().dt.total_seconds().div(60)  # Time difference in minutes
df['Cycle'] = (df['Time_Diff'] > 40).cumsum()

# Filter fixtures with 33 commands per cycle
fixture_command_counts = df.groupby(['Cycle', 'Fixture']).size().reset_index(name='Command_Count')
desired_fixtures = fixture_command_counts[fixture_command_counts['Command_Count'] == 33]

# Display the result to the user
import ace_tools as tools; tools.display_dataframe_to_user(name="Desired Fixtures by Cycle and Command Count", dataframe=desired_fixtures)
