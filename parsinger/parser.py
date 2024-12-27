import requests
from bs4 import BeautifulSoup
import json

from parsinger.preparations import Preparations

BASE_URL = "https://mauniver.ru/student/timetable/new/"


class Manager:
    def __init__(self):
        self.file_name = "profiles.json"

    def save_to(self, data: dict, file_name=None):
        if file_name is None:
            file_name = self.file_name

        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

    def get_from(self, file_name=None):
        if file_name is None:
            file_name = self.file_name

        with open(file_name, "r") as file:
            data = json.load(file)
            return data


class Parser:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()

    def do_request(self, url, params=None):
        return self.session.get(
            url,
            headers=self.config.get_headers(),
            proxies=self.config.get_proxy(),
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


class GroupsParser(MauParser):
    def __init__(self, config):
        super().__init__(config)
        self.parameter_names = ["pers", "facs", "courses"]
        self.parameters = {"mode": "1"}

    def get_params(self, names=None) -> dict:
        if names is None:
            names = self.parameter_names

        params = self.parameters
        params.update(
            {parameter: self.create_parameter(parameter) for parameter in names}
        )
        return params

    def select_group(self):
        manager = Manager()
        group_name = None
        inp = input("Хотите просмотреть информацию по прошлой группе: ")
        if "yes" in inp.lower() or "да" in inp.lower():
            input_data = manager.get_from()
            self.parameters = input_data["params"]
            params = self.get_params(names=["pers"])
            group_name = input_data["group_name"]
        else:
            params = self.get_params()

        soup = self.get_selection_page(BASE_URL, params)
        groups = soup.select("div.table-responsive a.btn")
        groups = {group.text: group.attrs["href"] for group in groups}
        if group_name is None:
            print(*groups, sep="\n")
            group_name = input("Выберите группу: ")

        if group_name not in groups:
            raise ValueError

        data = {
            "params": params,
            "group_name": group_name,
        }
        manager.save_to(data)
        return BASE_URL + groups.get(group_name, "")

    def get_timetable(self):
        return super().get_html(self.select_group())


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
    with open("file.html", "w") as f:
        try:
            f.write(timetable.get_timetable())
            print("All is well!")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


"https://mauniver.ru/student/timetable/new/?mode=1&pers=315&facs=8&courses=1"
# для обычного расписания mode=1 - первый параметр "mode=1&pers=315&facs=7&courses=1"

"https://mauniver.ru/student/timetable/new/?mode=1&pers=323&facs=1&courses=1"
