import time
import random
from abc import ABC, abstractmethod
from typing import Optional

import requests
from loguru import logger

from config.settings import settings
from src.middleware.anti_anti_spider import AntiAntiSpider


class BaseSpider(ABC):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": settings.USER_AGENT})
        self.anti = AntiAntiSpider(self.session)
        self.base_url = f"https://{settings.TARGET_DOMAIN}"

    def request(self, url: str, params: Optional[dict] = None) -> Optional[dict]:
        for attempt in range(1, settings.MAX_RETRIES + 1):
            try:
                self._delay()
                self.anti.randomize_headers()
                full_url = url if url.startswith("http") else f"{self.base_url}{url}"
                resp = self.session.get(
                    full_url, params=params, timeout=settings.TIMEOUT
                )
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                logger.warning(f"request failed (attempt {attempt}) [{url}]: {e}")
                if attempt == settings.MAX_RETRIES:
                    logger.error(f"request failed permanently [{url}]")
                    return None
                time.sleep(2 ** attempt)

    def request_html(self, url: str) -> Optional[str]:
        for attempt in range(1, settings.MAX_RETRIES + 1):
            try:
                self._delay()
                self.anti.randomize_headers()
                full_url = url if url.startswith("http") else f"{self.base_url}{url}"
                resp = self.session.get(full_url, timeout=settings.TIMEOUT)
                resp.raise_for_status()
                resp.encoding = "utf-8"
                return resp.text
            except Exception as e:
                logger.warning(f"HTML request failed (attempt {attempt}) [{url}]: {e}")
                if attempt == settings.MAX_RETRIES:
                    return None
                time.sleep(2 ** attempt)

    def _delay(self):
        delay = random.uniform(*settings.REQUEST_DELAY)
        time.sleep(delay)

    @abstractmethod
    def crawl(self):
        ...