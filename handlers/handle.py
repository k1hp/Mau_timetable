from bs4 import BeautifulSoup
from parsinger.times import Clocks


class HandleHTML(Clocks):
    def __init__(self, text: str):
        super().__init__()
        self.pars = "lxml"
        self.soup = BeautifulSoup(text, "lxml")
        self.months = {
            "января": 1,
            "февраля": 2,
            "марта": 3,
            "апреля": 4,
            "мая": 5,
            "июня": 6,
            "июля": 7,
            "августа": 8,
            "сентября": 9,
            "октября": 10,
            "ноября": 11,
            "декабря": 12,
        }

    def get_table(self):
        table = self.soup.find("div", class_="row table-row")
        # head = soup.select_one("div[class='col-md-12 content bvi-speech'] h1")
        # head = head.prettify()
        return table

    def get_days(self) -> list[tuple]:
        table = self.get_table()
        dates = [date.text for date in table.find_all("th")]
        bodies = table.find_all("table")
        return zip(dates, bodies)

    def convert_into_text(self, bs_object):
        return bs_object.prettify()


class CreatorTimetables(HandleHTML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_day(self, current_day):
        need_date = self.get_day_month(current_day)
        for date, body in self.get_days():
            print(date)
            day, month = date.split()[1:]
            month = self.months[month]
            if (int(day), month) == need_date:
                return date, body

    def create_today(self):
        return self.create_day(self.period_values["today"])

    def create_tomorrow(self):
        return self.create_day(self.period_values["tomorrow"])

    def create_week(self):
        bs_obj = self.get_table()
        return self.convert_into_text(bs_object=bs_obj)
