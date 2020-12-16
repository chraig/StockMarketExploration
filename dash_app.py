import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import definitions
from charts import (line_trace, area_trace, candlestick_trace, colored_bar_trace,
                    accumulation_trace, cci_trace, roc_trace, stoc_trace, mom_trace,
                    moving_average_trace, e_moving_average_trace, bollinger_trace, pp_trace)


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
def ticker_line(children):
    return html.Div(children, className="ticker-line")


div_ticker_line = ticker_line([
    # # Interval component for live clock
    # dcc.Interval(id="interval", interval=1 * 100, n_intervals=0),
    html.Div(
        id="live-clock",
        className="live-clock",
        children=html.P(datetime.now().strftime("%H:%M:%S")),
    ),
    html.Div(
        id="ticker",
        className="ticker",
        children=html.P("NEWS NEWS NEWS NEWS NEWS NEWS NEWS NEWS NEWS ")
    )
])


def news_history(children):
    return html.Div(children, className="news-history")


def main_chart_data(children):
    return html.Div(children, className="main-chart-data")


def favorites_board(children):
    return html.Div(children, className="favorites-board")


def analysis_board(children):
    return html.Div(children, className="analysis-board")


div_news_history = news_history([
    html.P("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod"
           + "tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et "
           + "justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata"
           + "sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, "
           + "sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. "
           + "At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata "
           + "sanctus est Lorem ipsum dolor sit amet.")
])

div_main_chart_data = main_chart_data([
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

    html.Div(
        id="period-selection", className="period-selection",
        children=[
            html.Div(id="period_1", className="period", children=[html.A("24h", id="24h")]),
            html.Div(id="period_2", className="period", children=[html.A("7d", id="7d")]),
            html.Div(id="period_3", className="period", children=[html.A("1M", id="1M")]),
            html.Div(id="period_4", className="period", children=[html.A("3M", id="3M")]),
            html.Div(id="period_5", className="period", children=[html.A("6M", id="6M")]),
            html.Div(id="period_6", className="period", children=[html.A("1J", id="1J")]),
            html.Div(id="period_7", className="period", children=[html.A("5J", id="5J")]),
            html.Div(id="period_8", className="period", children=[html.A("MAX", id="MAX")]),
         ]
    ),

    dcc.Dropdown(id="period_selection2",
                 options=definitions.PERIOD_SELECTION_OPTIONS,
                 multi=False,
                 clearable=False,
                 value=definitions.PERIOD_SELECTION_OPTIONS[3]["value"]),
    dcc.Dropdown(id="ticker_selection",
                 options=[{"label": "MSFT", "value": "MSFT"}],
                 multi=False,
                 clearable=False,
                 value="MSFT"),
    dcc.Dropdown(id="chart_type_selection",
                 options=definitions.CHART_TYPE_SELECTION_OPTIONS,
                 multi=False,
                 clearable=False,
                 value=definitions.CHART_TYPE_SELECTION_OPTIONS[0]["value"]),
    dcc.Dropdown(id="study_selection",
                 options=definitions.STUDY_TRACE_SELECTION_OPTIONS,
                 multi=False,
                 clearable=False,
                 value=definitions.STUDY_TRACE_SELECTION_OPTIONS[-2]["value"]),

    html.Div(id="output_container", children=[]),
])


div_favorites_board = favorites_board([
    html.Div(id="favorites_selection", className="favorites-selection", children=[
        html.Div(id="favorite_1", className="favorite", children=[html.P("Favorite 1")]),
        html.Div(id="favorite_2", className="favorite", children=[html.P("Favorite 2")]),
        html.Div(id="favorite_3", className="favorite", children=[html.P("Favorite 3")]),
        html.Div(id="favorite_4", className="favorite", children=[html.P("Favorite 4")]),
        html.Div(id="favorite_5", className="favorite", children=[html.P("Favorite 5")]),
        html.Div(id="favorite_6", className="favorite", children=[html.P("Favorite 6")]),
    ]),
    html.Div(id="favorites_configuration", className="favorites-configuration", children=[]),
])


div_analysis_board = analysis_board([
    div_news_history,
    div_main_chart_data,
    div_favorites_board,
])


app.layout = html.Div(
    className="app",
    children=[
        div_ticker_line,
        div_analysis_board,
    ]
)


# ------------------------------------------------------------------------------

