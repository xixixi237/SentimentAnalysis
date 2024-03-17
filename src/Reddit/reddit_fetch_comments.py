import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Search term
search_term = 'Labour'

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

# New structure to store post data and concatenated comments
posts_comments_data = {}

df = pd.read_csv(f'./data/raw/Reddit/reddit_{search_term}_posts.csv')

# Loop through each post ID to fetch top comments
for index, row in df.iterrows():
    post_id = row['ID']
    response = requests.get(f'https://oauth.reddit.com/comments/{post_id}?sort=top&limit=50',
                            headers=headers)
    comments = response.json()

    # Initialize an empty string to store concatenated comments for the current post
    concatenated_comments = ''
    
    # Extract top comments
    for comment in comments[1]['data']['children']:
        comment_data = comment['data']
        # Concatenate comment body to the string, followed by optional separator (e.g., "/")
        concatenated_comments += comment_data.get('body', 'N/A') + " "
    
    # Store post data and concatenated comments in the dictionary
    posts_comments_data[post_id] = [
        row['Title'], post_id, row['Author'], row['URL'], row['Upvotes'],
        row['Date'], row['Subreddit'], row['Subreddit_Size'],
        concatenated_comments
    ]

# Convert the dictionary to a DataFrame
columns = ['Title', 'Post_ID', 'Post_Author', 'URL', 'Post_Upvotes', 'Post_Date', 
           'Subreddit', 'Subreddit_Size', 'Top_Comments']
comments_df = pd.DataFrame.from_dict(posts_comments_data, orient='index', columns=columns)

# Save the comments DataFrame to a new CSV
new_csv_filename = f'./data/raw/Reddit/reddit_{search_term}_posts_comments.csv'
comments_df.to_csv(new_csv_filename, index=False)

print(f"Expanded data saved to {new_csv_filename}.")
