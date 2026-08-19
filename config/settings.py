from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "hzgjjzf"

    TARGET_URL: str = "https://gjj.hangzhou.gov.cn/col/col1229287674/index.html"
    TARGET_DOMAIN: str = "gjj.hangzhou.gov.cn"

    API_URL: str = "/api-gateway/jpaas-publish-server/front/page/build/unit"
    API_PARAMS: dict = {
        "webId": "3149",
        "pageId": "1229287674",
        "parseType": "bulidstatic",
        "pageType": "column",
        "tagId": "当前栏目列表",
        "tplSetId": "vBrxUb49QDxnBCMDHZlF1",
    }
    PAGE_SIZE: int = 14

    REQUEST_DELAY: tuple[float, float] = (3.0, 8.0)
    MAX_RETRIES: int = 3
    TIMEOUT: int = 30
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    PROXY_ENABLED: bool = False
    PROXY_URL: str = ""

    OUTPUT_DIR: str = "data"
    CSV_FILENAME: str = "report.csv"
    LAST_DATE_FILE: str = "last_date.txt"
    LOG_LEVEL: str = "INFO"

    DETAIL_FIELDS: list[str] = [
        "title", "publish_date", "source",
        "notice_object", "detail_content",
        "content_html", "keywords", "description",
        "url", "article_id",
    ]

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


settings = Settings()