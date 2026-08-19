import json
from datetime import datetime
from typing import Optional

from loguru import logger

from config import settings
from base import BaseSpider
from list_parser import ListParser
from detail_parser import DetailParser
from storage import StoragePipeline


class Spider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.list_parser = ListParser()
        self.detail_parser = DetailParser()
        self.pipeline = StoragePipeline()
        self.seen_urls = set()

    def crawl(self, target_date: Optional[str] = None):
        logger.info("start crawling notices")
        if target_date:
            try:
                datetime.strptime(target_date, "%Y-%m-%d")
            except ValueError:
                logger.error(
                    f"invalid target date: {target_date}, expected YYYY-MM-DD"
                )
                return
            logger.info(f"target date specified: {target_date}")

        last_date = self.pipeline.load_last_date()
        logger.info(f"last crawl date: {last_date or 'none'}")

        first_items = self._fetch_page(1)
        if not first_items:
            logger.info("list has no data, crawl finished")
            self.pipeline.close()
            return

        if target_date:
            latest_date = target_date
        else:
            latest_date = self._latest_date(first_items)
            if not latest_date:
                logger.info("failed to parse list date, crawl finished")
                self.pipeline.close()
                return

            today = datetime.now().strftime("%Y-%m-%d")
            if latest_date < today:
                logger.info(
                    f"no data for today ({today}), "
                    f"fall back to latest notice date: {latest_date}"
                )
            logger.info(f"list latest date: {latest_date}")
            if last_date and latest_date <= last_date:
                logger.info(
                    f"latest date {latest_date} not newer than last crawl date "
                    f"{last_date}, skip"
                )
                self.pipeline.close()
                return

        page = 1
        reached_target = False
        stopped = False
        processed = 0
        while not stopped:
            logger.info(f"crawling page {page}")
            items = self._fetch_page(page)
            if not items:
                logger.info(f"page {page} has no data, crawl finished")
                break

            page_has_target = False
            for item in items:
                item_date = (item.get("date") or "")[:10]
                if item_date > latest_date:
                    continue
                if item_date == latest_date:
                    if self._should_skip(item):
                        logger.info("encountered duplicate/empty URL, crawl finished")
                        stopped = True
                        break
                    self._process_item(item)
                    reached_target = True
                    page_has_target = True
                    processed += 1
                else:
                    logger.info(
                        f"encountered earlier date {item_date or 'empty'}, crawl finished"
                    )
                    stopped = True
                    break

            if stopped:
                break
            if page_has_target:
                page += 1
            elif reached_target:
                logger.info(f"no more items for date {latest_date}, crawl finished")
                break
            else:
                page += 1

        if not target_date:
            self.pipeline.save_last_date(latest_date)
        self.pipeline.close()
        logger.info(f"crawl finished, processed {processed} notices")

    def _latest_date(self, items: list[dict]) -> Optional[str]:
        dates = [(item.get("date") or "")[:10] for item in items if item.get("date")]
        return max(dates) if dates else None

    def _fetch_page(self, page: int) -> list[dict]:
        params = {
            **settings.LIST_API_PARAMS,
            "paramJson": json.dumps(
                {
                    "pageNo": page,
                    "pageSize": settings.PAGE_SIZE,
                    "search": "",
                },
                ensure_ascii=False,
            ),
        }
        data = self.request(settings.LIST_API_PATH, params=params)
        if not data or not data.get("success"):
            return []
        html = data.get("data", {}).get("html", "")
        return self.list_parser.parse(html)

    def _should_skip(self, item: dict) -> bool:
        url = item.get("url", "")
        if not url or url in self.seen_urls:
            return True
        self.seen_urls.add(url)
        return False

    def _process_item(self, item: dict):
        detail = self._fetch_detail(item["url"])
        if not detail:
            return
        record = {**item, **detail}
        self.pipeline.save(record)
        logger.info(f"saved: {record.get('title')} ({record.get('publish_date')})")

    def _fetch_detail(self, relative_url: str) -> Optional[dict]:
        html = self.request_html(relative_url)
        if not html:
            return None
        return self.detail_parser.parse(html)