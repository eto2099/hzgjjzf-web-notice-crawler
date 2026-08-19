import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from loguru import logger
from config.settings import settings
from src.spiders.hzgjj_spider import HZGJJSpider


def main():
    parser = argparse.ArgumentParser(description="Hangzhou provident fund crawler")
    parser.add_argument(
        "--date",
        default=None,
        metavar="YYYY-MM-DD",
        help="crawl a specific announcement date; default: latest date (today if available)",
    )
    args = parser.parse_args()

    logger.add(
        "logs/crawl_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        level=settings.LOG_LEVEL,
        encoding="utf-8",
        enqueue=True,
    )
    logger.info(f"{settings.PROJECT_NAME} spider started")
    logger.info(f"target site: {settings.TARGET_URL}")

    spider = HZGJJSpider()
    spider.crawl(args.date)


if __name__ == "__main__":
    main()