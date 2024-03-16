import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Replace 'YOUR_API_KEY' with your actual News API key
api_key = os.getenv('API_KEY')
url = f'https://newsapi.org/v2/sources?apiKey={api_key}' 

response = requests.get(url)
data = response.json()

import pandas as pd

sources_data = data['sources']

# Convert the list of dictionaries into a DataFrame
sources_df = pd.DataFrame(sources_data)

# Display the DataFrame to check
print(sources_df)

new_csv_filename = f'./data/news_sources_main.csv'
sources_df.to_csv(new_csv_filename, index=False)