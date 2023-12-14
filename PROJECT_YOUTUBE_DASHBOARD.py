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
selected_year = st.sidebar.slider("Select Year", min_value=df['year'].min(), max_value=df['year'].max(), value=default_year, key='year_slider')

# Filter the DataFrame based on the selected channel, metric, and year
filtered_df = df[(df['channel_name'] == selected_channel) & (df['year'] == selected_year)]

# Filter data for videos and shorts
videos_df = filtered_df[filtered_df['short'] == 0]
shorts_df = filtered_df[filtered_df['short'] == 1]

# Create two line charts, one for videos and one for shorts
fig_videos = px.line(videos_df, x='published', y=selected_metric,
                     title=f'Line Chart of {metric_names[selected_metric]} for Videos',
                     labels={'published': 'Published Date', selected_metric: metric_names[selected_metric]})

fig_shorts = px.line(shorts_df, x='published', y=selected_metric,
                     title=f'Line Chart of {metric_names[selected_metric]} for Shorts',
                     labels={'published': 'Published Date', selected_metric: metric_names[selected_metric]})

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
