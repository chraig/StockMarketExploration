#! -*- coding: utf-8 -*-
import json
from alpha_vantage.timeseries import TimeSeries


def load_appconfig():
    with open("appconfig.json", "r") as f:
        app_config = json.load(f)

    api_key = app_config["vantage_api_key"]
    return api_key


def api_usage_example(api_key: str):
    ts = TimeSeries(key=api_key, output_format="pandas")
    data, meta_data = ts.get_intraday(symbol="MSFT", interval="1min", outputsize="full")
    return data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    api_key = load_appconfig()
    data = api_usage_example(api_key=api_key)
    print(data)
