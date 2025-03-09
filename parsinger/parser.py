from __future__ import annotations
import requests
from bs4 import BeautifulSoup
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from parsinger.managers import Manager
from parsinger.times import Clocks
from flask_timetable.settings import *
from handlers.decorators import session_error_handling

if TYPE_CHECKING:
    from preparations import Preparations


class Parser(ABC):
    def __init__(self, configuration: Preparations):
        self.config = configuration
        self.session = self.create_session()
        self.clocks = Clocks()

    def create_session(self):
        session = requests.Session()
        session.headers.update(self.config.get_headers())
        # session.proxies.update(self.config.get_proxies())  # скорость зависит от прокси
        return session

    def kill_old_session(self):
        self.session.close()
        self.session = self.create_session()

    @session_error_handling
    def do_request(self, url, params=None):
        return self.session.get(
            url,
            params=params,
        )

    def get_html(self, url, params=None):
        response = self.do_request(url, params)
        return response.text

    def create_soup(self, html):
        soup = BeautifulSoup(html, "lxml")
        return soup

    @session_error_handling
    def get_selection_page(self, url, params=None):
        html = self.get_html(url, params)
        soup = self.create_soup(html)
        return soup

    @abstractmethod
    def get_timetable(self): ...


class MauParser(Parser, ABC):
    def __init__(self, configuration: Preparations):
        super().__init__(configuration)
        self.start_page = super().get_selection_page(BASE_URL)
        self.manager = Manager()

    def create_parameter(self, parameter) -> str:
        selects = self.start_page.find("select", attrs={"name": parameter})
        values = selects.find_all("option")
        print(*[value.text for value in values[1:]], sep="\n")
        inp = input(f"{values[0].text}: ")
        for value in values[1:]:
            if inp.lower() == value.text.lower():
                return value.attrs["value"]

    def get_parameter_values(self, parameter: str) -> dict:
        selects = self.start_page.find("select", attrs={"name": parameter})
        values = selects.find_all("option")
        return {value.text: value.attrs["value"] for value in values[1:]}

    @abstractmethod
    def define_data(self): ...


class GroupsParser(MauParser):
    def __init__(self, configuration: Preparations):
        super().__init__(configuration)
        self.parameter_names = GROUP_PARAMS
        self.config_names = GROUP_CONFIG_PARAMS
        self.parameters = {"mode": "1"}

    def get_params(self, names: list | None = None, filename=FILE) -> dict:
        data = self.manager.get_from(filename)
        data.update(self.parameters)
        if names is None:
            return data
        result = {}
        for name in names:
            result[name] = data.get(name)
        return result

    def get_groups(self):
        params = self.parameters
        params.update(self.manager.get_from(FILE))
        print(params)
        soup = self.get_selection_page(BASE_URL, params)
        groups = soup.select("div.table-responsive a.btn")
        groups = {group.text: group.attrs["href"] for group in groups}
        print(groups)
        return groups

    def fast_select_group(self, date: str):
        pers = self.get_parameter_values(GROUP_PARAMS[0]).keys()
        data = self.clocks.get_period_params(pers, date)
        settings = self.manager.get_from(GROUP_SETTINGS)
        settings.update(data)
        self.manager.save_to(settings, GROUP_SETTINGS)
        return (BASE_TIMETABLE_URL, settings)

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

    def define_data(self): ...


class TeacherParser(MauParser):
    def __init__(self, configuration: Preparations):
        super().__init__(configuration)
        self.start_page = super().get_selection_page(BASE_URL)
        self.parameter_names = TEACHER_PARAMS
        self.parameters = {"mode2": "1", "tab": "2"}

    def get_teachers(self) -> dict:
        params = self.parameters
        params.update(self.manager.get_from(FILE_T))
        print(params)
        soup = self.get_selection_page(BASE_URL, params)
        teachers = soup.select("table.table a")
        teachers = {teacher.text: teacher.attrs["href"] for teacher in teachers}
        return teachers

    def get_params(self, names=None) -> dict:
        if names is None:
            names = self.parameter_names

        params = self.parameters
        params[names[0]] = self.create_parameter(names[0])  # pers2
        inp = input("Введите текст для поиска преподавателя: ")
        params[names[1]] = inp  # sstring

        return params

    def create_config(self, teacher_url: str):
        params = teacher_url.split("?")[1].split("&")
        print(params)
        for element in params:
            if "key" in element:
                value = element.split("=")[1]
                self.manager.save_to({"key": value}, TEACHER_SETTINGS)

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

    def fast_select_teacher(self, date: str):
        pers = self.get_parameter_values(TEACHER_PARAMS[0]).keys()
        data = self.clocks.get_period_params(pers, date)
        settings = self.manager.get_from(TEACHER_SETTINGS)
        settings.update(data)
        self.manager.save_to(settings, TEACHER_SETTINGS)
        return (BASE_TIMETABLE_URL_T, settings)

    def get_timetable(self, date: str):
        return super().get_html(*self.fast_select_teacher(date))

    def define_data(self): ...


# class AuditoriumParser(MauParser): ...


"https://mauniver.ru/student/timetable/new/?mode=1&pers=315&facs=8&courses=1"
# для обычного расписания mode=1 - первый параметр "mode=1&pers=315&facs=7&courses=1"

"https://mauniver.ru/student/timetable/new/?mode=1&pers=323&facs=1&courses=1"
