# YouTube Channel Analysis App

## Overview

The YouTube Channel Analysis App is a powerful tool that provides in-depth insights and analytics for YouTube channels. By leveraging the YouTube API, this app offers a comprehensive analysis of channel performance, video statistics, and future predictions.

## Features

- Channel Information Display
- Video Title Analysis with Word Cloud
- Top Performing Videos Visualization
- View Count Distribution Analysis
- Upload Schedule Insights
- Future Predictions for Subscribers and Views

## How to Use

1. Enter your YouTube API Key
2. Input the YouTube Channel Handle you want to analyze
3. Explore the various analytics and visualizations provided

## Technical Details

The app is built using:

- Python
- Streamlit for the web interface
- Pandas for data manipulation
- Matplotlib and Plotly for data visualization
- Google API Client for YouTube data retrieval

## Key Components

- `app.py`: Main application file
- `word_cloud_analysis.py`: Generates word cloud from video titles
- `future_predictions.py`: Predicts future subscriber and view counts
- `upload_frequency_analysis.py`: Analyzes upload patterns
- `style.css`: Custom styling for the app

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/youtube-channel-analysis-app.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your YouTube API key:
   - Go to the [Google Developers Console](https://console.developers.google.com/)
   - Create a new project and enable the YouTube Data API v3
   - Create credentials (API key) for your project
   - Save your API key in a secure location

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Data Privacy

This app does not store any user data or API keys. All analysis is performed in real-time using the provided YouTube API key.

## Contributing

Contributions to improve the YouTube Channel Analysis App are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Muhammad Jamri - [@muhammadjamri](https://www.linkedin.com/in/muhammadjamri) - mhmdjmri@gmail.com

Project Link: [https://github.com/your-username/youtube-channel-analysis-app](https://github.com/your-username/youtube-channel-analysis-app)

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Plotly](https://plotly.com/)
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)