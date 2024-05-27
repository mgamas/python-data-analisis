# Create a new dataframe to store the results
time_summary = pd.DataFrame(columns=['Hour', 'HoraMinima', 'HoraMaxima', 'TiempoTranscurrido'])

# Iterate over each hour
for hour in df['Hour'].unique():
    hour_data = df[df['Hour'] == hour]
    hora_minima = hour_data['Date'].min()
    hora_maxima = hour_data['Date'].max()
    tiempo_transcurrido = (hora_maxima - hora_minima).total_seconds()
    
    time_summary = time_summary.append({
        'Hour': hour,
        'HoraMinima': hora_minima,
        'HoraMaxima': hora_maxima,
        'TiempoTranscurrido': tiempo_transcurrido
    }, ignore_index=True)

# Display the dataframe
tools.display_dataframe_to_user(name="Time Summary by Hour", dataframe=time_summary)

time_summary
