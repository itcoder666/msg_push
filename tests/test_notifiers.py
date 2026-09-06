import msg_push.notifiers as notifiers
from msg_push.config import DEFAULT_PUSHPLUS_URL, DEFAULT_WXPUSHER_URL, Settings
from msg_push.notifiers import (
    MissingNotificationChannelError,
    NotificationDeliveryError,
    send_configured_notifications,
)
from msg_push.pushplus import PushPlusError


def make_settings(**overrides: object) -> Settings:
    values = {
        "pushplus_token": None,
        "pushplus_topic": None,
        "wechat_work_webhook_url": None,
        "wxpusher_app_token": None,
        "wxpusher_uids": (),
        "wxpusher_topic_ids": (),
        "pushplus_url": DEFAULT_PUSHPLUS_URL,
        "wxpusher_url": DEFAULT_WXPUSHER_URL,
    }
    values.update(overrides)
    return Settings(**values)


def test_send_configured_notifications_requires_at_least_one_channel() -> None:
    try:
        send_configured_notifications(make_settings(), title="title", content="content")
    except MissingNotificationChannelError as exc:
        assert "No notification channel" in str(exc)
    else:
        raise AssertionError("Expected MissingNotificationChannelError")


def test_send_configured_notifications_only_sends_configured_channels(
    monkeypatch,
) -> None:
    sent_channels = []

    def fake_pushplus(**kwargs):
        sent_channels.append(("pushplus", kwargs["title"], kwargs["content"]))

    monkeypatch.setattr(notifiers, "send_pushplus_message", fake_pushplus)

    results = send_configured_notifications(
        make_settings(pushplus_token="token"),
        title="汇率日报",
        content="当前汇率",
    )

    assert sent_channels == [("pushplus", "汇率日报", "当前汇率")]
    assert [(result.channel, result.success) for result in results] == [
        ("PushPlus", True)
    ]


def test_send_configured_notifications_sends_all_configured_channels(
    monkeypatch,
) -> None:
    sent_channels = []

    def fake_pushplus(**kwargs):
        sent_channels.append(("pushplus", kwargs["token"]))

    def fake_wechat_work(**kwargs):
        sent_channels.append(("wechat_work", kwargs["webhook_url"]))

    def fake_wxpusher(**kwargs):
        sent_channels.append(("wxpusher", kwargs["uids"], kwargs["topic_ids"]))

    monkeypatch.setattr(notifiers, "send_pushplus_message", fake_pushplus)
    monkeypatch.setattr(notifiers, "send_wechat_work_message", fake_wechat_work)
    monkeypatch.setattr(notifiers, "send_wxpusher_message", fake_wxpusher)

    results = send_configured_notifications(
        make_settings(
            pushplus_token="pushplus-token",
            wechat_work_webhook_url="https://example.test/webhook",
            wxpusher_app_token="wxpusher-token",
            wxpusher_uids=("UID_1",),
            wxpusher_topic_ids=(100,),
        ),
        title="汇率日报",
        content="当前汇率",
    )

    assert sent_channels == [
        ("pushplus", "pushplus-token"),
        ("wechat_work", "https://example.test/webhook"),
        ("wxpusher", ("UID_1",), (100,)),
    ]
    assert all(result.success for result in results)


def test_send_configured_notifications_continues_after_channel_failure(
    monkeypatch,
) -> None:
    sent_channels = []

    def fake_pushplus(**kwargs):
        sent_channels.append("pushplus")
        raise PushPlusError("boom")

    def fake_wechat_work(**kwargs):
        sent_channels.append("wechat_work")

    monkeypatch.setattr(notifiers, "send_pushplus_message", fake_pushplus)
    monkeypatch.setattr(notifiers, "send_wechat_work_message", fake_wechat_work)

    try:
        send_configured_notifications(
            make_settings(
                pushplus_token="pushplus-token",
                wechat_work_webhook_url="https://example.test/webhook",
            ),
            title="汇率日报",
            content="当前汇率",
        )
    except NotificationDeliveryError as exc:
        assert sent_channels == ["pushplus", "wechat_work"]
        assert [(result.channel, result.success) for result in exc.results] == [
            ("PushPlus", False),
            ("WeChat Work", True),
        ]
    else:
        raise AssertionError("Expected NotificationDeliveryError")
