from datetime import datetime, timedelta


class Clocks:
    def __init__(self):
        self.today = datetime.today().date()
        self.format = "%d.%m.%Y"

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

    def define_today_period(self, periods: list[str]) -> str:
        print(self.today)
        for period in periods:
            if self.today in self.remake_period(period):
                return period


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
    print(clocks.define_today_period(periods))
