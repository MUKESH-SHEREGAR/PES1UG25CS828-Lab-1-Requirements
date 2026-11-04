"""Tests chosen to execute every source line in credit_card_rewards."""

import pytest

from credit_card_rewards import card_status, late_payment_fee, reward_points


def test_reward_points_for_all_tiers_and_categories():
    assert reward_points("classic", 1000, "grocery", False) == 10
    assert reward_points("gold", 999, "grocery", False) == 18
    assert reward_points("platinum", 500, "dining", False) == 40
    assert reward_points("gold", 500, "travel", False) == 20
    assert reward_points("platinum", 1000, "fuel", True) == 0
    assert reward_points("gold", 1000, "grocery", True) == 70
    assert reward_points("classic", 1000, "grocery", True) == 10


@pytest.mark.parametrize("tier,amount,message", [
    ("silver", 100, "unknown card tier"),
    ("classic", 0, "invalid amount"),
    ("gold", -1, "invalid amount"),
])
def test_reward_points_reject_invalid_inputs(tier, amount, message):
    with pytest.raises(ValueError, match=message):
        reward_points(tier, amount, "grocery", False)


def test_late_payment_fees():
    assert late_payment_fee(5000, 0) == 0
    assert late_payment_fee(5000, 5) == 500
    assert late_payment_fee(500, 1) == 100
    assert late_payment_fee(10000, 31) == 1250
    assert late_payment_fee(10001, 31) == 1750
    assert late_payment_fee(0, 5) == 0


def test_card_statuses():
    assert card_status(0, 0, True) == "frozen"
    assert card_status(0, 3, False) == "blocked"
    assert card_status(91, 0, False) == "over limit risk"
    assert card_status(31, 0, False) == "watch"
    assert card_status(0, 1, False) == "watch"
    assert card_status(30, 0, False) == "good"
