from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_EXCHANGE_RATE_URL = "https://hq.sinajs.cn/list=fx_susdcny"
DEFAULT_PUSHPLUS_URL = "https://www.pushplus.plus/send"
DEFAULT_WXPUSHER_URL = "https://wxpusher.zjiecode.com/api/send/message"


class ConfigError(RuntimeError):
    """Raised when notification configuration is invalid."""


@dataclass(frozen=True)
class Settings:
    pushplus_token: str | None
    wechat_work_webhook_url: str | None
    wxpusher_app_token: str | None
    wxpusher_uids: tuple[str, ...]
    wxpusher_topic_ids: tuple[int, ...]
    exchange_rate_url: str = DEFAULT_EXCHANGE_RATE_URL
    pushplus_url: str = DEFAULT_PUSHPLUS_URL
    wxpusher_url: str = DEFAULT_WXPUSHER_URL


class MissingNotificationChannelError(ConfigError):
    """Raised when no notification channel is configured."""


def parse_csv_values(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()

    return tuple(part.strip() for part in value.split(",") if part.strip())


def parse_topic_ids(value: str | None) -> tuple[int, ...]:
    topic_ids = []
    for raw_topic_id in parse_csv_values(value):
        try:
            topic_ids.append(int(raw_topic_id))
        except ValueError as exc:
            raise ConfigError(
                "WXPUSHER_TOPIC_IDS must be comma-separated integers"
            ) from exc

    return tuple(topic_ids)


def load_settings() -> Settings:
    return Settings(
        pushplus_token=os.environ.get("PUSHPLUS_TOKEN"),
        wechat_work_webhook_url=os.environ.get("WECHAT_WORK_WEBHOOK_URL"),
        wxpusher_app_token=os.environ.get("WXPUSHER_APP_TOKEN"),
        wxpusher_uids=parse_csv_values(os.environ.get("WXPUSHER_UIDS")),
        wxpusher_topic_ids=parse_topic_ids(os.environ.get("WXPUSHER_TOPIC_IDS")),
        exchange_rate_url=os.environ.get(
            "SINA_EXCHANGE_URL",
            DEFAULT_EXCHANGE_RATE_URL,
        ),
        pushplus_url=os.environ.get("PUSHPLUS_URL", DEFAULT_PUSHPLUS_URL),
        wxpusher_url=os.environ.get("WXPUSHER_URL", DEFAULT_WXPUSHER_URL),
    )
