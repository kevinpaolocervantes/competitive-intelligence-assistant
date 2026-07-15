from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

USER_AGENT = "PMM-Competitive-Intelligence-Assistant/0.1"


@dataclass(frozen=True)
class PageSnapshot:
    url: str
    title: str
    text: str
    captured_at: str
    content_hash: str

    def to_dict(self) -> dict[str, str]:
        return {
            "url": self.url,
            "title": self.title,
            "text": self.text,
            "captured_at": self.captured_at,
            "content_hash": self.content_hash,
        }


def _clean_text(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "nav", "footer"]):
        tag.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else "Untitled"
    text = "\n".join(
        line.strip()
        for line in soup.get_text("\n").splitlines()
        if line.strip()
    )
    return title, text[:60_000]


def fetch_page(url: str, timeout: int = 20) -> PageSnapshot:
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=timeout,
        allow_redirects=True,
    )
    response.raise_for_status()
    title, text = _clean_text(response.text)
    return PageSnapshot(
        url=response.url,
        title=title,
        text=text,
        captured_at=datetime.now(timezone.utc).isoformat(),
        content_hash=hashlib.sha256(text.encode("utf-8")).hexdigest(),
    )


def discover_same_domain_links(base_url: str, html: str, limit: int = 5) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    base_domain = urlparse(base_url).netloc
    found: list[str] = []
    for anchor in soup.find_all("a", href=True):
        absolute = urljoin(base_url, anchor["href"]).split("#")[0]
        parsed = urlparse(absolute)
        if parsed.scheme in {"http", "https"} and parsed.netloc == base_domain:
            if absolute not in found:
                found.append(absolute)
        if len(found) >= limit:
            break
    return found


def crawl_urls(urls: Iterable[str]) -> list[PageSnapshot]:
    snapshots: list[PageSnapshot] = []
    for url in urls:
        snapshots.append(fetch_page(url.strip()))
    return snapshots
