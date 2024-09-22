import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_collection import get_channel_data
import plotly.graph_objects as go

def predict_future_stats(api_key, channel_id, months_to_predict=12):
    df = get_channel_data(api_key, channel_id)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    monthly_subscriber_growth = (df['subscribers'].iloc[-1] / df['subscribers'].iloc[0]) ** (1/12) - 1
    monthly_view_growth = (df['views'].iloc[-1] / df['views'].iloc[0]) ** (1/12) - 1
    min_growth, max_growth = 0.01, 0.05
    monthly_subscriber_growth = max(min_growth, min(monthly_subscriber_growth, max_growth))
    monthly_view_growth = max(min_growth, min(monthly_view_growth, max_growth))
    last_date = df['date'].max()
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=months_to_predict, freq='MS')
    last_subscribers, last_views = df['subscribers'].iloc[-1], df['views'].iloc[-1]
    future_subscribers, future_views = [last_subscribers], [last_views]
    for _ in range(1, months_to_predict):
        subscriber_growth = max(0, np.random.normal(monthly_subscriber_growth, 0.01))
        view_growth = max(0, np.random.normal(monthly_view_growth, 0.01))
        new_subscribers = int(future_subscribers[-1] * (1 + subscriber_growth))
        new_views = int(future_views[-1] * (1 + view_growth))
        future_subscribers.append(new_subscribers)
        future_views.append(new_views)
    future_df = pd.DataFrame({
        'Goal Date': future_dates,
        'Time Until': [(date - pd.Timestamp.now()).days for date in future_dates],
        'Subscribers Prediction': future_subscribers,
        'Views Prediction': future_views
    })
    return future_df

def prepare_chart_data(future_df):
    chart_data = future_df[['Goal Date', 'Subscribers Prediction', 'Views Prediction']]
    return chart_data.set_index('Goal Date')

def create_custom_chart(chart_data, title, y_column):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chart_data.index,
        y=chart_data[y_column],
        fill='tozeroy',
        fillcolor='rgba(255, 0, 0, 0.1)',
        line=dict(color='rgba(255, 0, 0, 0.8)'),
        name=y_column
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=y_column,
        yaxis=dict(side="right", showgrid=False, zeroline=False, nticks=3),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig