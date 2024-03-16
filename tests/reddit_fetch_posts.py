import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()

# Search term and subreddit
search_term = 'Israel'
subreddit = 'News'

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
user_agent = os.getenv('user_agent')

# Authenticate
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
data = {'grant_type': 'password', 'username': os.getenv('user_name'), 'password': os.getenv('password')}
headers = {'User-Agent': user_agent}
response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = response.json()['access_token']

# Setting up the header with our access token
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# Perform a search in the specified subreddit
response = requests.get(f'https://oauth.reddit.com/r/{subreddit}/search?q={search_term}&sort=top&t=week&limit=100',
                        headers=headers)

# Extracting data
posts = response.json()['data']['children']
data = []
for post in posts:
    p = post['data']
    data.append([
        p['title'], p['id'], p['author'], p['url'], p['ups'],
        datetime.fromtimestamp(p['created_utc']), p['subreddit'], p['subreddit_subscribers']
    ])

# Create a pandas DataFrame
columns = ['Title', 'ID', 'Author', 'URL', 'Upvotes', 'Date', 'Subreddit', 'Subreddit_Size']
df = pd.DataFrame(data, columns=columns)
df= df.drop_duplicates(subset=['ID', 'Title'], keep='first') # Removes duplicate posts


csv_filename = f'./data/raw/reddit_{search_term}_posts.csv'
df.to_csv(csv_filename, index=False)


# Notify
print(f"Data saved to {csv_filename}.")