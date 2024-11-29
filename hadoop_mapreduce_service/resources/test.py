import pandas as pd
import re

# Load the CSV file into a pandas DataFrame
# Replace 'your_file.csv' with your actual file path
df = pd.read_csv('nbadatasettest.csv')

# Define a function to extract the score from the 'description' column
def extract_score(description):
    match = re.search(r'\((\d+) PTS\)', description)
    if match:
        return int(match.group(1))
    return 0  # Return 0 if no score is found

df['HOMEDESCRIPTION'] = df['HOMEDESCRIPTION'].astype(str)

# Apply the function to extract scores
df['score'] = df['HOMEDESCRIPTION'].apply(extract_score)

# Select and reorder the desired columns
output_df = df[['PLAYER1_NAME', 'GAME_ID', 'score']]

max_scores = df.groupby(['PLAYER1_NAME', 'GAME_ID'])['score'].max().reset_index()

# Display the resulting DataFrame
# print(output_df.head())
final = max_scores.groupby('PLAYER1_NAME')['score'].sum().reset_index()

print(final.sort_values(by='score'))