# Returns graph figure
def get_fig(ticker: str, period: int, chart_type: str, studies: tuple):
    if ticker not in tickers:
        fig = go.Figure()
        return fig

    now = datetime.now()
    start_dt = now - timedelta(hours=period)
    end_dt = now

    dff = df.copy()
    dff = dff[(dff.date >= start_dt) & (dff.date <= end_dt)]

    # first row traces
    subplot_traces = [
        "accumulation_trace",
        "cci_trace",
        "roc_trace",
        "stoc_trace",
        "mom_trace",
    ]
    selected_subplots_studies = []
    selected_first_row_studies = []
    row = 1  # number of subplots

    if studies:
        for study in studies:
            if study in subplot_traces:
                row += 1  # increment number of rows only if the study needs a subplot
                selected_subplots_studies.append(study)
            else:
                selected_first_row_studies.append(study)

    fig = make_subplots(
        rows=row,
        shared_xaxes=True,
        shared_yaxes=True,
        cols=1,
        print_grid=False,
        vertical_spacing=0.12,
    )

    # Add main trace (style) to figure, eval of chart type
    fig.append_trace(eval(chart_type)(dff), row=1, col=1)  # chart_type

    # Add trace(s) on fig's first row
    for study in selected_first_row_studies:
        fig = eval(study)(dff, fig)

    row = 1
    # Plot trace on new row
    for study in selected_subplots_studies:
        row += 1
        fig.append_trace(eval(study)(dff), row=row, col=1)

    fig.update_traces(xaxis="x1")  # rebinds all traces to the x-axis

    fig["layout"]["uirevision"] = "The User is always right"  # Ensures zoom on graph is the same on update
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 600

    # legend definitions
    fig["layout"]["showlegend"] = True              # defines if showlegend of single charts is True (default) or False
    # fig["layout"]["legend_orientation"] = "h"     # somehow cannot be defined here
    fig["layout"]["legend"] = dict(y=1, x=0)        # position of legend
    fig["layout"]["font"] = dict(color="#dedddc")   # legend and probably title font definitions

    # x-axis definitions
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False    # disables sub-graph time range slider
    fig["layout"]["xaxis"]["tickformat"] = "%H:%M"              # numbers not showing????????

    # y-axis definitions
    # fig["layout"]["xaxis"]["showline"] = True
    # fig["layout"]["yaxis"]["showgrid"] = True
    fig["layout"]["yaxis"]["gridcolor"] = "#3E3F40"
    fig["layout"]["yaxis"]["gridwidth"] = 1

    # crosshairs definitions
    fig["layout"]["xaxis"]["spikedash"] = "solid"       # solid line instead of dashed default or others
    fig["layout"]["xaxis"]["spikesnap"] = "cursor"      # snap to cursor or data point
    fig["layout"]["yaxis"]["spikedash"] = "solid"       # solid line instead of dashed default or others
    fig["layout"]["yaxis"]["spikesnap"] = "cursor"      # snap to cursor or data point

    fig["layout"].update(paper_bgcolor="#21252C",
                         plot_bgcolor="#21252C",
                         legend_orientation="v",        # orient legend content vertically or horizontally
                         # legend=dict(y=1, x=0),
                         # font=dict(color="#dedddc"),
                         # dragmode='pan',              # grab and move chart instead of time selection
                         hovermode='x unified',         # enables cursor crosshairs
                         )
    return fig


# ------------------------------------------------------------------------------
@app.callback(
    Output(component_id="msft" + "_chart2", component_property="figure"),
    [  # Input(component_id="period_selection2", component_property="value"),
     Input(component_id="3M", component_property="id"),
     Input(component_id="ticker_selection", component_property="value"),
     Input(component_id="chart_type_selection", component_property="value"),
     Input(component_id="study_selection", component_property="value")],
    [State(component_id="msft" + "_chart2", component_property="figure")]
)
def generate_figure_callback(period_4, ticker_selection, chart_type_selection, study_selection, old_fig):

    period_selection = definitions.PERIOD_SELECTION_DICT[period_4]

    if tickers is None:
        return {"layout": {}, "data": {}}

    if ticker_selection not in tickers:
        return {"layout": {}, "data": []}

    if old_fig is None or old_fig == {"layout": {}, "data": {}}:
        return get_fig(ticker_selection, period_selection, chart_type_selection, (study_selection,))

    fig = get_fig(ticker_selection, period_selection, chart_type_selection, (study_selection,))
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
