import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("msft_prices.csv")
# df.set_index("date", inplace=True)
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S")
print(df.dtypes)
print(df[:5])


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                    {"label": "2015", "value": 2015},
                    {"label": "2016", "value": 2016},
                    {"label": "2017", "value": 2017},
                    {"label": "2018", "value": 2018},
                    {"label": "2019", "value": 2019},
                    {"label": "2020", "value": 2020}],
                 multi=False,
                 value=2020,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='stock_prices', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='stock_prices', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["date"].dt.year == option_slctd]
    # dff = dff[dff["Affected by"] == "Varroa_mites"]

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


if __name__ == '__main__':
    app.run_server(debug=True)
