# Count the number of commands per fixture per hour
fixture_counts = df.groupby(['Hour', 'Fixture']).size().reset_index(name='Count')

# Filter fixtures that exceed 33 commands per hour
exceeding_fixtures = fixture_counts[fixture_counts['Count'] > 33]

# Display the dataframe
tools.display_dataframe_to_user(name="Fixtures Exceeding 33 Commands per Hour", dataframe=exceeding_fixtures)

exceeding_fixtures
