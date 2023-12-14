import pandas as pd
import streamlit as st
import plotly.express as px

# Load your dataset
df = pd.read_csv("my_data.csv", index_col=False)

# Metric name mapping
metric_names = {
    'view_count': 'Views',
    'comment_count': 'Comments',
    'like_count': 'Likes',
    'engagement': 'Engagement Rate',
}

# Custom function to format metric values
def format_metric_value(value, metric):
    if metric == 'engagement':
        return f"{value * 100:.2f}%"
    elif value >= 1e6:
        return f"{value / 1e6:.1f}M"
    elif value >= 1e3:
        return f"{value / 1e3:.1f}K"
    else:
        return f"{value:.0f}"

# Create a Streamlit app
st.title("YouTube Analytics")

# Set default values for the filters
default_channel = df['channel_name'].unique()[0]
default_metric = 'view_count'
default_year = df['year'].max()

# Sidebar to select channel name, metric, and year with default values
selected_channel = st.sidebar.selectbox("Select Channel Name", df['channel_name'].unique(), index=0, key='channel_selectbox')
selected_metric = st.sidebar.selectbox("Select Metric", ['view_count', 'like_count', 'comment_count', 'engagement'], index=0, key='metric_selectbox')
selected_year = st.sidebar.slider("Select Year", min_value=df['yea
