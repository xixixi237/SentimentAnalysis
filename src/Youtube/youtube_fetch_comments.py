from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv
import argparse
from googleapiclient.errors import HttpError
    
    
    
    
def main(search_term):   
    
    load_dotenv()
    
    DEVELOPER_KEY = os.getenv('DEVELOPER_KEY')
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    # Initialize 
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    def get_top_comments(video_id, max_results=50):
        comments_with_likes = []
        try:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=max_results,
                order='relevance',
                textFormat='plainText'
            ).execute()

            for item in response.get('items', []):
                comment_snippet = item['snippet']['topLevelComment']['snippet']
                comment = comment_snippet['textDisplay']
                likes = comment_snippet.get('likeCount', 0)
                author_channel_id = comment_snippet.get('authorChannelId', {}).get('value', 'Unknown')
                published_at = comment_snippet.get('publishedAt', 'Unknown date')

                comment_info = {
                    'Comment': comment,
                    'Likes': likes,
                    'AuthorChannelId': author_channel_id,
                    'PublishedAt': published_at
                }
                comments_with_likes.append(comment_info)
        except HttpError as e:
            print(f"Error fetching comments for video {video_id}: {e}")
            if e.resp.status == 403:
                print(f"Comments are disabled for video {video_id}.")
        except Exception as e:
            print(f"Error fetching comments for video {video_id}: {e}")
        
        return comments_with_likes  # Ensure this is outside the try/except blocks



    def append_comments_to_df(df):
        comments_details = []

        for index, row in df.iterrows():
            video_id = row['ID']
            comments_with_likes = get_top_comments(video_id)

            for comment_info in comments_with_likes:
                comment_record = {
                    'VideoID': video_id,
                    'AuthorChannelId': comment_info['AuthorChannelId'],
                    'PublishedAt': comment_info['PublishedAt'],
                    'Comment': comment_info['Comment'],
                    'Likes': comment_info['Likes']
                }
                comments_details.append(comment_record)

        comments_df = pd.DataFrame(comments_details)
        df_merged = pd.merge(df, comments_df, left_on='ID', right_on='VideoID', how='left')
        
        return df_merged
    

    def fetch_channel_details(channel_ids):
        channel_details = {}
        try:
            response = youtube.channels().list(
                part="snippet",
                id=",".join(channel_ids)
            ).execute()

            for item in response.get("items", []):
                channel_id = item["id"]
                country = item["snippet"].get("country", "Unknown")
                channel_details[channel_id] = country
        except HttpError as e:
            print(f"Failed to fetch channel details: {e}")
        
        return channel_details  
    
    def update_comments_with_countries(df):
        BATCH_SIZE = 50  # YouTube API allows fetching details for up to 50 channels at a time
        unique_author_ids = df['AuthorChannelId'].dropna().unique()
        string_author_ids = [str(id) for id in unique_author_ids if pd.notnull(id)]
        
        channel_details = {}
        # Process in batches
        for i in range(0, len(string_author_ids), BATCH_SIZE):
            batch = string_author_ids[i:i + BATCH_SIZE]
            batch_details = fetch_channel_details(batch)
            channel_details.update(batch_details)  # Merge batch details into the main dictionary

        # Map the country information back to the DataFrame
        df['Country'] = df['AuthorChannelId'].map(channel_details)

        return df


    
    # Load existing DataFrame
    df_videos = pd.read_csv(f'./data/raw/Youtube/youtube_{search_term}_results.csv')

    # Append comments to DataFrame
    df_videos_with_comments = append_comments_to_df(df_videos)

    # Update DataFrame with country information
    df_videos_with_comments_and_countries = update_comments_with_countries(df_videos_with_comments)

    # Save to a new CSV
    df_videos_with_comments_and_countries.to_csv(f'./data/raw/Youtube/youtube_{search_term}_results_with_comments_and_countries.csv', index=False)

    print(f"Data saved to youtube_{search_term}_results_with_comments_and_countries.csv.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("search_term", help="The search term to use for fetching posts")
    args = parser.parse_args()

    main(args.search_term)