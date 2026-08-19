from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "web-notice-crawler"

    TARGET_DOMAIN: str = "example.gov.cn"
    LIST_API_PATH: str = "/api-gateway/jpaas-publish-server/front/page/build/unit"
    LIST_API_PARAMS: dict = {
        "webId": "0000",
        "pageId": "0000",
        "parseType": "bulidstatic",
        "pageType": "column",
        "tagId": "current_column_list",
        "tplSetId": "changeme",
    }
    PAGE_SIZE: int = 14

    REQUEST_DELAY: tuple[float, float] = (3.0, 8.0)
    MAX_RETRIES: int = 3
    TIMEOUT: int = 30

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