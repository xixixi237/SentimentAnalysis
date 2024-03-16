import requests
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
user_agent = os.getenv('user_agent')

# Obtain an access token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
data = {'grant_type': 'client_credentials'}
headers = {'User-Agent': user_agent}
response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
access_token = response.json().get('access_token')

# Use the access token to access the Reddit API
headers = {
    'Authorization': f'bearer {access_token}',
    'User-Agent': user_agent
}
username = ''  # The user's username you want to fetch posts for
response = requests.get(f'https://oauth.reddit.com/user/{username}/comments?&limit=100', headers=headers)

# Process the response
reddit_response = response.json()  # This is the correct variable containing the response data

# Ensure the correct path is used to access the comments data
comments = [item["data"] for item in reddit_response["data"]["children"]]

# Create a DataFrame
df = pd.DataFrame(comments, columns=['author', 'body', 'score', 'subreddit', 'created_utc'])

new_csv_filename = f'./data/raw/users/reddit_{username}_posts.csv'
df.to_csv(new_csv_filename, index=False)

print(f"Expanded data saved to {new_csv_filename}.")
print(df)