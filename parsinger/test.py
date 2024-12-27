from parsinger.parser import Parser
from parsinger.preparations import Preparations

parser = Parser(Preparations())


def create_group_url(soup):
    table = soup.select("div.table-responsive a")
    print(table)


url, params = "https://mauniver.ru/student/timetable/new/", {
    "mode": "1",
    "pers": "323",
    "facs": "1",
    "courses": "1",
}

html = parser.get_html(url, params)
soup = parser.create_soup(html)
create_group_url(soup)
