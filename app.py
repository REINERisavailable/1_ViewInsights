import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from googleapiclient.discovery import build
import seaborn as sns
from word_cloud_analysis import generate_word_cloud
from future_predictions import predict_future_stats, prepare_chart_data, create_custom_chart
from upload_frequency_analysis import calculate_upload_frequency

API_KEY = ''
youtube = build('youtube', 'v3', developerKey=API_KEY)

def load_css():
    with open("Streamlit_App/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="YouTube Channel Analyzer")
load_css()
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.title('YouTube Channel Analysis App')

channel_handle = st.text_input('Enter YouTube Channel Handle (e.g., @channelname)', key="search_bar")

if channel_handle:
    try:
        channel_handle = channel_handle.lstrip('@')
        channel_url = f'https://www.youtube.com/@{channel_handle}'
        
        channel_response = youtube.channels().list(part='snippet,statistics', forHandle=channel_handle).execute()

        if 'items' in channel_response and len(channel_response['items']) > 0:
            channel_info = channel_response['items'][0]
            statistics = channel_info['statistics']
            snippet = channel_info['snippet']

            st.success("Channel found!")
            
            st.subheader("Channel Information")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Channel Title:** {snippet['title']}")
                st.write(f"**Channel URL:** {channel_url}")
            with col2:
                st.write(f"**Subscriber Count:** {int(statistics.get('subscriberCount', 0)):,}")
                st.write(f"**Total Views:** {int(statistics.get('viewCount', 0)):,}")
                st.write(f"**Total Videos:** {int(statistics.get('videoCount', 0)):,}")

            st.subheader("Video Title Analysis")
            with st.spinner("Generating word cloud..."):
                try:
                    wordcloud_fig, video_data = generate_word_cloud(channel_info['id'], API_KEY)
                    if wordcloud_fig is not None:
                        st.pyplot(wordcloud_fig)
                    else:
                        st.warning("Unable to generate word cloud. Not enough data available.")
                except Exception as e:
                    st.error(f"Error generating word cloud: {str(e)}")

            if 'video_data' in locals() and not video_data.empty:
                st.subheader("Top Performing Videos")
                top_videos = video_data.sort_values('viewCount', ascending=False).head(10)
                fig = px.bar(top_videos, x='title', y='viewCount', title='Top 10 Videos by View Count')
                fig.update_layout(xaxis_title="Video Title", yaxis_title="View Count")
                st.plotly_chart(fig)

                st.subheader("View Count Distribution")
                fig, ax = plt.subplots()
                sns.violinplot(x=video_data['viewCount'], ax=ax)
                plt.title("Distribution of Video Views")
                plt.xlabel("View Count")
                st.pyplot(fig)

                st.subheader("Upload Schedule")
                video_data['publishedAt'] = pd.to_datetime(video_data['publishedAt'])
                video_data['publishDayName'] = video_data['publishedAt'].dt.day_name()
                day_df = pd.DataFrame(video_data['publishDayName'].value_counts()).reset_index()
                day_df.columns = ['Day', 'Count']
                day_df = day_df.sort_values('Day')
                fig = px.bar(day_df, x='Day', y='Count', title='Upload Frequency by Day of Week')
                st.plotly_chart(fig)
            else:
                st.warning("No video data available for analysis.")

            st.subheader("Future Predictions")
            try:
                future_df = predict_future_stats(API_KEY, channel_info['id'])
                
                st.write("Prediction Table:")
                st.dataframe(future_df)
                
                chart_data = prepare_chart_data(future_df)
                
                subscribers_fig = create_custom_chart(chart_data, "Subscribers Prediction", "Subscribers Prediction")
                views_fig = create_custom_chart(chart_data, "Views Prediction", "Views Prediction")
                
                st.plotly_chart(subscribers_fig, use_container_width=True)
                st.plotly_chart(views_fig, use_container_width=True)

            except Exception as e:
                st.error("An error occurred while generating predictions:")
                st.exception(e)
                st.write("Unable to generate predictions. This could be due to insufficient historical data or API issues.")
                st.write("API_KEY:", API_KEY)
                st.write("channel_id:", channel_info['id'])

        else:
            st.error('Channel not found. Please check the handle and try again.')

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Please check your API key and ensure you have proper YouTube API access.")

st.markdown(
    """
    <div class="footer">
        <a href="https://example.com/docs" target="_blank">Documentation</a>
        <a href="https://example.com/feedback" target="_blank">Feedback</a>
        <a href="https://www.linkedin.com/in/yourprofile" target="_blank">LinkedIn</a>
        <a href="mailto:mhmdjmri@gmail.com">Email</a>
    </div>
    """,
    unsafe_allow_html=True
)
