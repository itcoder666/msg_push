from msg_push.config import ConfigError, parse_csv_values, parse_topic_ids


def test_parse_csv_values_strips_empty_values() -> None:
    assert parse_csv_values(" UID_1, ,UID_2 ") == ("UID_1", "UID_2")


def test_parse_topic_ids_returns_integers() -> None:
    assert parse_topic_ids(" 100,200 ") == (100, 200)


def test_parse_topic_ids_rejects_non_integer() -> None:
    try:
        parse_topic_ids("100,abc")
    except ConfigError as exc:
        assert "comma-separated integers" in str(exc)
    else:
        raise AssertionError("Expected ConfigError")
