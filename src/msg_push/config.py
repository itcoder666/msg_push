from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_EXCHANGE_RATE_URL = "https://hq.sinajs.cn/list=fx_susdcny"
DEFAULT_PUSHPLUS_URL = "https://www.pushplus.plus/send"


@dataclass(frozen=True)
class Settings:
    pushplus_token: str | None
    exchange_rate_url: str = DEFAULT_EXCHANGE_RATE_URL
    pushplus_url: str = DEFAULT_PUSHPLUS_URL


class MissingTokenError(RuntimeError):
    """Raised when PushPlus token is not configured."""


def load_settings() -> Settings:
    return Settings(
        pushplus_token=os.environ.get("PUSHPLUS_TOKEN"),
        exchange_rate_url=os.environ.get(
            "SINA_EXCHANGE_URL",
            DEFAULT_EXCHANGE_RATE_URL,
        ),
        pushplus_url=os.environ.get("PUSHPLUS_URL", DEFAULT_PUSHPLUS_URL),
    )
