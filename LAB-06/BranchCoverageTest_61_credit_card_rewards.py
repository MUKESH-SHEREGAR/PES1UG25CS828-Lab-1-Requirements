"""Tests each true and false outcome of the module's decision branches."""

import pytest

from credit_card_rewards import card_status, late_payment_fee, reward_points


@pytest.mark.parametrize("tier", ["classic", "gold", "platinum"])
def test_valid_card_tier_branch(tier):
    assert reward_points(tier, 100, "other", False) >= 0


def test_unknown_tier_branch():
    with pytest.raises(ValueError, match="unknown card tier"):
        reward_points("silver", 100, "other", False)


@pytest.mark.parametrize("amount", [-1, 0])
def test_nonpositive_amount_branch(amount):
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("classic", amount, "other", False)


@pytest.mark.parametrize("category", ["fuel", "grocery", "dining", "travel"])
def test_category_branches(category):
    result = reward_points("gold", 500, category, False)
    assert result == {"fuel": 0, "grocery": 10, "dining": 20, "travel": 20}[category]


@pytest.mark.parametrize("weekend,tier,expected", [
    (True, "gold", 60),
    (False, "gold", 10),
    (True, "classic", 5),
])
def test_weekend_and_tier_bonus_decisions(weekend, tier, expected):
    assert reward_points(tier, 500, "other", weekend) == expected


@pytest.mark.parametrize("outstanding,days,expected", [
    (0, 1, 0),       # outstanding <= 0 is true
    (500, 0, 0),     # days_late <= 0 is true
    (500, 1, 100),   # fee <= 1000 true, > 30 false
    (1000, 31, 850), # first boundary true, > 30 true
    (1001, 1, 500),  # first threshold false, second true
    (10000, 31, 1250),
    (10001, 1, 1000), # both thresholds false
    (20000, 31, 1750),
])
def test_fee_boolean_and_threshold_branches(outstanding, days, expected):
    assert late_payment_fee(outstanding, days) == expected


@pytest.mark.parametrize("utilisation,missed,frozen,expected", [
    (0, 0, True, "frozen"),
    (0, 3, False, "blocked"),
    (91, 0, False, "over limit risk"),
    (90, 0, False, "watch"), # > 90 false, > 30 true
    (0, 1, False, "watch"),  # > 30 false, missed > 0 true
    (0, 0, False, "good"),   # both sides of OR false
    (30, 0, False, "good"),
])
def test_card_status_decision_paths(utilisation, missed, frozen, expected):
    assert card_status(utilisation, missed, frozen) == expected
