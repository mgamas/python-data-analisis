# Filter fixtures that have exactly 33 commands per hour
fixtures_with_33_commands = fixture_counts[fixture_counts['Count'] == 33]

# Display the dataframe
tools.display_dataframe_to_user(name="Fixtures with 33 Commands per Hour", dataframe=fixtures_with_33_commands)

fixtures_with_33_commands
