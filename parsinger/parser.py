import requests
from bs4 import BeautifulSoup
import json

from parsinger.preparations import Preparations
from parsinger.managers import Manager
from parsinger.times import Clocks
from flask_timetable.settings import (
    FILE,
    BASE_URL,
    GROUP_SETTINGS,
    GROUP_PARAMS,
    GROUP_CONFIG_PARAMS,
    BASE_TIMETABLE_URL,
)


class Parser:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.clocks = Clocks()

    def do_request(self, url, params=None):
        return self.session.get(
            url,
            headers=self.config.get_headers(),
            proxies=self.config.get_proxy(),  # скорость зависит от прокси
            params=params,
        )

    def get_html(self, url, params=None):
        response = self.do_request(url, params)
        return response.text

    def create_soup(self, html):
        soup = BeautifulSoup(html, "lxml")
        return soup

    def get_selection_page(self, url, params=None):
        html = self.get_html(url, params)
        soup = self.create_soup(html)
        return soup

    def get_timetable(self): ...


class MauParser(Parser):
    def __init__(self, config):
        super().__init__(config)
        self.start_page = super().get_selection_page(BASE_URL)

    def create_parameter(self, parameter) -> str:
        selects = self.start_page.find("select", attrs={"name": parameter})
        values = selects.find_all("option")
        print(*[value.text for value in values[1:]], sep="\n")
        inp = input(f"{values[0].text}: ")
        for value in values[1:]:
            if inp.lower() == value.text.lower():
                return value.attrs["value"]

    def define_data(self): ...


class GroupsParser(MauParser):
    def __init__(self, config):
        super().__init__(config)
        self.parameter_names = GROUP_PARAMS
        self.config_names = GROUP_CONFIG_PARAMS
        self.parameters = {"mode": "1"}
        self.manager = Manager()

    def get_params(self, names: list | None = None, filename=FILE) -> dict:
        data = self.manager.get_from(filename)
        data.update(self.parameters)
        if names is None:
            return data
        result = {}
        for name in names:
            result[name] = data.get(name)
        return result

    def get_parameter_values(self, parameter: str) -> dict:
        selects = self.start_page.find("select", attrs={"name": parameter})
        values = selects.find_all("option")
        return {value.text: value.attrs["value"] for value in values[1:]}

    def get_groups(self):
        params = self.parameters
        params.update(
            self.manager.get_from(
                r"C:\Users\USER\PycharmProjects\Mau_timetable\flask_timetable\group_selection.json"
            )
        )
        print(params)
        soup = self.get_selection_page(BASE_URL, params)
        groups = soup.select("div.table-responsive a.btn")
        groups = {group.text: group.attrs["href"] for group in groups}
        print(groups)
        return groups

    def default_select_group(self):
        # group_name = None
        # if old_group:
        #     input_data = self.manager.get_from()
        #     self.parameters = input_data["params"]
        #     params = self.get_params(names=["pers"])
        #     group_name = input_data["group_name"]
        # else:
        params = self.get_params()

        soup = self.get_selection_page(BASE_URL, params)
        groups = soup.select("div.table-responsive a.btn")
        groups = {group.text: group.attrs["href"] for group in groups}
        group_name = params["group"]

        if group_name not in groups:
            raise ValueError("Ошибка в названии группы")

        group_url = groups.get(group_name, "")
        if group_url != "":
            self.create_config(group_url)  # обновляем информацию по группе в конфиге

        return BASE_URL + group_url

    def fast_select_group(self, date: str):
        pers = self.get_parameter_values(GROUP_PARAMS[0]).keys()
        data = self.clocks.get_period_params(pers, date)
        data.update(self.manager.get_from(GROUP_SETTINGS))
        self.manager.save_to(data, GROUP_SETTINGS)
        return (BASE_TIMETABLE_URL, data)

    def create_config(self, group_url: str):
        params = group_url.split("?")[1].split("&")
        print(params)
        for element in params:
            if "key" in element:
                value = element.split("=")[1]
                self.manager.save_to({"key": value}, GROUP_SETTINGS)

    def get_timetable(self, date: str):
        # через try except посмотреть если запрос ничего не дает из готовых параметров
        # return self.get_html(self.default_select_group())
        return self.get_html(*self.fast_select_group(date))


class TeacherParser(MauParser):
    def __init__(self, config):
        super().__init__(config)
        self.start_page = super().get_selection_page(BASE_URL)
        self.parameter_names = ["pers2", "sstring"]
        self.parameters = {"mode2": "1", "tab": "2"}

    def get_params(self, names=None) -> dict:
        if names is None:
            names = self.parameter_names

        params = self.parameters
        params[names[0]] = self.create_parameter(names[0])  # pers2
        inp = input("Введите текст для поиска преподавателя: ")
        params[names[1]] = inp  # sstring

        return params

    def select_teacher(self):
        params = self.get_params()
        soup = self.get_selection_page(BASE_URL, params)
        teachers = soup.select("table.table a")
        teachers = {teacher.text: teacher.attrs["href"] for teacher in teachers}
        print(*teachers, sep="\n")
        teacher_name = input("Выберите группу: ")

        if teacher_name not in teachers:
            raise ValueError

        return BASE_URL + teachers.get(teacher_name, "")

    def get_timetable(self):
        return super().get_html(self.select_teacher())


class AuditoriumParser(MauParser): ...


if __name__ == "__main__":
    config = Preparations()
    timetable = GroupsParser(config)
    # with open("file.html", "w") as f:
    #     f.write(timetable.get_timetable())
    # timetable = TeacherParser(config)
    # soup = BeautifulSoup(timetable.get_timetable(...), "lxml")
    table = soup.find("div", class_="row table-row")
    table = table.prettify()
    head = soup.select_one("div[class='col-md-12 content bvi-speech'] h1")
    head = head.prettify()
    with open("file.html", "w", encoding="utf-8") as f:
        try:
            f.write(head)
            f.write(table)
            print("All is well!")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


"https://mauniver.ru/student/timetable/new/?mode=1&pers=315&facs=8&courses=1"
# для обычного расписания mode=1 - первый параметр "mode=1&pers=315&facs=7&courses=1"

"https://mauniver.ru/student/timetable/new/?mode=1&pers=323&facs=1&courses=1"
