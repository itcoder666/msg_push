from msg_push.config import MissingTokenError
from msg_push.pushplus import build_pushplus_payload


def test_build_pushplus_payload_requires_token() -> None:
    try:
        build_pushplus_payload("", "title", "content")
    except MissingTokenError as exc:
        assert "PUSHPLUS_TOKEN" in str(exc)
    else:
        raise AssertionError("Expected MissingTokenError")


def test_build_pushplus_payload_contains_expected_fields() -> None:
    payload = build_pushplus_payload("token-value", "汇率日报", "当前汇率")

    assert payload == {
        "token": "token-value",
        "title": "汇率日报",
        "content": "当前汇率",
    }
