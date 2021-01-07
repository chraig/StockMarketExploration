import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import dash_actions
import definitions
from charts import (line_trace, area_trace, candlestick_trace,
                    colored_bar_trace, accumulation_trace, cci_trace,
                    roc_trace, stoc_trace, mom_trace, moving_average_trace,
                    e_moving_average_trace, bollinger_trace, pp_trace)


app = dash.Dash(__name__, meta_tags=[{"name": "viewport",
                                      "content": "width=device-width"}])

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

ticker_selected = "MSFT"
tickers = ["MSFT"]


# ------------------------------------------------------------------------------
# Returns main graph figure
def get_main_fig(ticker: str, period: int, chart_type: str, studies: tuple):
    if ticker not in tickers:
        fig = go.Figure()
        return fig

    now = datetime.now()
    start_dt = now - timedelta(hours=period)
    end_dt = now

    dff = df.copy()
    dff = dff[(dff.date >= start_dt) & (dff.date <= end_dt)]

    if dff[dff.date < start_dt].empty:
        true_start_data = [{"date": start_dt, "open": None, "high": None, "low": None, "close": None, "volume": None}]
        dff_new = pd.DataFrame(true_start_data)
        dff_new["date"] = pd.to_datetime(dff_new["date"], format="%Y-%m-%d %H:%M:%S")
        dff = dff_new.append(dff)

    dff.set_index("date", inplace=True)

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
            if study == "":
                break
            if study in subplot_traces:
                # increment number of rows only if the study needs a subplot
                row += 1
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

    # rebinds all traces to the x-axis
    # fig.update_traces(xaxis="x1")

    # Ensures zoom on graph is the same on update
    fig["layout"]["uirevision"] = "The User is always right"

    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 600

    # --- legend definitions ---
    # defines if showlegend of single charts is True (default) or False
    fig["layout"]["showlegend"] = True
    # somehow cannot be defined here
    # fig["layout"]["legend_orientation"] = "h"
    # position of legend
    fig["layout"]["legend"] = dict(y=1, x=0)
    # legend and probably title font definitions
    fig["layout"]["font"] = dict(color="#dedddc")

    # --- x-axis definitions ---
    # disables sub-graph time range slider
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    # numbers not showing????????
    if period <= 24:
        fig["layout"]["xaxis"]["tickformat"] = "%H:%M"
    else:
        fig["layout"]["xaxis"]["tickformat"] = "%Y-%m-%d %H:%M"

    # --- y-axis definitions ---
    # fig["layout"]["xaxis"]["showline"] = True
    # fig["layout"]["yaxis"]["showgrid"] = True
    fig["layout"]["yaxis"]["gridcolor"] = "#3E3F40"
    fig["layout"]["yaxis"]["gridwidth"] = 1

    # --- crosshairs definitions ---
    # solid line instead of dashed default or others
    fig["layout"]["xaxis"]["spikedash"] = "solid"
    # snap to cursor or data point
    fig["layout"]["xaxis"]["spikesnap"] = "cursor"
    # solid line instead of dashed default or others
    fig["layout"]["yaxis"]["spikedash"] = "solid"
    # snap to cursor or data point
    fig["layout"]["yaxis"]["spikesnap"] = "cursor"

    fig["layout"].update(paper_bgcolor="#21252C",
                         plot_bgcolor="#21252C",
                         # orient legend content vertically or horizontally
                         legend_orientation="v",
                         # legend=dict(y=1, x=0),
                         # font=dict(color="#dedddc"),
                         # grab and move chart instead of time selection
                         # dragmode='pan',
                         # enables cursor crosshairs
                         hovermode='x unified',

                         # width=200,
                         # height=200,
                         )
    return fig


