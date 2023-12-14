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

# Set default values for the filters
default_channel = df['channel_name'].unique()[0]
default_metric = 'view_count'
default_year = df['year'].max()

# Sidebar to select channel name, metric, and year with default values
st.sidebar.title("YouTube Analytics Dashboard")
st.sidebar.write("Welcome to the YouTube Analytics Dashboard! Use the filters below to explore YouTube channel statistics.")
selected_channel = st.sidebar.selectbox("Select Channel Name", df['channel_name'].unique(), index=0, key='channel_selectbox')
st.sidebar.write("Select a YouTube channel to analyze.")
selected_metric = st.sidebar.selectbox("Select Metric", ['view_count', 'like_count', 'comment_count', 'engagement'], index=0, key='metric_selectbox')
st.sidebar.write("Choose a metric to visualize.")
selected_year = st.sidebar.slider("Select Year", min_value=df['year'].min(), max_value=df['year'].max(), value=default_year, key='year_slider')
st.sidebar.write("Adjust the year for data analysis.")

# Introduction and Purpose
st.write("""
# YouTube Analytics Dashboard

This interactive dashboard allows you to explore YouTube channel statistics, including views, likes, comments, and engagement rate, for different channels and years. Use the filters on the sidebar to customize your analysis.

## How to Use
1. **Select Channel Name:** Choose a YouTube channel from the dropdown list in the sidebar.
2. **Select Metric:** Select the metric you want to visualize (Views, Likes, Comments, or Engagement Rate).
3. **Select Year:** Adjust the year slider to focus on data from a specific year.

The dashboard will display line charts for the selected metric, broken down into regular videos and shorts (if available). You can analyze trends and compare performance between videos and shorts.

Enjoy exploring the YouTube analytics of my three favorite cooking YouTube channels!
""")

# Update the main title dynamically based on the selected channel
st.title(f"YouTube Analytics for {selected_channel}")

# Filter the DataFrame based on the selected channel, metric, and year
filtered_df = df[(df['channel_name'] == selected_channel) & (df['year'] == selected_year)]

# Filter data for videos and shorts
videos_df = filtered_df[filtered_df['short'] == 0]
shorts_df = filtered_df[filtered_df['short'] == 1]

fig_videos = px.line(videos_df, x='published', y=selected_metric,
                     title=f'Line Chart of {metric_names[selected_metric]} for Videos',
                     labels={'published': 'Published Date', selected_metric: metric_names[selected_metric]},
                     hover_data=['title'])

fig_shorts = px.line(shorts_df, x='published', y=selected_metric,
                     title=f'Line Chart of {metric_names[selected_metric]} for Shorts',
                     labels={'published': 'Published Date', selected_metric: metric_names[selected_metric]},
                     hover_data=['title'])

# Update y-axis labels for engagement to display as percentages
if selected_metric == 'engagement':
    fig_videos.update_yaxes(tickformat=".2%")
    fig_shorts.update_yaxes(tickformat=".2%")

# Create two equal-sized columns to display the charts side by side
col1, col2 = st.columns(2)

# Display the charts in the respective columns
col1.plotly_chart(fig_videos, use_container_width=True)
col2.plotly_chart(fig_shorts, use_container_width=True)

# Calculate and display the average metric value for videos at the bottom of the line chart for videos
average_metric_videos = videos_df[selected_metric].mean()
col1.write(f"Average {metric_names[selected_metric]} in {selected_year} (Videos): {format_metric_value(average_metric_videos, selected_metric)}")

# Calculate and display the average metric value for shorts at the bottom of the line chart for shorts
average_metric_shorts = shorts_df[selected_metric].mean()
col2.write(f"Average {metric_names[selected_metric]} in {selected_year} (Shorts): {format_metric_value(average_metric_shorts, selected_metric)}")
