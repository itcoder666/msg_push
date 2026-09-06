from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from msg_push.config import MissingNotificationChannelError, Settings
from msg_push.pushplus import PushPlusError, send_pushplus_message
from msg_push.wechat_work import WeChatWorkError, send_wechat_work_message
from msg_push.wxpusher import WxPusherError, send_wxpusher_message


@dataclass(frozen=True)
class NotificationResult:
    channel: str
    success: bool
    error: str | None = None


class NotificationDeliveryError(RuntimeError):
    """Raised when one or more configured notification channels fail."""

    def __init__(self, results: list[NotificationResult]) -> None:
        self.results = results
        failed_channels = ", ".join(
            result.channel for result in results if not result.success
        )
        super().__init__(f"Notification delivery failed for: {failed_channels}")


def _send_channel(channel: str, send: Callable[[], object]) -> NotificationResult:
    try:
        send()
    except (PushPlusError, WeChatWorkError, WxPusherError) as exc:
        return NotificationResult(channel=channel, success=False, error=str(exc))

    return NotificationResult(channel=channel, success=True)


def send_configured_notifications(
    settings: Settings,
    *,
    title: str,
    content: str,
) -> list[NotificationResult]:
    tasks: list[tuple[str, Callable[[], object]]] = []

    if settings.pushplus_token:
        tasks.append(
            (
                "PushPlus",
                lambda: send_pushplus_message(
                    token=settings.pushplus_token or "",
                    title=title,
                    content=content,
                    url=settings.pushplus_url,
                ),
            )
        )

    if settings.wechat_work_webhook_url:
        tasks.append(
            (
                "WeChat Work",
                lambda: send_wechat_work_message(
                    webhook_url=settings.wechat_work_webhook_url or "",
                    content=f"{title}\n{content}",
                ),
            )
        )

    if settings.wxpusher_app_token and (
        settings.wxpusher_uids or settings.wxpusher_topic_ids
    ):
        tasks.append(
            (
                "WxPusher",
                lambda: send_wxpusher_message(
                    app_token=settings.wxpusher_app_token or "",
                    summary=title,
                    content=content,
                    uids=settings.wxpusher_uids,
                    topic_ids=settings.wxpusher_topic_ids,
                    url=settings.wxpusher_url,
                ),
            )
        )

    if not tasks:
        raise MissingNotificationChannelError("No notification channel is configured")

    results = [_send_channel(channel, send) for channel, send in tasks]
    if any(not result.success for result in results):
        raise NotificationDeliveryError(results)

    return results
