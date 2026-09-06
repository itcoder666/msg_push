from msg_push.wxpusher import WxPusherError, build_wxpusher_payload


def test_build_wxpusher_payload_supports_uids() -> None:
    payload = build_wxpusher_payload(
        app_token="app-token",
        summary="汇率日报",
        content="当前汇率",
        uids=("UID_1", "UID_2"),
    )

    assert payload == {
        "appToken": "app-token",
        "summary": "汇率日报",
        "content": "当前汇率",
        "contentType": 1,
        "uids": ["UID_1", "UID_2"],
    }


def test_build_wxpusher_payload_supports_topic_ids() -> None:
    payload = build_wxpusher_payload(
        app_token="app-token",
        summary="汇率日报",
        content="当前汇率",
        topic_ids=(100, 200),
    )

    assert payload == {
        "appToken": "app-token",
        "summary": "汇率日报",
        "content": "当前汇率",
        "contentType": 1,
        "topicIds": [100, 200],
    }


def test_build_wxpusher_payload_supports_uids_and_topic_ids() -> None:
    payload = build_wxpusher_payload(
        app_token="app-token",
        summary="汇率日报",
        content="当前汇率",
        uids=("UID_1",),
        topic_ids=(100,),
    )

    assert payload["uids"] == ["UID_1"]
    assert payload["topicIds"] == [100]


def test_build_wxpusher_payload_requires_recipient() -> None:
    try:
        build_wxpusher_payload(
            app_token="app-token",
            summary="汇率日报",
            content="当前汇率",
        )
    except WxPusherError as exc:
        assert "WXPUSHER_UIDS or WXPUSHER_TOPIC_IDS" in str(exc)
    else:
        raise AssertionError("Expected WxPusherError")
