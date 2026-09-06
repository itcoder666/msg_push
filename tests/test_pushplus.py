from msg_push.pushplus import PushPlusError, build_pushplus_payload


def test_build_pushplus_payload_requires_token() -> None:
    try:
        build_pushplus_payload("", "title", "content")
    except PushPlusError as exc:
        assert "PUSHPLUS_TOKEN" in str(exc)
    else:
        raise AssertionError("Expected PushPlusError")


def test_build_pushplus_payload_contains_expected_fields() -> None:
    payload = build_pushplus_payload("token-value", "汇率日报", "当前汇率")

    assert payload == {
        "token": "token-value",
        "title": "汇率日报",
        "content": "当前汇率",
    }


def test_build_pushplus_payload_includes_topic_for_group() -> None:
    payload = build_pushplus_payload(
        "token-value",
        "汇率日报",
        "当前汇率",
        topic="group-code",
    )

    assert payload == {
        "token": "token-value",
        "title": "汇率日报",
        "content": "当前汇率",
        "topic": "group-code",
    }
