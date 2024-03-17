import praw
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv('client_id'),
    client_secret = os.getenv('client_secret'),
    user_agent = os.getenv('user_agent'),
)

# Define the search term
search_term = 'Gaza'

# Search the search_term subreddit or use 'all' for all of Reddit
subreddit = reddit.subreddit('all')

# Search for the term and get the top 10 results
search_results = subreddit.search(search_term, limit=90)

# List for posts
posts_data = []

# Extract information from search results
for post in search_results:
    posts_data.append({
        "Title": post.title,
        "ID": post.id,
        "Author": str(post.author),
        "URL": post.url,
        "Score": post.score,
        "Created": post.created_utc,
        "Subreddit": str(post.subreddit),
        "Subreddit_Size": post.subreddit.subscribers
    })

# Convert to pandas DataFrame
posts_df = pd.DataFrame(posts_data)

# Save the DataFrame to a CSV file
csv_filename = f'./data/raw/reddit_{search_term}_results.csv'
posts_df.to_csv(csv_filename, index=False)


# Notify
print(f"Data saved to {csv_filename}.")