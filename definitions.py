import attr


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


TIME_SELECTION_DICT = {
    "Last 8h": LookBackHours(value=8, unit="H").h,
    "Last day": LookBackHours(value=24, unit="H").h,
    "Last week": LookBackHours(value=7, unit="d").h,
    "Last month": LookBackHours(value=1, unit="m").h}


TIME_SELECTION_OPTIONS = [{"label": o[0], "value": o[1]} for o in TIME_SELECTION_DICT.items()]
