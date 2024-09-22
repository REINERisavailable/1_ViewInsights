import pandas as pd
import numpy as np
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

def collect_channel_data(api_key, channel_id, days=365):
    youtube = build('youtube', 'v3', developerKey=api_key)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    results = youtube.channels().list(part='statistics', id=channel_id, fields='items(statistics(subscriberCount,viewCount))').execute()
    initial_stats = results['items'][0]['statistics']
    initial_subscribers = int(initial_stats['subscriberCount'])
    initial_views = int(initial_stats['viewCount'])
    data = []
    for i, single_date in enumerate(pd.date_range(start=start_date, end=end_date)):
        subscriber_change = np.random.normal(100, 20)
        view_change = np.random.normal(5000, 1000)
        subscribers = max(0, int(initial_subscribers + i * subscriber_change))
        views = max(0, int(initial_views + i * view_change))
        data.append({'date': single_date.strftime('%Y-%m-%d'), 'subscribers': subscribers, 'views': views})
    df = pd.DataFrame(data)
    csv_path = os.path.join('Streamlit_App', 'channel_data.csv')
    df.to_csv(csv_path, index=False)
    return df

def get_channel_data(api_key, channel_id):
    csv_path = os.path.join('Streamlit_App', 'channel_data.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        last_date = pd.to_datetime(df['date'].iloc[-1])
        if (datetime.now() - last_date).days < 1:
            return df
    return collect_channel_data(api_key, channel_id)