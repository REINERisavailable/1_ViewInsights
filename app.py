import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from googleapiclient.discovery import build
import seaborn as sns
from word_cloud_analysis import generate_word_cloud
from future_predictions import predict_future_stats, prepare_chart_data, create_custom_chart
from upload_frequency_analysis import calculate_upload_frequency
import os
from streamlit_extras.metric_cards import style_metric_cards

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

st.set_page_config(layout="wide", page_title="YouTube Channel Analyzer")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

header = st.container()
with header:
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        st.image("View.png", width=800)

st.markdown(
    """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            top: 2.875rem;
            background-color: white;
            z-index: 999;
        }
        .fixed-header {
            border-bottom: 1px solid black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""Enter your YouTube API Key [<a href="https://developers.google.com/youtube/v3/getting-started" target="_blank">How to get API key?</a>]""", unsafe_allow_html=True)
API_KEY = st.text_input('', type='password')

channel_handle = st.text_input('Enter YouTube Channel Handle (e.g., @channelname)', key="search_bar")

if API_KEY and channel_handle:
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        channel_handle = channel_handle.lstrip('@')
        channel_url = f'https://www.youtube.com/@{channel_handle}'
        
        channel_response = youtube.channels().list(part='snippet,statistics', forHandle=channel_handle).execute()

        if 'items' in channel_response and len(channel_response['items']) > 0:
            channel_info = channel_response['items'][0]
            statistics = channel_info['statistics']
            snippet = channel_info['snippet']
            
            st.subheader("Channel Information")

            col_logo, col_info = st.columns([1, 4])
            with col_logo:
                logo_url = snippet.get('thumbnails', {}).get('high', {}).get('url', '')
                if logo_url:
                    st.markdown(f'''
                        <a href="{channel_url}" target="_blank">
                            <img src="{logo_url}" width="200" style="border-radius: 20%; object-fit: cover; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
                        </a>
                    ''', unsafe_allow_html=True)
                else:
                    st.warning("No channel logo available")

            with col_info:
                style_metric_cards(
                    background_color="#FFEBEE",
                    border_left_color="#D32F2F",
                    border_color="#FF4444",
                    box_shadow="#B71C1C"
                )

                col1, col2, col3, col4 = st.columns(4, gap="small")

                with col1:
                    st.error('Channel Title', icon="📺")
                    st.metric(label="", value=snippet['title'])

                with col2:
                    st.error('Subscriber Count', icon="👥")
                    st.metric(label="", value=f"{int(statistics.get('subscriberCount', 0)):,}")

                with col3:
                    st.error('Total Views', icon="👁️")
                    st.metric(label="", value=f"{int(statistics.get('viewCount', 0)):,}")

                with col4:
                    st.error('Total Videos', icon="🎥")
                    st.metric(label="", value=f"{int(statistics.get('videoCount', 0)):,}")

            st.subheader("Video Title Analysis")
            with st.spinner("Generating word cloud..."):
                try:
                    wordcloud_fig, video_data = generate_word_cloud(channel_info['id'], API_KEY, background_color='white')
                    if wordcloud_fig is not None:
                        st.pyplot(wordcloud_fig)
                    else:
                        st.warning("Unable to generate word cloud. Not enough data available.")
                except Exception as e:
                    st.error(f"Error generating word cloud: {str(e)}")

            if 'video_data' in locals() and not video_data.empty:
                st.subheader("Top Performing Videos")
                top_videos = video_data.sort_values('viewCount', ascending=False).head(10)
                fig = px.bar(top_videos, x='title', y='viewCount', title='Top 10 Videos by View Count', color_discrete_sequence=['#FF0000'])
                fig.update_layout(xaxis_title="Video Title", yaxis_title="View Count")
                st.plotly_chart(fig)

                st.subheader("View Count Distribution")
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.violinplot(y='viewCount', data=video_data, ax=ax, color='#FF0000')
                plt.title("Distribution of Video Views")
                plt.xlabel("All Videos")
                plt.ylabel("View Count")
                
                y_ticks = [0, 25000000, 50000000, 75000000, 100000000]
                ax.set_yticks(y_ticks)
                ax.set_yticklabels([f'{int(y/1e6)}M' for y in y_ticks])
                ax.set_ylim(0, 100000000)
                
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
                
                st.pyplot(fig)

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Upload Schedule")
                    video_data['publishedAt'] = pd.to_datetime(video_data['publishedAt'])
                    video_data['publishDayName'] = video_data['publishedAt'].dt.day_name()
                    day_df = pd.DataFrame(video_data['publishDayName'].value_counts()).reset_index()
                    day_df.columns = ['Day', 'Count']
                    day_df = day_df.sort_values('Day')
                    fig = px.bar(day_df, x='Day', y='Count', title='Upload Frequency by Day of Week')
                    fig.update_traces(marker_color='#FF0000')
                    st.plotly_chart(fig)

                with col2:
                    st.subheader("Future Predictions")
                    
                    future_df = predict_future_stats(API_KEY, channel_info['id'])
                        
                    st.write("Prediction Table:")
                    st.dataframe(future_df)
                chart_data = prepare_chart_data(future_df)
                        
                subscribers_fig = create_custom_chart(chart_data, "Subscribers Prediction", "Subscribers Prediction")
                views_fig = create_custom_chart(chart_data, "Views Prediction", "Views Prediction")
                        
                st.plotly_chart(subscribers_fig, use_container_width=True)
                st.plotly_chart(views_fig, use_container_width=True)
                        
            else:
                st.warning("No video data available for analysis.")

        else:
            st.error('Channel not found. Please check the handle and try again.')

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Please check your API key and ensure you have proper YouTube API access.")

else:
    st.warning("Please enter both your YouTube API Key and a channel handle to proceed.")

st.markdown(
    """
    <div class="footer">
        <a href="https://github.com/REINERisavailable/1_ViewInsights/blob/main/README.md" target="_blank">Documentation</a>
        <a href="mailto:mhmdjmri@gmail.com?subject=Feedback%20-%20YouTube%20Stats">Feedback</a>
        <a href="https://www.linkedin.com/in/muhammadjamri" target="_blank">LinkedIn</a>
        <a href="mailto:mhmdjmri@gmail.com">Email</a>
    </div>
    """,
    unsafe_allow_html=True
)

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)