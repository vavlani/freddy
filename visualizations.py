import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_category_data
import streamlit as st

def plot_time_series(data_file, output_file=None):
    """
    Plots an interactive line chart for a given time series data file.
    
    Parameters:
    data_file (str): Path to the CSV file containing the time series data.
    
    Returns:
    plotly.graph_objects.Figure: The Plotly figure object for the time series plot.
    """
    # Load the data
    df = pd.read_csv(data_file)
    
    # Create the line chart
    if df.shape[0] == 0:
        return None
    fig = px.line(df, x='date', y='value', title=df['title'][0])
    
    # Add tooltips with text limited to 50 characters
    if 'notes' not in df.columns:
        df['notes'] = ''
    df['notes'] = df['notes'].str.wrap(50).apply(lambda x: x.replace('\n', '<br>'))

    # Add descriptive elements
    fig.update_traces(mode='lines+markers')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title=df['units'][0],
        hovermode='x unified'
    )
    
    fig.update_traces(
        hovertemplate='<b>Date</b>: %{x}<br><b>Value</b>: %{y}<br>' +
                      '<b>ID</b>: %{customdata[0]}<br><b>Title</b>: %{customdata[1]}<br>' +
                      '<b>Frequency</b>: %{customdata[2]}<br><b>Units</b>: %{customdata[3]}<br>' +
                      '<b>Last Updated</b>: %{customdata[4]}<br><b>Notes</b>: %{customdata[5]}<extra></extra>',
        customdata=df[['id', 'title', 'frequency', 'units', 'last_updated', 'notes']].values
    )
    
    # Add time slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    if output_file:
        fig.write_html(output_file)
    else:
        return fig

def plot_category_sunburst(data_file, output_file=None):

    df = load_category_data(data_file)

    # Create the sunburst chart
    fig = px.sunburst(
        df,
        ids='id',
        parents='parent_id',
        names='name',
        values='count',  # Use 'count' to represent the number of categories at each level
        hover_data={'id': True, 'notes': True, 'level': True, 'count': True},
    )

    fig.update_layout(
        margin=dict(t=30, l=0, r=0, b=0),
        hovermode='closest',
        width=420,  # Set the width of the chart
        height=420, # Set the height of the chart
    )

    fig.update_traces(
        hovertemplate='<b>Category</b>: %{label}<br>' +
                    '<b>ID</b>: %{customdata[0]}<br>' +
                    '<b>Notes</b>: %{customdata[1]}<br>' +
                    '<b>Level</b>: %{customdata[2]}<br>' +
                    '<b>Sub-categories</b>: %{customdata[3]}<extra></extra>',
        customdata=df[['id', 'notes', 'level', 'count']].values
    )

    if output_file:
        fig.write_html(output_file)
    else:
        return fig


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plot time series data.")
    parser.add_argument("--data_file", type=str, help="Path to the CSV file containing the time series data.")
    parser.add_argument("--output_file", type=str, help="Path to save the HTML file of the plot.", default=None)

    args = parser.parse_args()

    plot_time_series(args.data_file, args.output_file)
