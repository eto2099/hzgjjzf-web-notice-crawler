from bs4 import BeautifulSoup


class DetailParser:
    def parse(self, html: str) -> dict:
        soup = BeautifulSoup(html, "lxml")

        title = self._get_meta(soup, "ArticleTitle")
        publish_date = self._get_meta(soup, "PubDate")
        source = self._get_meta(soup, "ContentSource")
        keywords = self._get_meta(soup, "Keywords")
        description = self._get_meta(soup, "Description")
        article_id = self._get_meta(soup, "extend1")

        content_div = soup.find("div", id="zoom")
        content_html = str(content_div) if content_div else ""
        notice_object, detail_content = self._split_content(content_div)

        return {
            "title": title,
            "publish_date": publish_date,
            "source": source,
            "notice_object": notice_object,
            "detail_content": detail_content,
            "content_html": content_html,
            "keywords": keywords,
            "description": description,
            "article_id": article_id,
        }

    def _split_content(self, content_div) -> tuple[str, str]:
        if not content_div:
            return "", ""
        first_p = content_div.find("p")
        if not first_p:
            return "", content_div.get_text("\n", strip=True)
        notice_object = first_p.get_text(strip=True).rstrip("：:")
        first_p.decompose()
        detail_content = content_div.get_text("\n", strip=True)
        return notice_object, detail_content

    def _get_meta(self, soup: BeautifulSoup, name: str) -> str:
        tag = soup.find("meta", attrs={"name": name})
        return tag.get("content", "").strip() if tag else ""