import os
import json
import logging
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from streamlit_plotly_events import plotly_events

from fred_metadata import fetch_all_series_metadata
from fred_data_downloader import (
    fetch_series_info,
    fetch_series_tags,
    save_data_to_csv,
    fetch_fred_data
)
from visualizations import plot_time_series, plot_category_sunburst
from utils import load_category_data, load_data, call_openai

pio.templates.default = "plotly_dark"

# Set the Streamlit layout to use the full width
st.set_page_config(layout="wide")

# Title and subtitle
st.markdown("## :world_map: Freddy's Insights")
st.markdown("### Explore and visualize FRED data series")
st.markdown("**FRED (Federal Reserve Economic Data)** is a comprehensive collection of economic data from various sources. Use this tool to explore and visualize different data series.")

# Create the layout with different sections
top_left_col, top_mid_col, top_right_col = st.columns([1, 1, 1])
bottom_left_col, bottom_right_col = st.columns([1, 3])

data_file = './data/categories/categories_20240615145115.csv'
df = load_category_data(data_file)
    
with top_left_col:
    st.subheader("1. Select a FRED category", divider='rainbow')
    fig = plot_category_sunburst(data_file)
    selected_points = plotly_events(fig, click_event=True, select_event=True)

with top_mid_col:
    st.subheader("2. Popular series for selected category", divider='rainbow')
    if selected_points and 'pointNumber' in selected_points[0]:
        selected_id = selected_points[0]['pointNumber']
        # Perform downstream actions with the selected ID
        filtered_data = df[df.index == selected_id]
        print(filtered_data)

        # Fetch series metadata for the selected category
        selected_category_id = filtered_data['id'].values[0]
        series_metadata = fetch_all_series_metadata(selected_category_id, limit=20)
        if series_metadata is not None:
            # Display the series metadata in a clean table
            st.session_state.series_id_selection = st.dataframe(
                series_metadata, 
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row"
            )

            if 'series_id_selection' in st.session_state:
                if st.session_state.series_id_selection['selection']['rows']:
                    row_num = st.session_state.series_id_selection['selection']['rows'][0]
                    selected_series_id = series_metadata.iloc[row_num]['id']
                    series_info = fetch_series_info(selected_series_id)
                    series_tags = fetch_series_tags(selected_series_id)
                    # explanation = get_series_explanation(series_info)
                    # st.subheader("Series Explanation")
                    # st.write(explanation)



with top_right_col:
    st.subheader("3. Get help understanding the series", divider='rainbow')
    if 'series_id_selection' in st.session_state and \
        st.session_state.series_id_selection['selection']['rows'] and \
            selected_points and 'pointNumber' in selected_points[0]:
        # Generate user prompt
        user_prompt = f"""Explain the following series that was collected from FRED's data portal:\n\
            Series Info: {series_info}\n\n\
            Tags: {series_tags}\n\n\
            Provide a brief explanation of what this series means, \
            where it was sourced from, and talk about it\'s significance (in bullets only) \
            and what kind of insights we can derive from it. Keep it less than 300 words"""
        with st.container(height=430):
            # Display user prompt in an editable text box
            with st.expander("Use this query to have the LLM explain selected series", expanded=True):
                user_prompt = st.text_area("Edit the user prompt below:", user_prompt, height=200)
            
                # with st.expander("LLM's series explanation", expanded=False):
                    # Add a button to generate the OpenAI-driven explanation
            if st.button("Generate Explanation"):
                logging.info("Calling OpenAI API for series explanation")
                explanation = call_openai(user_prompt, model_name="gpt-4o")
                logging.info("Received explanation from OpenAI API")
                st.subheader("Series Explanation")
                st.markdown(explanation, )


with bottom_left_col:
    st.subheader("4. Input series for plotting", divider='rainbow')
    with st.container(height=500):
        # Input fields for series_id, start_date, and end_date
        if 'series_id_selection' in st.session_state:
            if st.session_state.series_id_selection['selection']['rows']:
                id = selected_series_id
                series_id = st.text_input("Enter Series ID", value=id)
        else:
            series_id = st.text_input("Enter Series ID")
        start_date = st.date_input("Start Date", value=datetime(2000, 1, 1), help="Select the start date (YYYY/MM/DD)")
        end_date = st.date_input("End Date", value=datetime.today(), help="Select the end date (YYYY/MM/DD)")

        if 'series_id_selection' in st.session_state:
            if st.session_state.series_id_selection['selection']['rows']:
                data_folder = 'data/series_data'
                data_file = os.path.join(data_folder, f"{selected_series_id}.csv")
                
                series_info_file = os.path.join('data/series_info', f"{selected_series_id}.json")
                
                if os.path.exists(series_info_file):
                    logging.info(f"Loading series info for series_id: {selected_series_id} from local file: {series_info_file}")
                    with open(series_info_file, 'r') as file:
                        series_info = json.load(file)
                else:
                    logging.info(f"Fetching series info for series_id: {selected_series_id} from FRED API")
                    series_info = fetch_series_info(series_id)
                
                if not os.path.exists(data_file):
                    df = fetch_fred_data(selected_series_id, start_date, end_date, series_info)
                    save_data_to_csv(df, selected_series_id, data_folder)
                else:
                    logging.info(f"Loading data for series_id: {selected_series_id} from local file: {data_file}")
                    df = load_data(data_file)
                
                if 'notes' not in series_info:
                    series_info['notes'] = ''
                st.markdown("#### Series information")
                st.markdown(f"<p style='font-size: 16px; color: grey;'><strong>Title:</strong> <span style='color: darkgrey;'>{series_info['title']}</span></p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 16px; color: grey;'><strong>Frequency:</strong> <span style='color: darkgrey;'>{series_info['frequency']}</span></p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 16px; color: grey;'><strong>Notes:</strong> <span style='color: darkgrey;'>{series_info['notes']}</span></p>", unsafe_allow_html=True)


with bottom_right_col:
    st.subheader("5. Visualize the trend", divider='rainbow')
    with st.container(height=500):
        if 'series_id_selection' in st.session_state:
            if st.session_state.series_id_selection['selection']['rows']:
                fig = plot_time_series(data_file)
                if fig is None:
                    logging.info(f"No data returned for series_id: {series_id} for the given time period")
                    st.write('No data returned for series for given time period')
                else:
                    st.plotly_chart(fig, use_container_width=True)

