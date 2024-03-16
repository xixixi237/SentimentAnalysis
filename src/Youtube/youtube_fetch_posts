from googleapiclient.discovery import build
import pandas as pd
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

DEVELOPER_KEY = os.getenv('DEVELOPER_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

##########################
search_term = 'Rishi Sunak'
##########################


# Initialize
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def search_videos(search_term):
    search_response = youtube.search().list(
        q=search_term,
        part='snippet',
        maxResults=50,
        order='relevance',
        type='video',
    ).execute()
    
    videos = []
    for search_result in search_response.get('items', []):
        videos.append(search_result['id']['videoId'])
    return videos

def get_videos_details(video_ids):
    videos_response = youtube.videos().list(
        id=','.join(video_ids),
        part='snippet,statistics'
    ).execute()
    
    video_details = []
    for video in videos_response.get('items', []):
        video_details.append({
            'ID': video['id'],
            'Title': video['snippet']['title'],
            'Author': video['snippet']['channelTitle'],
            'Date Uploaded': video['snippet']['publishedAt'],
            'Views': video['statistics'].get('viewCount', 'N/A'),
            'Likes': video['statistics'].get('likeCount', 'N/A'),
            'Channel ID': video['snippet']['channelId']
        })
    return video_details

def get_channel_subscriber_count(channel_ids):
    channels_response = youtube.channels().list(
        id=','.join(channel_ids),
        part='statistics'
    ).execute()
    
    channel_details = {channel['id']: channel['statistics'].get('subscriberCount', 'N/A') 
                       for channel in channels_response.get('items', [])}
    return channel_details

def search_and_compile_video_data(search_term):
    video_ids = search_videos(search_term)
    if not video_ids:
        return pd.DataFrame()  # Return an empty DataFrame if no videos found
    
    video_details = get_videos_details(video_ids)
    channel_ids = list({video['Channel ID'] for video in video_details})
    channel_subscriber_count = get_channel_subscriber_count(channel_ids)
    
    for video in video_details:
        video['Subscriber Count'] = channel_subscriber_count.get(video['Channel ID'], 'N/A')
        del video['Channel ID']  # Remove Channel ID if not needed in the final DataFrame
    
    return pd.DataFrame(video_details)


df_videos = search_and_compile_video_data(search_term)

csv_filename = f'./data/raw/youtube_{search_term}_results.csv'
df_videos.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}.")