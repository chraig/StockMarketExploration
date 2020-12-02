import plotly.graph_objects as go


def candlestick_chart(df):
    return go.Candlestick(
        # x=df.index,
        x=df['date'],
        open=df["1. open"],
        high=df["2. high"],
        low=df["3. low"],
        close=df["4. close"],
        increasing=dict(line=dict(color="green")),
        decreasing=dict(line=dict(color="red")),
        showlegend=False,
        name="candlestick",
    )
