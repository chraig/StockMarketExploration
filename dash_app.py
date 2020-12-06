import attr
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import charts
import definitions
from charts import candlestick_trace, accumulation_trace


app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width"}])


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("assets/msft_prices.csv")
# df.set_index("date", inplace=True)
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")
df.rename(columns={"1. open": "open",
                   "2. high": "high",
                   "3. low": "low",
                   "4. close": "close",
                   "5. volume": "volume"},
          inplace=True)
print(df.dtypes)
print(df[:5])

ticker_selected = "MSFT"
tickers = ["MSFT"]


# ------------------------------------------------------------------------------
# Sub-divs loaded into app layout
def charts_div(ticker):
    return html.Div(
        id=ticker+"_graph_div",
        className="display-none",
        children=[
            html.Div(
                dcc.Graph(
                    id=ticker+"_chart",
                    className="chart-graph",
                    config={"displayModeBar": False, "scrollZoom": True},
                )
            ),
        ]
    )


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    className="app",
    children=[
        # Interval component for live clock
        dcc.Interval(id="interval", interval=1 * 100, n_intervals=0),

        # html.H1(className="app-header", children="Stock Markets Exploration Board"),
        dcc.Dropdown(id="period_selection",
                     options=definitions.PERIOD_SELECTION_OPTIONS,
                     multi=False,
                     clearable=False,
                     value=definitions.PERIOD_SELECTION_OPTIONS[2]['value']),
        dcc.Dropdown(id="ticker_selection",
                     options=[{"label": "MSFT", "value": "MSFT"}],
                     multi=False,
                     clearable=False,
                     value="MSFT"),

        html.Div(id="output_container", children=[]),

        # dcc.Graph(id="charts", className="col-charts",
        #           children=[]),  # children=[charts_div(ticker_selected)]),

        # Charts Div
        html.Div(
            id="charts",
            className="charts",
            children=[
                # charts_div(ticker_selected),
                html.Div(
                    id="msft" + "_graph_div",
                    className="display-none",
                    children=[
                        html.Div(
                            dcc.Graph(
                                id="msft" + "_chart",
                                className="chart-graph",
                                config={"displayModeBar": False, "scrollZoom": True},
                                children=[]
                            ),
                        ),
                        html.Div(
                            dcc.Graph(
                                id="msft" + "_chart2",
                                className="chart-graph2",
                                config={"displayModeBar": False, "scrollZoom": True},
                                children=[]
                            ),
                        ),
                    ]
                )
            ],
        ),

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


# Returns graph figure
def get_fig(ticker_selection, period_selection):
    if ticker_selection not in tickers:
        fig = go.Figure()
        return fig

    now = datetime.now()
    start_dt = now - timedelta(hours=period_selection)
    end_dt = now

    dff = df.copy()
    dff = dff[(dff.date >= start_dt) & (dff.date <= end_dt)]

    subplot_traces = [  # first row traces
        "accumulation_trace",
        "cci_trace",
        "roc_trace",
        "stoc_trace",
        "mom_trace",
    ]
    selected_subplots_studies = []
    selected_first_row_studies = []
    row = 1  # number of subplots

    fig = make_subplots(
        rows=row,
        shared_xaxes=True,
        shared_yaxes=True,
        cols=1,
        print_grid=False,
        vertical_spacing=0.12,
    )

    # Add main trace (style) to figure, eval of chart type
    fig.append_trace(eval("candlestick_trace")(dff), 1, 1)

    # Add trace(s) on fig's first row, eval of chart study
    # fig = fig.add_trace(eval("accumulation_trace")(dff))

    row = 1
    # Plot trace on new row
    # fig.append_trace(eval("accumulation_trace")(dff), row, 1)

    fig["layout"][
        "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on update
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["xaxis"]["tickformat"] = "%H:%M"
    fig["layout"]["yaxis"]["showgrid"] = True
    fig["layout"]["yaxis"]["gridcolor"] = "#3E3F40"
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"].update(paper_bgcolor="#21252C", plot_bgcolor="#21252C")

    return fig


# ------------------------------------------------------------------------------
@app.callback(
    Output(component_id="msft" + "_chart2", component_property="figure"),
    [Input(component_id="period_selection", component_property="value"),
     Input(component_id="ticker_selection", component_property="value")],
    [State(component_id="msft" + "_chart2", component_property="figure")]
)
def generate_figure_callback(period_selection, ticker_selection, old_fig):
    if tickers is None:
        return {"layout": {}, "data": {}}

    if ticker_selection not in tickers:
        return {"layout": {}, "data": []}

    if old_fig is None or old_fig == {"layout": {}, "data": {}}:
        return get_fig(ticker_selection, period_selection)

    fig = get_fig(ticker_selection, period_selection)
    return fig


# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id="msft_chart", component_property="figure"),
    [Input(component_id="period_selection", component_property="value"),
     Input(component_id="ticker_selection", component_property="value")]
)
def update_graph_callback(period_selection, ticker_selection):
    if ticker_selection not in tickers:
        fig = go.Figure()
        return fig

    now = datetime.now()
    start_dt = now - timedelta(hours=period_selection)
    end_dt = now

    dff = df.copy()
    dff = dff[(dff.date >= start_dt) & (dff.date <= end_dt)]

    fig = go.Figure(charts.candlestick_chart(dff))

    fig.update_layout(
        title_text="Stock Price",
        # xaxis_rangeslider_visible='slider' in value
    )

    return fig


# Callback for className of div for graphs
@app.callback(
    Output("msft" + "_graph_div", "className"),
    [Input("ticker_selection", "value")]
)
def generate_show_hide_graph_div_callback(ticker_selection):
    return "display-none"


"""
# Callback to update live clock
@app.callback(Output("live-clock", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.now().strftime("%H:%M:%S")
"""


if __name__ == '__main__':
    app.run_server(debug=True)
