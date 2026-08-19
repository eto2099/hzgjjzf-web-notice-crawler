import random

from requests import Session
from fake_useragent import UserAgent


class AntiAntiSpider:
    def __init__(self, session: Session):
        self.session = session
        self.ua = UserAgent()
        self._init_headers()

    def _init_headers(self):
        self.session.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        })

    def randomize_headers(self):
        self.session.headers.update({"User-Agent": self.ua.random})
        self.session.headers.update({
            "Referer": random.choice([
                "https://gjj.hangzhou.gov.cn/",
                "https://gjj.hangzhou.gov.cn/col/col1229287674/index.html",
                "https://gjj.hangzhou.gov.cn/col/col1562975/index.html",
            ]),
        })