from googleapiclient.discovery import build
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st

# Function to initialize YouTube API client
def initialize_youtube_api():
    load_dotenv()
    DEVELOPER_KEY = os.getenv('DEVELOPER_KEY')
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    print("Youtube API Succesfully Initialised")
    return youtube

# Function to fetch YouTube video details based on search term
def fetch_video_details(youtube, search_term):
    search_response = youtube.search().list(q=search_term, part='snippet', maxResults=50, order='relevance', type='video').execute()
    videos = []
    for item in search_response.get('items', []):
        video_id = item['id']['videoId']
        video_details = youtube.videos().list(id=video_id, part='snippet,statistics').execute().get('items', [])[0]
        channel_id = video_details['snippet']['channelId']
        videos.append({
            'ID': video_id,
            'Title': video_details['snippet']['title'],
            'Author': video_details['snippet']['channelTitle'],
            'Date Uploaded': video_details['snippet']['publishedAt'],
            'Views': video_details['statistics'].get('viewCount', 'N/A'),
            'Likes': video_details['statistics'].get('likeCount', 'N/A'),
            'Channel ID': channel_id
        })
    print(f"{search_term} video details fetched")
    return videos

# Function to fetch comments for each video
def fetch_comments(youtube, video_ids):
    comments = []
    videos_with_disabled_comments =[]
    for video_id in video_ids:
        try:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=50,
                order='relevance',
                textFormat='plainText'
            ).execute()
            for item in response.get('items', []):
                comment_snippet = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'ID': video_id,
                    'Comment': comment_snippet['textDisplay'],
                    'Likes': comment_snippet.get('likeCount', 0),
                    'AuthorChannelId': comment_snippet.get('authorChannelId', {}).get('value', 'Unknown'),
                    'PublishedAt': comment_snippet.get('publishedAt', 'Unknown date')
                })
        except Exception as e:
            if e.resp.status == 403:
                videos_with_disabled_comments.append(video_id)
                continue #no comments, skip to next video
            else:
                print(f"Error fetching comments for video {video_id}: {e}")
    if videos_with_disabled_comments:
        print(f"Comments are disabled for videos: {', '.join(videos_with_disabled_comments)}")
    print(f"comments fetched..")
    return comments

# Function to fetch channel details, including country
def fetch_channel_countries(youtube, channel_ids):
    channel_countries = {}
    BATCH_SIZE = 50 

    # Process channel IDs in batches to reduce API calls
    for i in range(0, len(channel_ids), BATCH_SIZE): # 98% Less API calls!
        batch_channel_ids = channel_ids[i:i+BATCH_SIZE]
        try:
            response = youtube.channels().list(
                id=",".join(batch_channel_ids),
                part="snippet"
            ).execute()
            for item in response.get("items", []):
                channel_id = item["id"]
                country = item["snippet"].get("country", "Unknown")
                channel_countries[channel_id] = country
        except Exception as e:
            print(f"Error fetching channel details: {e}")

    return channel_countries

def fetch_channel_subscriber_count(youtube, channel_ids):
    channel_subscribers = {}
    for channel_id in channel_ids:
        try:
            response = youtube.channels().list(id=channel_id, part='statistics').execute()
            for item in response.get('items', []):
                subscribers = item['statistics'].get('subscriberCount', 'Unknown')
                channel_subscribers[channel_id] = subscribers
        except Exception as e:
            print(f"Error fetching subscriber count for channel {channel_id}: {e}")
            channel_subscribers[channel_id] = 'Unknown'
    return channel_subscribers

# Main function to orchestrate the fetching and compiling of YouTube data
def search_term_fetch(search_term):
    if search_term:  # Only proceed if a search term was entered
        youtube = initialize_youtube_api()

        # Fetch video details based on the search term
        video_details = fetch_video_details(youtube, search_term)
        video_ids = [video['ID'] for video in video_details]

        # Fetch comments for the fetched videos
        comments = fetch_comments(youtube, video_ids)

        # Create DataFrames from the fetched data
        videos_df = pd.DataFrame(video_details)
        comments_df = pd.DataFrame(comments)

        # Fetch channel subscriber count for the channels associated with the videos
        unique_channel_ids = list(set(videos_df['Channel ID']))
        channel_subscribers = fetch_channel_subscriber_count(youtube, unique_channel_ids)

        # Map the subscriber count to the videos DataFrame
        videos_df['Subscriber Count'] = videos_df['Channel ID'].map(channel_subscribers)

        # Fetch channel countries for additional data enrichment
        channel_countries = fetch_channel_countries(youtube, unique_channel_ids)
        videos_df['Country'] = videos_df['Channel ID'].map(channel_countries)

        # Insert the search term column at the beginning of both DataFrames
        videos_df.insert(0, 'Search Term', search_term)
        comments_df.insert(0, 'Search Term', search_term)

        # Merge video details with comments
        final_df = pd.merge(videos_df, comments_df, on='ID', how='outer')

        # Save the updated DataFrame
        csv_filename = f'./data/{search_term}_youtube.csv'
        final_df.to_csv(csv_filename, index=False)
        st.success(f"Data saved to {csv_filename}.")