def get_empty_fig(msg):
    fig = make_subplots()

    fig["layout"]["xaxis"]["showgrid"] = False
    fig["layout"]["xaxis"]["zeroline"] = False
    fig["layout"]["xaxis"]["visible"] = False
    fig["layout"]["xaxis"]["range"] = [0, 2]

    fig["layout"]["yaxis"]["showgrid"] = False
    fig["layout"]["yaxis"]["zeroline"] = False
    fig["layout"]["yaxis"]["visible"] = False
    fig["layout"]["yaxis"]["range"] = [0, 2]

    fig["layout"].update(paper_bgcolor="#21252C", plot_bgcolor="#21252C",
                         annotations=[
                             dict(
                                 x=1, y=1,  # annotation point
                                 xref='x1', yref='y1',
                                 text=msg,
                                 font=dict(size=40, color="#b2b2b2")
                             )
                         ])

    return fig


# Returns favorite graph figure
def get_favorite_fig(ticker: str, period: int, chart_type: str, studies: tuple):
    if ticker not in tickers:
        fig = go.Figure()
        return fig

    now = datetime.now()
    start_dt = now - timedelta(hours=period)
    end_dt = now

    dff = df.copy()
    dff = dff[(dff.date >= start_dt) & (dff.date <= end_dt)]

    if dff[dff.date < start_dt].empty:
        true_start_data = [{"date": start_dt, "open": None, "high": None,
                            "low": None, "close": None, "volume": None}]
        dff_new = pd.DataFrame(true_start_data)
        dff_new["date"] = pd.to_datetime(dff_new["date"],
                                         format="%Y-%m-%d %H:%M:%S")
        dff = dff_new.append(dff)

    dff.set_index("date", inplace=True)

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
            if study == "":
                break
            if study in subplot_traces:
                # increment number of rows only if the study needs a subplot
                row += 1
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

    # rebinds all traces to the x-axis
    # fig.update_traces(xaxis="x1")

    # Ensures zoom on graph is the same on update
    fig["layout"]["uirevision"] = "The User is always right"

    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    # fig["layout"]["height"] = 600

    # --- legend definitions ---
    # defines if showlegend of single charts is True (default) or False
    fig["layout"]["showlegend"] = False

    # --- x-axis definitions ---
    # disables sub-graph time range slider
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False

    fig["layout"]["yaxis"]["visible"] = False
    fig["layout"]["xaxis"]["visible"] = False

    fig["layout"].update(paper_bgcolor="#21252C",
                         plot_bgcolor="#21252C",
                         # width=200,
                         # height=200,
                         xaxis=dict(
                             autorange=True
                         ),
                         yaxis=dict(
                             autorange=True
                         ),
                         )
    return fig


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

# --- news ticker section
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


# --- analysis board section ---

# news history subsection
def news_history(children):
    return html.Div(children, className="news-history")


# main chart subsection
def main_chart_configuration(children):
    return html.Div(children, className="main-chart-configuration")


def chart_data(children, class_name):
    return html.Div(children, className=class_name)


def main_chart_period(children):
    return html.Div(children, className="main-chart-period")


def main_chart_info(children):
    return html.Div(children, className="main-chart-info")


def main_chart(children):
    return html.Div(children, className="main-chart")


# favorites board subsection
def favorites_board(children):
    return html.Div(children, className="favorites-board")


def analysis_board(children):
    return html.Div(children, className="analysis-board")


div_news_history = news_history([
    html.P("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed")
])


div_main_chart_configuration = main_chart_configuration([
    html.Div(id="data-selection", className="data-selection", children=[
        dcc.Input(id="search-input", className="search-input", type="search",
                  placeholder="Search", debounce=True,
                  # inputMode="latin-prose"
                  )
    ]),
    html.Div(id="chart-depiction-selection",
             className="chart-depiction-selection",
             children=[
                 dcc.Dropdown(id="chart-type-selection",
                              className="dropdown",
                              options=definitions.CHART_TYPE_SELECTION_OPTIONS,
                              multi=False,
                              clearable=False,
                              value=definitions.CHART_TYPE_SELECTION_OPTIONS[0]["value"]),
                 dcc.Dropdown(id="study-selection",
                              className="dropdown",
                              options=definitions.STUDY_TRACE_SELECTION_OPTIONS,
                              multi=False,
                              clearable=False,
                              value=definitions.STUDY_TRACE_SELECTION_OPTIONS[0]["value"]),
             ])
])

