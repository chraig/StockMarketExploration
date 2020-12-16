import attr


# ------------------------------------------------------------------------------
# Period selection
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
        elif self.unit == "M":
            h = self.value * 24 * 30
        return h


PERIOD_SELECTION_DICT = {
    "24h": LookBackHours(value=24, unit="H").h,
    "7d": LookBackHours(value=7, unit="d").h,
    "1M": LookBackHours(value=1, unit="M").h,
    "3M": LookBackHours(value=3, unit="M").h,
    "6M": LookBackHours(value=6, unit="M").h,
    "1J": LookBackHours(value=1, unit="J").h,
    "5J": LookBackHours(value=5, unit="J").h}


PERIOD_SELECTION_OPTIONS = [{"label": o[0], "value": o[1]}
                            for o in PERIOD_SELECTION_DICT.items()]


# ------------------------------------------------------------------------------
# Study trace selection
CHART_TYPE_SELECTION_DICT = {
    "Line": "line_trace",
    "Area": "area_trace",
    "Candlestick": "candlestick_trace",
    "Bar": "colored_bar_trace"}


CHART_TYPE_SELECTION_OPTIONS = [{"label": o[0], "value": o[1]}
                                for o in CHART_TYPE_SELECTION_DICT.items()]


# ------------------------------------------------------------------------------
# Study trace selection
STUDY_TRACE_SELECTION_DICT = {
    "Accumulation": "accumulation_trace",
    "CCI": "cci_trace",
    "ROC": "roc_trace",
    "STOC": "stoc_trace",
    "MOM": "mom_trace",
    "PP": "pp_trace",
    "Bollinger Band": "bollinger_trace",
    "Moving average": "moving_average_trace",
    "Exponential moving average": "e_moving_average_trace"}


STUDY_TRACE_SELECTION_OPTIONS = [{"label": o[0], "value": o[1]}
                                 for o in STUDY_TRACE_SELECTION_DICT.items()]
