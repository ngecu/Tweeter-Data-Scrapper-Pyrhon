import pandas as pd
import json

# Read the JSON data from the file
with open('tweet_data.json', 'r') as file:
    json_data = json.load(file)

# Convert JSON to DataFrame
df = pd.json_normalize(json_data, 'data', ['keyword'])

# Save DataFrame to Excel file
df.to_excel('data.xlsx', index=False)

print("Data converted to Excel successfully.")
