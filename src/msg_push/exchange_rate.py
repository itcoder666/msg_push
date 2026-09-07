from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.error import URLError
from urllib.request import Request, urlopen

SINA_REFERER = "https://finance.sina.com.cn/"
USER_AGENT = "Mozilla/5.0"


@dataclass(frozen=True)
class ExchangeRate:
    symbol: str
    rate: float
    source_time: str | None = None
    source_date: str | None = None


def parse_sina_usdcny_response(body: str) -> ExchangeRate:
    match = re.search(r"var\s+hq_str_(?P<symbol>\w+)=\"(?P<data>[^\"]*)\";?", body)
    if not match:
        raise ValueError(f"Unexpected Sina response format: {body!r}")

    fields = match.group("data").split(",")
    if len(fields) < 17:
        raise ValueError(f"Sina response has insufficient fields: {fields!r}")

    try:
        rate = float(fields[8])
    except ValueError as exc:
        raise ValueError(f"Invalid USD/CNY rate value: {fields[3]!r}") from exc

    source_time = fields[0] or None
    source_date = fields[-1] if fields and fields[-1] else None
    return ExchangeRate(
        symbol=match.group("symbol"),
        rate=rate,
        source_time=source_time,
        source_date=source_date,
    )


def fetch_usdcny_rate(url: str, timeout: int = 10) -> ExchangeRate:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Referer": SINA_REFERER,
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("gbk", errors="ignore")
    except URLError as exc:
        raise RuntimeError(f"Failed to fetch USD/CNY exchange rate: {exc}") from exc

    return parse_sina_usdcny_response(body)
