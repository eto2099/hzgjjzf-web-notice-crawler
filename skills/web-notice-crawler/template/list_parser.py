from bs4 import BeautifulSoup


class ListParser:
    def parse(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "lxml")
        items = []
        for li in soup.select("li"):
            a_tag = li.find("a")
            span_tag = li.find("span")
            if not a_tag:
                continue
            title = a_tag.get("title", "").strip()
            href = a_tag.get("href", "").strip()
            date_text = span_tag.get_text(strip=True) if span_tag else ""
            date = date_text.strip("[]")
            items.append({
                "title": title,
                "url": href,
                "date": date,
            })
        return items