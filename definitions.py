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
        elif self.unit == "m":
            h = self.value * 24 * 30
        return h


PERIOD_SELECTION_DICT = {
    "Last 8h": LookBackHours(value=8, unit="H").h,
    "Last day": LookBackHours(value=24, unit="H").h,
    "Last week": LookBackHours(value=7, unit="d").h,
    "Last month": LookBackHours(value=1, unit="m").h}


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
    "MOM": "mom_trace"}


STUDY_TRACE_SELECTION_OPTIONS = [{"label": o[0], "value": o[1]}
                                 for o in STUDY_TRACE_SELECTION_DICT.items()]
