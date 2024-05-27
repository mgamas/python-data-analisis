# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Extract the hour from the 'Date' column and create a new column for it
df['Hour'] = df['Date'].dt.hour

# Group by 'Hour' and 'Command' to get the count of each command per hour
summary_table = df.groupby(['Hour', 'Command']).size().reset_index(name='Count')

# Pivot the table to have hours as rows and commands as columns
pivot_table = summary_table.pivot(index='Hour', columns='Command', values='Count').fillna(0).astype(int)

import ace_tools as tools; tools.display_dataframe_to_user(name="Summary of Commands by Hour", dataframe=pivot_table)

pivot_table