div_main_chart_period = main_chart_period([
    html.Div(
        id="period-selection", className="period-selection",
        children=[
            html.Div(id="24H", className="period", children=[html.A("24H")]),
            html.Div(id="7D", className="period", children=[html.A("7D")]),
            html.Div(id="1M", className="period", children=[html.A("1M")]),
            html.Div(id="3M", className="period", children=[html.A("3M")]),
            html.Div(id="6M", className="period", children=[html.A("6M")]),
            html.Div(id="1J", className="period", children=[html.A("1J")]),
            html.Div(id="5J", className="period", children=[html.A("5J")]),
            html.Div(id="MAX", className="period", children=[html.A("MAX")]),
        ]
    ),
])


div_main_chart_data = chart_data([
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
                            config={"displayModeBar": False,
                                    "scrollZoom": True},
                            children=[]
                        ),
                    ),
                ]
            )
        ],
    ),
], "main-chart-data")


def generate_favorite_chart(chart):
    return html.Div(
        id=chart,
        className="favorite",
        children=[
            html.Div(
                id=chart + "_graph_div",
                className="display-none",
                children=[
                    html.Div(
                        dcc.Graph(
                            id=chart + "_chart",
                            className="favorite-chart-graph",
                            config={"displayModeBar": False,
                                    "scrollZoom": False},
                            children=[]
                        ),
                    ),
                    # favorite-chart-overlay covers all access to chart and carries buttons and information
                    html.Div(
                        className="favorite-chart-overlay",
                        children=[
                            html.Div(
                                className="favorite-infos",
                                children=[
                                    html.P(
                                        className="favorite-ticker",
                                        children="MSFT"
                                    ),
                                    html.P(
                                        className="favorite-day-trend",
                                        children="+2.3%"
                                    )
                                ]
                            ),
                            html.Div(
                                className="favorite-buttons",
                                children=[
                                    html.Button(
                                        id=chart + "_select",
                                        className="favorite-button",
                                        children="Select",
                                        n_clicks=0,
                                    ),
                                    html.Button(
                                        id=chart + "_release",
                                        className="favorite-button",
                                        children="Release",
                                        n_clicks=0,
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ],
    )


div_favorites_board = favorites_board([
    html.Div(id="favorites_selection", className="favorites-selection",
             children=[chart_data([generate_favorite_chart(chart)], "favorite-chart-data")
                       for chart in dash_actions.FAVORITE_CHARTS]
             ),
])


div_main_chart_info = main_chart_info([
    html.Div(
        id="main-chart-info",
        className="main-chart-info",
        children=[
            html.Div(
                className="mark-favorite-div",
                children=[
                    html.Button(
                        id="make-favorite-button",
                        className="make-favorite-button",
                        children="Make Favorite",
                        n_clicks=0,
                    )
                ]
            )
        ]
    ),
    html.I(className="fa fa-camera-retro fa-lg")
])


div_main_chart = main_chart([
    div_main_chart_configuration,
    div_main_chart_data,
    div_main_chart_period,
    div_main_chart_info,
])


div_analysis_board = analysis_board([
    div_news_history,
    div_main_chart,
    div_favorites_board,
])


# --- overall layout aggregation ---
app.layout = html.Div(
    className="app",
    children=[
        div_ticker_line,
        div_analysis_board,
    ]
)


# ------------------------------------------------------------------------------
# main chart depiction callback
@app.callback(
    Output(component_id="msft" + "_chart", component_property="figure"),
    [Input(component_id="24H", component_property="n_clicks"),
     Input(component_id="7D", component_property="n_clicks"),
     Input(component_id="1M", component_property="n_clicks"),
     Input(component_id="3M", component_property="n_clicks"),
     Input(component_id="6M", component_property="n_clicks"),
     Input(component_id="1J", component_property="n_clicks"),
     Input(component_id="5J", component_property="n_clicks"),
     Input(component_id="MAX", component_property="n_clicks"),
     Input(component_id="search-input", component_property="value"),
     Input(component_id="chart-type-selection", component_property="value"),
     Input(component_id="study-selection", component_property="value")],
    [State(component_id="msft" + "_chart", component_property="figure")]
)
def generate_main_chart_callback(one_day, one_week, one_month,
                                 three_month, six_month, one_year, five_years,
                                 max_data, search_input, chart_type_selection,
                                 study_selection, old_fig):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "24H" in changed_id:
        period_selection = definitions.PERIOD_SELECTION_DICT["24H"]
    elif "7D" in changed_id:
        period_selection = definitions.PERIOD_SELECTION_DICT["7D"]
    elif "1M" in changed_id:
        period_selection = definitions.PERIOD_SELECTION_DICT["1M"]
    elif "3M" in changed_id:
        period_selection = definitions.PERIOD_SELECTION_DICT["3M"]
    elif "6M" in changed_id:
        period_selection = definitions.PERIOD_SELECTION_DICT["6M"]
    elif "1J" in changed_id:
        period_selection = definitions.PERIOD_SELECTION_DICT["1J"]
    elif "5J" in changed_id:
        period_selection = definitions.PERIOD_SELECTION_DICT["5J"]
    # elif "MAX" in changed_id:
    #     period_selection = definitions.PERIOD_SELECTION_DICT["MAX"]
    else:
        period_selection = definitions.PERIOD_SELECTION_DICT["3M"]

    # dummy while no search bar dummy strategy is met
    if search_input is None:
        search_input = "MSFT"

    if search_input not in tickers:
        return get_empty_fig("No ticker data available")

    if old_fig is None or old_fig["data"] == {}:
        return get_main_fig(search_input, period_selection, chart_type_selection, (study_selection,))

    fig = get_main_fig(search_input, period_selection, chart_type_selection,
                       (study_selection,))

    return fig


# make favorite callback
@app.callback(
    Output(component_id="make-favorite-button", component_property="disabled"),
    Input(component_id="make-favorite-button", component_property="n_clicks"),
)
def mark_favorite(submit_button_clicks):
    print(submit_button_clicks)
    dash_actions.create_favorite()
    return False


# favorite charts callback
def generate_favorite_charts():
    def generate_favorite_charts_callback(search_input, old_fig):
        period_selection = definitions.PERIOD_SELECTION_DICT["7D"]
        chart_type_selection = definitions.CHART_TYPE_SELECTION_OPTIONS[0]["value"]
        study_selection = ""

        # dummy while no search bar dummy strategy is met
        if search_input is None:
            search_input = "MSFT"

        if search_input not in tickers:
            return get_empty_fig("No ticker data available")

        if old_fig is None or old_fig["data"] == {}:
            return get_favorite_fig(search_input, period_selection, chart_type_selection, (study_selection,))

        fig = get_favorite_fig(search_input, period_selection, chart_type_selection, (study_selection,))
        print(fig)

        return fig

    return generate_favorite_charts_callback


for chart in dash_actions.FAVORITE_CHARTS:
    app.callback(
        Output(component_id=chart + "_chart", component_property="figure"),
        Input(component_id="search-input", component_property="value"),
        State(component_id=chart + "_chart", component_property="figure")
    )(generate_favorite_charts())


"""
# Callback to update live clock
@app.callback(Output("live-clock", "children"),
              [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.now().strftime("%H:%M:%S")
"""


if __name__ == '__main__':
    app.run_server(debug=True)
