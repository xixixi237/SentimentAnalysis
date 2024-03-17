from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
search_term = 'Traitor BBC'

# Load your API key from an environment variable or directly insert it
DEVELOPER_KEY = os.getenv('DEVELOPER_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Initialize the YouTube API client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def get_top_comments(video_id, max_results=50):
    comments = []
    try:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=max_results,
            order='relevance',  # Assuming 'relevance' might favor comments with more likes
            textFormat='plainText'
        ).execute()

        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
    except Exception as e:
        print(f"Error fetching comments for video {video_id}: {e}")
    return comments

def append_comments_to_df(df):
    df['Comments'] = df['ID'].apply(get_top_comments)
    return df

# Load existing DataFrame
df_videos = pd.read_csv(f'./data/raw/youtube_{search_term}_results.csv')  # path to CSV file

# Append comments to DataFrame
df_videos_with_comments = append_comments_to_df(df_videos)

# Save to a new CSV
df_videos_with_comments.to_csv(f'./data/raw/Youtube/youtube_{search_term}_results_with_comments.csv', index=False)

print("Top comments added and data saved.")
