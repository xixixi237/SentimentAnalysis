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

search_term = 'Gaza'

# Load the CSV file containing post IDs
df = pd.read_csv(f'./data/raw/reddit_{search_term}_results.csv')

# Fetch top 3 comments for a given post ID
def fetch_top_comments(post_id):
    post = reddit.submission(id=post_id)
    post.comment_sort = 'best'
    post.comments.replace_more(limit=0)  # only get actual comments, no "more comments" links
    top_comments = [comment.body for comment in post.comments.list()[:3]]
    return top_comments

# Add a column for top comments to the dataframe
df['Top_Comments'] = df['ID'].apply(lambda x: fetch_top_comments(x))

# Optionally, save this enhanced dataframe back to a new CSV
df.to_csv(f'./data/raw/reddit_{search_term}_results_with_comments.csv', index=False)

print("Top comments added and data saved.")
