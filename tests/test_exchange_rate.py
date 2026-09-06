from msg_push.exchange_rate import parse_sina_usdcny_response


def test_parse_sina_usdcny_response_extracts_latest_rate() -> None:
    body = (
        'var hq_str_fx_susdcny="02:56:38,6.7103000000,6.7113000000,'
        '6.7108000000,195.0000000000,6.7176000000,6.7187000000,'
        '6.6992000000,6.7108000000,在岸人民币,0.0000,0.0000,0.0195,'
        '美元人民币,0.0000,0.0000,,2026-09-05";'
    )

    rate = parse_sina_usdcny_response(body)

    assert rate.symbol == "fx_susdcny"
    assert rate.rate == 6.7108
    assert rate.source_time == "02:56:38"
    assert rate.source_date == "2026-09-05"


def test_parse_sina_usdcny_response_rejects_invalid_format() -> None:
    try:
        parse_sina_usdcny_response("unexpected")
    except ValueError as exc:
        assert "Unexpected Sina response format" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_parse_sina_usdcny_response_rejects_invalid_rate() -> None:
    body = 'var hq_str_fx_susdcny="02:56:38,6.7103,6.7113,not-a-number";'

    try:
        parse_sina_usdcny_response(body)
    except ValueError as exc:
        assert "Invalid USD/CNY rate value" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
