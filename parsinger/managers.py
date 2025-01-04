import json


class Manager:
    def __init__(self):
        self.file_name = "profiles.json"

    def save_to(self, data: dict, file_name=None):
        if file_name is None:
            file_name = self.file_name

        with open(file_name, "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=4)

    def get_from(self, file_name=None):
        if file_name is None:
            file_name = self.file_name

        with open(file_name, "r", encoding="UTF-8") as file:
            data = json.load(file)
            return data
