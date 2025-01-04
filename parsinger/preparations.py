from fake_useragent import UserAgent


class Preparations:
    def __init__(self):
        self.user = "tvZ4YH"
        self.passwd = "ZT5upy"
        self.authorization_proxy = self.user + ":" + self.passwd + "@"

    def get_proxy(self) -> dict:
        result = {}
        for proxy in self.proxy_list:
            result.update(
                {
                    "http": f"socks5://{self.authorization_proxy}{proxy}",
                    "https": f"socks5://{self.authorization_proxy}{proxy}",
                }
            )
        return result

    @property
    def proxy_list(self) -> list:
        return ["196.18.2.253:8000"]

    @staticmethod
    def get_headers() -> dict:
        return {
            "User-Agent": UserAgent().chrome,
        }
