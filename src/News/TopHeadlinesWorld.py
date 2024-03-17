import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()



# Replace 'YOUR_API_KEY' with your actual News API key
api_key = os.getenv('NEWS_API_KEY')
countrycode = ''
search_term = 'Bitcoin'
url = f'https://newsapi.org/v2/top-headlines?country={countrycode}&q={search_term}&apiKey={api_key}'

# Call API
response = requests.get(url)
data = response.json()


# Extracting the articles
articles = data['articles']

# Normalizing the data and converting it into a DataFrame
df = pd.json_normalize(articles)

# Keeping only the columns of interest
df = df[['title', 'author', 'source.name', 'publishedAt', 'url']]

# Renaming the columns
df.rename(columns={'source.name': 'Source Name', 'publishedAt': 'Published At'}, inplace=True)

# Display the DataFrame
print(df)

new_csv_filename = f'./data/raw/news_top_{countrycode}_{search_term}.csv'
df.to_csv(new_csv_filename, index=False)