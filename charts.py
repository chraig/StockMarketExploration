import plotly.graph_objects as go


# Accumulation Distribution
def accumulation_trace(df):
    df["volume"] = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / (
        df["high"] - df["low"]
    )
    trace = go.Scatter(
        x=df.index, y=df["volume"], mode="lines", showlegend=False, name="Accumulation"
    )
    return trace


def candlestick_trace(df):
    return go.Candlestick(
        # x=df.index,
        x=df["date"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        increasing=dict(line=dict(color="green")),
        decreasing=dict(line=dict(color="red")),
        showlegend=False,
        name="candlestick",
    )


def candlestick_chart(df):
    return go.Candlestick(
        # x=df.index,
        x=df["date"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        increasing=dict(line=dict(color="green")),
        decreasing=dict(line=dict(color="red")),
        showlegend=False,
        name="candlestick",
    )
