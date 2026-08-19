import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from loguru import logger

from config import settings
from spider import Spider


def main():
    parser = argparse.ArgumentParser(description="notice crawler")
    parser.add_argument(
        "--date",
        default=None,
        metavar="YYYY-MM-DD",
        help="crawl a specific date; default: latest date (today if available)",
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

    spider = Spider()
    spider.crawl(args.date)


if __name__ == "__main__":
    main()