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


app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width"}])


# ------------------------------------------------------------------------------
# Definitions

@attr.s(kw_only=True)
class LookBackHours:
    value = attr.ib(type=int)
    unit = attr.ib(type=str)
    h = attr.ib()

    @h.default
    def get_look_back_hours(self):
        h = 0
        if self.unit == "H":
            h = self.value
        elif self.unit == "d":
            h = self.value * 24
        elif self.unit == "m":
            h = self.value * 24 * 30
        return h


@attr.s(kw_only=True)
class StartEndTime:
    start_dt = attr.ib(type=datetime)
    end_dt = attr.ib(type=datetime)


@attr.s(kw_only=True)
class DropdownTimeSelectionOptions:
    label = attr.ib(type=str)
    value = attr.ib(type=int)


TIME_SELECTION_DICT = {
    "Last 8h": LookBackHours(value=8, unit="H").h,
    "Last day": LookBackHours(value=24, unit="H").h,
    "Last week": LookBackHours(value=7, unit="d").h,
    "Last month": LookBackHours(value=1, unit="m").h}


TIME_SELECTION_OPTIONS = [{"label": o[0], "value": o[1]} for o in TIME_SELECTION_DICT.items()]


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("msft_prices.csv")
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
                     options=TIME_SELECTION_OPTIONS,
                     multi=False,
                     clearable=False,
                     value=TIME_SELECTION_OPTIONS[0]['value']),
                     # style={'width': "40%"}),

        html.Div(id="output_container", children=[]),

        dcc.Graph(id="charts", className="col-charts",
                  children=[]),
                  #children=[charts_div(ticker_selected)]),

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

# [{"label": "Last 8h", "value": 2020},
# {"label": "Last 24h", "value": 2021}],


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='charts', component_property='figure')],
    [Input(component_id='time_selection', component_property='value')]
)
def update_graph(time_selection):
    print(time_selection)

    container = "The time selected was: {}".format(time_selection)

    now = datetime.now()
    start_dt = now - timedelta(hours=time_selection)
    end_dt = now

    dff = df.copy()
    dff = dff[(dff.date >= start_dt) & (dff.date <= end_dt)]
    print(dff)

    fig = go.Figure(go.Candlestick(
        x=dff['date'],
        open=dff['1. open'],
        high=dff['2. high'],
        low=dff['3. low'],
        close=dff['4. close']
    ))

    fig.update_layout(
        title_text="Stock Price",
        # xaxis_rangeslider_visible='slider' in value
    )

    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig


"""
# Callback to update live clock
@app.callback(Output("live-clock", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.now().strftime("%H:%M:%S")
"""

"""
@app.callback(Output("ticker", "children"), [Input("interval", "n_intervals")])
def update_ticker(n):
    ticker = "test"
    return ticker
"""

if __name__ == '__main__':
    app.run_server(debug=True)
