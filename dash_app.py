import attr
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import charts
import definitions

app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width"}])


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("assets/msft_prices.csv")
# df.set_index("date", inplace=True)
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S")
print(df.dtypes)
print(df[:5])

ticker_selected = "MSFT"


# ------------------------------------------------------------------------------
# Sub-divs loaded into app layout
def charts_div(ticker):
    return html.Div(

    )


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    className="app",
    children=[
        # Interval component for live clock
        dcc.Interval(id="interval", interval=1 * 100, n_intervals=0),

        # html.H1(className="app-header", children="Stock Markets Exploration Board"),
        dcc.Dropdown(id="time_selection",
                     options=definitions.TIME_SELECTION_OPTIONS,
                     multi=False,
                     clearable=False,
                     value=definitions.TIME_SELECTION_OPTIONS[0]['value']),


        dcc.Graph(id="charts", className="col-charts",
                  children=[]),  # children=[charts_div(ticker_selected)]),

        """
        # Ticker line
        html.Div(
            className="div-ticker-line",
            children=[
                html.Div(
                    id="live-clock",
                    className="live-clock",
                    children=datetime.now().strftime("%H:%M:%S")),
                html.Div(
                    id="ticker",
                    className="ticker",
                    children=[
                        html.P("updatetext")
                    ])
            ]
        )
        """
    ]
)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='charts', component_property='figure'),
    Input(component_id='time_selection', component_property='value')
)
def update_graph(time_selection):
    print(time_selection)

    now = datetime.now()
    start_dt = now - timedelta(hours=time_selection)
    end_dt = now

    dff = df.copy()
    dff = dff[(dff.date >= start_dt) & (dff.date <= end_dt)]
    print(dff)

    fig = go.Figure(charts.candlestick_chart(dff))

    fig.update_layout(
        title_text="Stock Price",
        xaxis_rangeslider_visible=False
    )

    return fig


"""
# Callback to update live clock
@app.callback(Output("live-clock", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.now().strftime("%H:%M:%S")
"""


if __name__ == '__main__':
    app.run_server(debug=True)
