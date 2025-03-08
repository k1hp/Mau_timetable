from fake_useragent import UserAgent
from typing import List, Optional


class Preparations:
    def __init__(self):
        self.__proxy_list = self.__initialize_proxy_list()

    @staticmethod
    def __initialize_proxy_list() -> List["Proxy"]:
        return [
            Proxy("192.168.1.1", "user1", "password1"),
            Proxy("192.168.1.2", "user2", "password2"),
            Proxy("192.168.1.3"),  # Прокси без авторизации
        ]

    def get_proxy_list(self) -> List["Proxy"]:
        return self.__proxy_list

    @staticmethod
    def get_headers() -> dict:
        return {
            "User-Agent": UserAgent().chrome,
        }

    def get_proxies(self) -> List[dict]:
        proxies = self.get_proxy_list()
        result = []
        for proxy in proxies:
            result.append({"http": proxy, "https": proxy})
        return result


class Proxy:
    def __init__(
        self, ip_address: str, user: Optional[str] = None, passwd: Optional[str] = None
    ):
        self.__ip_address = ip_address
        self.__user = user
        self.__passwd = passwd
        self.__proxy_authorization = (
            f"{self.__user}:{self.__passwd}@" if user and passwd else None
        )

    @property
    def proxy_authorization(self) -> Optional[str]:
        return self.__proxy_authorization

    def __str__(self) -> str:
        if self.__user is not None:
            return f"socks5://{self.proxy_authorization}{self.__ip_address}"
        return f"socks5://{self.__ip_address}"


if __name__ == "__main__":
    cl = Preparations()
    print(cl.get_proxies())
