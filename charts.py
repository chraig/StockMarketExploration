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
        showlegend=True,
        name="candlestick",
    )


# STUDIES TRACES --------------------------------------------------------------
# Moving average
def moving_average_trace(df, fig):
    df2 = df.rolling(window=5).mean()
    trace = go.Scatter(
        x=df2.index, y=df2["close"], mode="lines", showlegend=True, name="MA",
        line=dict(width=1),
    )
    fig.append_trace(trace, 1, 1)  # plot in first row
    return fig


# Exponential moving average
def e_moving_average_trace(df, fig):
    df2 = df.rolling(window=20).mean()
    trace = go.Scatter(
        x=df2.index, y=df2["close"], mode="lines", showlegend=True, name="EMA",
        line = dict(width=1),
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
        x=df.index, y=upper_band, mode="lines", showlegend=True,
        name="BB_upper", line=dict(width=0.6),
    )

    trace2 = go.Scatter(
        x=df.index, y=rolling_mean, mode="lines", showlegend=True,
        name="BB_mean", line=dict(width=0.6),
    )

    trace3 = go.Scatter(
        x=df.index, y=lower_band, mode="lines", showlegend=True,
        name="BB_lower", line=dict(width=0.6),
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
        x=df.index, y=df["volume"], mode="lines", showlegend=True,
        name="Accumulation", line=dict(width=0.6),
    )
    return trace


# Commodity Channel Index
# Developed by Donald Lambert, the Commodity Channel Index (CCI) is a momentum-based oscillator used to help determine
# when an investment vehicle is reaching a condition of being overbought or oversold. It is also used to assess price
# trend direction and strength. This information allows traders to determine if they want to enter or exit a trade,
# refrain from taking a trade, or add to an existing position. In this way, the indicator can be used to provide trade
# signals when it acts in a certain way.
# source: https://www.investopedia.com/terms/c/commoditychannelindex.asp
def cci_trace(df, n_days=20):
    tp = (df["high"] + df["low"] + df["close"]) / 3
    cci = pd.Series(
        (tp - tp.rolling(window=n_days, center=False).mean())
        / (0.015 * tp.rolling(window=n_days, center=False).std()),
        name="cci",
    )
    trace = go.Scatter(x=df.index, y=cci, mode="lines", showlegend=True,
                       name="CCI", line=dict(width=0.6),)
    return trace


# Price Rate of Change
# The Price Rate of Change (ROC) is a momentum-based technical indicator that measures the percentage change in price
# between the current price and the price a certain number of periods ago. The ROC indicator is plotted against zero,
# with the indicator moving upwards into positive territory if price changes are to the upside, and moving into
# negative territory if price changes are to the downside.
# source: https://www.investopedia.com/terms/p/pricerateofchange.asp
def roc_trace(df, n_days=5):
    n = df["close"].diff(n_days)
    d = df["close"].shift(n_days)
    roc = pd.Series(n / d, name="roc")
    trace = go.Scatter(x=df.index, y=roc, mode="lines", showlegend=True,
                       name="ROC", line=dict(width=0.6),)
    return trace


# Stochastic oscillator %K
def stoc_trace(df):
    so_k = pd.Series((df["close"] - df["low"]) / (df["high"] - df["low"]),
                     name="SO%k")
    trace = go.Scatter(x=df.index, y=so_k, mode="lines", showlegend=True,
                       name="SO%k", line=dict(width=0.6),)
    return trace


# Momentum
def mom_trace(df, n=5):
    m = pd.Series(df["close"].diff(n), name="Momentum_" + str(n))
    trace = go.Scatter(x=df.index, y=m, mode="lines", showlegend=True,
                       name="MOM", line=dict(width=0.6),)
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
    trace = go.Scatter(x=df.index, y=pp, mode="lines", showlegend=True,
                       name="PP", line=dict(width=0.6),)
    trace1 = go.Scatter(x=df.index, y=r1, mode="lines", showlegend=True,
                        name="R1", line=dict(width=0.6),)
    trace2 = go.Scatter(x=df.index, y=s1, mode="lines", showlegend=True,
                        name="S1", line=dict(width=0.6),)
    trace3 = go.Scatter(x=df.index, y=r2, mode="lines", showlegend=True,
                        name="R2", line=dict(width=0.6),)
    trace4 = go.Scatter(x=df.index, y=s2, mode="lines", showlegend=True,
                        name="S2", line=dict(width=0.6),)
    trace5 = go.Scatter(x=df.index, y=r3, mode="lines", showlegend=True,
                        name="R3", line=dict(width=0.6),)
    trace6 = go.Scatter(x=df.index, y=s3, mode="lines", showlegend=True,
                        name="S3", line=dict(width=0.6),)
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
        x=df.index, y=df["close"], mode="lines", showlegend=True, name="Line",
        line=dict(width=0.6)
    )
    return trace


def area_trace(df):
    trace = go.Scatter(
        x=df.index, y=df["close"], showlegend=True, fill="toself", name="Area",
        line=dict(width=0.6)
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
        showlegend=True,
        name="Bar",
        line=dict(width=0.6),
    )


def colored_bar_trace(df):
    return go.Ohlc(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        showlegend=True,
        name="Colored bar",
        line=dict(width=0.6),
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
        showlegend=True,
        name="Candlestick",
        line=dict(width=0.6),
    )
