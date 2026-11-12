from hypothesis import given, strategies as st

from credit_card_rewards_parser import (
    mask_card_number,
    parse_statement_total,
    parse_transaction,
)


FUZZ_VALUES = st.one_of(
    st.none(),
    st.text(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.binary(),
    st.lists(st.text(max_size=8), max_size=3),
    st.dictionaries(st.text(max_size=5), st.integers(), max_size=3),
)


@given(FUZZ_VALUES)
def test_mask_card_number_no_crash(value):
    try:
        result = mask_card_number(value)
    except Exception as exc:
        assert False, f"mask_card_number crashed for {value!r}: {type(exc).__name__}: {exc}"
    assert isinstance(result, str)


@given(FUZZ_VALUES)
def test_parse_transaction_no_crash(value):
    try:
        result = parse_transaction(value)
    except Exception as exc:
        assert False, f"parse_transaction crashed for {value!r}: {type(exc).__name__}: {exc}"
    assert isinstance(result, tuple) and len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], int)


@given(FUZZ_VALUES)
def test_parse_statement_total_no_crash(value):
    try:
        result = parse_statement_total(value)
    except Exception as exc:
        assert False, f"parse_statement_total crashed for {value!r}: {type(exc).__name__}: {exc}"
    assert isinstance(result, int)


def test_valid_inputs_keep_expected_results():
    assert mask_card_number("4111 1111 1111 1234") == "************1234"
    assert parse_transaction("2026-11-05,Dining,1550") == ("dining", 1550)
    assert parse_statement_total("Total: 12,500") == 12500

