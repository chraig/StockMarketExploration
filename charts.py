import pandas as pd
import plotly.graph_objects as go


# remove later
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


# STUDIES TRACES --------------------------------------------------------------
# Moving average
def moving_average_trace(df, fig):
    df2 = df.rolling(window=5).mean()
    trace = go.Scatter(
        x=df2.index, y=df2["close"], mode="lines", showlegend=False, name="MA"
    )
    fig.append_trace(trace, 1, 1)  # plot in first row
    return fig


# Exponential moving average
def e_moving_average_trace(df, fig):
    df2 = df.rolling(window=20).mean()
    trace = go.Scatter(
        x=df2.index, y=df2["close"], mode="lines", showlegend=False, name="EMA"
    )
    fig.append_trace(trace, 1, 1)  # plot in first row
    return fig


# Bollinger Bands
def bollinger_trace(df, fig, window_size=10, num_of_std=5):
    price = df["close"]
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)

    trace = go.Scatter(
        x=df.index, y=upper_band, mode="lines", showlegend=False, name="BB_upper"
    )

    trace2 = go.Scatter(
        x=df.index, y=rolling_mean, mode="lines", showlegend=False, name="BB_mean"
    )

    trace3 = go.Scatter(
        x=df.index, y=lower_band, mode="lines", showlegend=False, name="BB_lower"
    )

    fig.append_trace(trace, 1, 1)  # plot in first row
    fig.append_trace(trace2, 1, 1)  # plot in first row
    fig.append_trace(trace3, 1, 1)  # plot in first row
    return fig


# Accumulation Distribution
def accumulation_trace(df):
    df["volume"] = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / (
        df["high"] - df["low"]
    )
    trace = go.Scatter(
        x=df.index, y=df["volume"], mode="lines", showlegend=False, name="Accumulation"
    )
    return trace


# Commodity Channel Index
def cci_trace(df, n_days=10):
    tp = (df["high"] + df["low"] + df["close"]) / 3
    cci = pd.Series(
        (tp - tp.rolling(window=n_days, center=False).mean())
        / (0.015 * tp.rolling(window=n_days, center=False).std()),
        name="cci",
    )
    trace = go.Scatter(x=df.index, y=cci, mode="lines", showlegend=False, name="CCI")
    return trace


# Price Rate of Change
def roc_trace(df, n_days=5):
    n = df["close"].diff(n_days)
    d = df["close"].shift(n_days)
    roc = pd.Series(n / d, name="roc")
    trace = go.Scatter(x=df.index, y=roc, mode="lines", showlegend=False, name="ROC")
    return trace


# Stochastic oscillator %K
def stoc_trace(df):
    so_k = pd.Series((df["close"] - df["low"]) / (df["high"] - df["low"]), name="SO%k")
    trace = go.Scatter(x=df.index, y=so_k, mode="lines", showlegend=False, name="SO%k")
    return trace


# Momentum
def mom_trace(df, n=5):
    m = pd.Series(df["close"].diff(n), name="Momentum_" + str(n))
    trace = go.Scatter(x=df.index, y=m, mode="lines", showlegend=False, name="MOM")
    return trace


# Pivot points
def pp_trace(df, fig):
    pp = pd.Series((df["high"] + df["low"] + df["close"]) / 3)
    r1 = pd.Series(2 * pp - df["low"])
    s1 = pd.Series(2 * pp - df["high"])
    r2 = pd.Series(pp + df["high"] - df["low"])
    s2 = pd.Series(pp - df["high"] + df["low"])
    r3 = pd.Series(df["high"] + 2 * (pp - df["low"]))
    s3 = pd.Series(df["low"] - 2 * (df["high"] - pp))
    trace = go.Scatter(x=df.index, y=pp, mode="lines", showlegend=False, name="PP")
    trace1 = go.Scatter(x=df.index, y=r1, mode="lines", showlegend=False, name="R1")
    trace2 = go.Scatter(x=df.index, y=s1, mode="lines", showlegend=False, name="S1")
    trace3 = go.Scatter(x=df.index, y=r2, mode="lines", showlegend=False, name="R2")
    trace4 = go.Scatter(x=df.index, y=s2, mode="lines", showlegend=False, name="S2")
    trace5 = go.Scatter(x=df.index, y=r3, mode="lines", showlegend=False, name="R3")
    trace6 = go.Scatter(x=df.index, y=s3, mode="lines", showlegend=False, name="S3")
    fig.append_trace(trace, 1, 1)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 1)
    fig.append_trace(trace3, 1, 1)
    fig.append_trace(trace4, 1, 1)
    fig.append_trace(trace5, 1, 1)
    fig.append_trace(trace6, 1, 1)
    return fig


# MAIN CHART TRACES (STYLE tab)
def line_trace(df):
    trace = go.Scatter(
        x=df.index, y=df["close"], mode="lines", showlegend=False, name="line"
    )
    return trace


def area_trace(df):
    trace = go.Scatter(
        x=df.index, y=df["close"], showlegend=False, fill="toself", name="area"
    )
    return trace


def bar_trace(df):
    return go.Ohlc(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        increasing=dict(line=dict(color="#888888")),
        decreasing=dict(line=dict(color="#888888")),
        showlegend=False,
        name="bar",
    )


def colored_bar_trace(df):
    return go.Ohlc(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        showlegend=False,
        name="colored bar",
    )


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
