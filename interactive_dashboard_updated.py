
# Open your browser and go to http://127.0.0.1:8050/ to explore the dashboard

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the dataset
df = pd.read_csv("3d_cross_table_updated.csv")

# Initialize the Dash app
app = Dash(__name__)
app.title = "3D Cross-Table Dashboard"

# Layout of the dashboard
app.layout = html.Div([
    html.H1("3D Cross-Table of Sensors, Signal Processing, and Track Parameters"),

    html.Div([
        html.Label("Sensor Type:"),
        dcc.Dropdown(
            options=[{"label": s, "value": s} for s in sorted(df["Sensor Type"].unique())],
            value=None,
            id="sensor-dropdown",
            multi=True,
            placeholder="Select sensor types"
        ),
    ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),

    html.Div([
        html.Label("Signal Processing Technique:"),
        dcc.Dropdown(
            options=[{"label": s, "value": s} for s in sorted(df["Signal Processing Technique"].unique())],
            value=None,
            id="signal-dropdown",
            multi=True,
            placeholder="Select signal processing techniques"
        ),
    ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),

    html.Div([
        html.Label("Track Parameter or Irregularity:"),
        dcc.Dropdown(
            options=[{"label": s, "value": s} for s in sorted(df["Track Parameter or Irregularity"].unique())],
            value=None,
            id="track-dropdown",
            multi=True,
            placeholder="Select track parameters or irregularities"
        ),
    ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),

    dcc.Graph(id="3d-scatter")
])

# Callback to update the 3D scatter plot
@app.callback(
    Output("3d-scatter", "figure"),
    Input("sensor-dropdown", "value"),
    Input("signal-dropdown", "value"),
    Input("track-dropdown", "value")
)
def update_figure(selected_sensors, selected_signals, selected_tracks):
    filtered_df = df.copy()
    if selected_sensors:
        filtered_df = filtered_df[filtered_df["Sensor Type"].isin(selected_sensors)]
    if selected_signals:
        filtered_df = filtered_df[filtered_df["Signal Processing Technique"].isin(selected_signals)]
    if selected_tracks:
        filtered_df = filtered_df[filtered_df["Track Parameter or Irregularity"].isin(selected_tracks)]

    fig = px.scatter_3d(
        filtered_df,
        x="Sensor Type",
        y="Signal Processing Technique",
        z="Track Parameter or Irregularity",
        size="Shared References",
        color="Shared References",
        hover_data={
            "Sensor Type": True,
            "Signal Processing Technique": True,
            "Track Parameter or Irregularity": True,
            "Shared References": True,
            "References": True
        }
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Sensor Type", titlefont=dict(size=14), tickfont=dict(size=10), tickangle=45),
            yaxis=dict(title="Signal Processing Technique", titlefont=dict(size=14), tickfont=dict(size=10), tickangle=45),
            zaxis=dict(title="Track Parameter or Irregularity", titlefont=dict(size=14), tickfont=dict(size=10), tickangle=45)
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    return fig

# Run the app

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run_server(debug=False, host="0.0.0.0", port=port)

