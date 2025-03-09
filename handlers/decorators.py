import functools
from requests.exceptions import RequestException


def session_error_handling(function):
    @functools.wraps(function)
    def wrapper(self_obj, *args, **kwargs):
        try:
            print("Декторатор применился")
            return function(self_obj, *args, **kwargs)

        except RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            self_obj.kill_old_session()
            self_obj.session = self_obj.create_session()
            return function(self_obj, *args, **kwargs)

    return wrapper
