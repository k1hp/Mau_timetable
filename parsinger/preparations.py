from fake_useragent import UserAgent


class Preparations:
    def __init__(self):
        self.user = "SV4TGr"
        self.passwd = "bxnXF1"
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
        return ["196.19.123.20:8000"]

    @staticmethod
    def get_headers() -> dict:
        return {
            "User-Agent": UserAgent().chrome,
        }
