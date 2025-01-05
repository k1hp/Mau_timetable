from datetime import datetime, timedelta

from flask_timetable.settings import GROUP_CONFIG_PARAMS


class Clocks:
    def __init__(self):
        self.today = datetime.today().date()
        self.format = "%d.%m.%Y"
        self.new_format = "%Y-%m-%d"
        self.period_values = {"today": None, "tomorow": self.today + timedelta(days=1)}

    def remake_period(self, inp: str) -> list[datetime]:
        period = inp.split()[0].split("-")
        start = datetime.strptime(period[0], self.format)
        end = datetime.strptime(period[1], self.format)
        lst = []
        while True:
            lst.append(start.date())
            if end < start + timedelta(days=1):
                break
            start += timedelta(days=1)

        return lst

    def define_need_period(
        self, periods: list[str], our_date: datetime | None = None
    ) -> str:
        if our_date is None:
            our_date = self.today
        for period in periods:
            if our_date in self.remake_period(period):
                return period

    def get_period_params(self, periods: list[str], our_date: str = "today") -> dict:
        our_date = self.period_values[our_date]
        inp = self.define_need_period(periods, our_date)
        start, end, kind = GROUP_CONFIG_PARAMS[1:]
        data = {}
        # вид даты 2025-01-06
        period, week = inp.split()
        period_start, period_end = period.split("-")
        period_start = datetime.strptime(period_start, self.format)
        period_end = datetime.strptime(period_end, self.format)
        data[start] = period_start.strftime(self.new_format)
        data[end] = period_end.strftime(self.new_format)
        data[kind] = week.split("/")[0].strip("(")
        print(data)
        return data


if __name__ == "__main__":
    period = "09.09.2024-15.09.2024 (н/н)"
    periods = [
        "02.09.2024-08.09.2024 (ч/н)",
        "09.09.2024-15.09.2024 (н/н)",
        "16.09.2024-22.09.2024 (ч/н)",
        "23.09.2024-29.09.2024 (н/н)",
        "30.09.2024-06.10.2024 (ч/н)",
        "07.10.2024-13.10.2024 (н/н)",
        "14.10.2024-20.10.2024 (ч/н)",
        "21.10.2024-27.10.2024 (н/н)",
        "28.10.2024-03.11.2024 (ч/н)",
        "04.11.2024-10.11.2024 (н/н)",
        "11.11.2024-17.11.2024 (ч/н)",
        "18.11.2024-24.11.2024 (н/н)",
        "25.11.2024-01.12.2024 (ч/н)",
        "02.12.2024-08.12.2024 (н/н)",
        "09.12.2024-15.12.2024 (ч/н)",
        "16.12.2024-22.12.2024 (ч/н)",
        "23.12.2024-29.12.2024 (н/н)",
        "30.12.2024-05.01.2025 (ч/н)",
        "06.01.2025-12.01.2025 (н/н)",
        "13.01.2025-19.01.2025 (ч/н)",
        "20.01.2025-26.01.2025 (н/н)",
        "27.01.2025-02.02.2025 (ч/н)",
        "03.02.2025-09.02.2025 (н/н)",
        "10.02.2025-16.02.2025 (ч/н)",
    ]

    clocks = Clocks()
    print(clocks.remake_period(period))
    print(clocks.define_need_period(periods))
