import json
from flask import session


class Manager:

    def save_to(self, data: dict, file_name=None) -> None:
        if file_name is None:
            raise FileNotFoundError("В Manager нет файла по умолчанию")

        session[file_name] = data
        # with open(file_name, "w", encoding="UTF-8") as file:
        #     json.dump(data, file, indent=4)

    def get_from(self, file_name=None) -> dict | None:
        if file_name is None:
            raise FileNotFoundError("В Manager нет файла по умолчанию")

        # with open(file_name, "r", encoding="UTF-8") as file:
        #     data = json.load(file)
        #     return data

        return session.get(file_name, None)
