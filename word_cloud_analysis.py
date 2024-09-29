from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
from collections import Counter
import re
import pandas as pd

def generate_word_cloud(channel_id, api_key, background_color='black'):
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_ids = fetch_video_ids(youtube, channel_id)
    video_data = fetch_video_details(youtube, video_ids)
    all_words = preprocess_titles(video_data['title'])
    word_freq = Counter(all_words)
    wordcloud = WordCloud(width=800, height=400, background_color=background_color, colormap='viridis', stopwords=STOPWORDS, min_font_size=10).generate_from_frequencies(word_freq)
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.title("Most Common Words in Video Titles", fontsize=24)
    return fig, video_data

def preprocess_titles(titles):
    words = ' '.join(titles).lower().split()
    stopwords = set(STOPWORDS)
    words = [word for word in words if word not in stopwords and len(word) > 2]
    words = [re.sub(r'[^a-zA-Z]', '', word) for word in words]
    return words

def fetch_video_ids(youtube, channel_id, max_results=50):
    video_ids = []
    next_page_token = None
    while True:
        try:
            request = youtube.search().list(part="id", channelId=channel_id, maxResults=max_results, type="video", pageToken=next_page_token)
            response = request.execute()
            video_ids.extend([item['id']['videoId'] for item in response['items']])
            next_page_token = response.get('nextPageToken')
            if not next_page_token or len(video_ids) >= 200:
                break
        except Exception as e:
            print(f"An error occurred while fetching video IDs: {str(e)}")
            break
    return video_ids

def fetch_video_details(youtube, video_ids):
    all_video_info = []
    for i in range(0, len(video_ids), 50):
        try:
            request = youtube.videos().list(part="snippet,contentDetails,statistics", id=','.join(video_ids[i:i+50]))
            response = request.execute()
            for video in response['items']:
                video_info = {
                    'video_id': video['id'],
                    'title': video['snippet']['title'],
                    'publishedAt': video['snippet']['publishedAt'],
                    'viewCount': int(video['statistics'].get('viewCount', 0)),
                    'likeCount': int(video['statistics'].get('likeCount', 0)),
                    'commentCount': int(video['statistics'].get('commentCount', 0)),
                    'duration': video['contentDetails']['duration']
                }
                all_video_info.append(video_info)
        except Exception as e:
            print(f"An error occurred while fetching video details: {str(e)}")
    return pd.DataFrame(all_video_info)