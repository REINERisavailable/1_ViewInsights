import plotly.express as px
from googleapiclient.discovery import build
from collections import Counter
from datetime import datetime

def calculate_upload_frequency(channel_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    upload_dates = []
    next_page_token = None
    while True:
        request = youtube.search().list(part="snippet", channelId=channel_id, maxResults=50, type="video", order="date", pageToken=next_page_token)
        response = request.execute()
        for item in response['items']:
            upload_date = datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            upload_dates.append(upload_date.strftime("%A"))
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    frequency = Counter(upload_dates)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    counts = [frequency.get(day, 0) for day in days]
    fig = px.bar(x=days, y=counts, title='Upload Frequency by Day of Week')
    fig.update_layout(xaxis_title="Day of Week", yaxis_title="Number of Uploads")
    return fig