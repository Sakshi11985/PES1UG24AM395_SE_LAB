import pytest
from house_painting_quote import painting_quote, paint_litres, crew_days


# ================= painting_quote =================
def test_exterior_enamel():
    # exterior surcharge branch TRUE
    assert painting_quote("enamel", 500, 2, True) == 32500


def test_interior_no_surcharge():
    # is_exterior FALSE branch
    assert painting_quote("emulsion", 500, 2, False) == 20000


def test_unknown_paint():
    with pytest.raises(ValueError, match="unknown paint"):
        painting_quote("gloss", 500, 1, False)


def test_zero_area():
    # first operand of `area_sqft <= 0 or coats < 1`
    with pytest.raises(ValueError, match="invalid job"):
        painting_quote("emulsion", 0, 1, False)


def test_negative_area():
    with pytest.raises(ValueError, match="invalid job"):
        painting_quote("emulsion", -10, 1, False)


def test_zero_coats():
    # second operand: area is valid, coats < 1
    with pytest.raises(ValueError, match="invalid job"):
        painting_quote("emulsion", 500, 0, False)


def test_distemper_exterior_rejected():
    with pytest.raises(ValueError, match="interiors only"):
        painting_quote("distemper", 500, 1, True)


def test_distemper_interior_allowed():
    # exterior False + distemper -> must NOT raise
    assert painting_quote("distemper", 500, 1, False) == 6000


def test_exterior_non_distemper_allowed():
    # exterior True + not distemper -> must NOT raise
    assert painting_quote("emulsion", 500, 1, True) == 12500


def test_discount_applies_above_2000():
    # 3000 * 20 = 60000, minus 10% -> 54000
    assert painting_quote("emulsion", 3000, 1, False) == 54000


def test_no_discount_at_exactly_2000():
    # boundary: area_sqft > 2000 is FALSE at 2000
    assert painting_quote("emulsion", 2000, 1, False) == 40000


def test_discount_just_above_boundary():
    # 2001 * 20 = 40020, 40020 // 10 = 4002, 40020 - 4002 = 36018
    assert painting_quote("emulsion", 2001, 1, False) == 36018


def test_minimum_charge_when_below_5000():
    assert painting_quote("distemper", 100, 1, False) == 5000


def test_cost_exactly_5000_not_bumped():
    # boundary: cost < 5000 is FALSE at 5000 (250 * 20 = 5000)
    assert painting_quote("emulsion", 250, 1, False) == 5000


def test_cost_just_above_5000():
    # 251 * 20 = 5020 -> returned as-is
    assert painting_quote("emulsion", 251, 1, False) == 5020


def test_cost_just_below_5000():
    # 249 * 20 = 4980 -> bumped to 5000
    assert painting_quote("emulsion", 249, 1, False) == 5000


# ================= paint_litres =================
def test_smooth_exact_litres():
    # smooth branch, no remainder
    assert paint_litres(200, 1, "smooth") == 2


def test_smooth_rounds_up():
    # smooth branch, remainder -> +1
    assert paint_litres(250, 1, "smooth") == 3


def test_rough_exact_litres():
    # rough branch, no remainder (120 / 60 = 2)
    assert paint_litres(120, 1, "rough") == 2


def test_rough_rounds_up():
    # rough branch, remainder -> +1
    assert paint_litres(130, 1, "rough") == 3


def test_multiple_coats_litres():
    assert paint_litres(100, 3, "smooth") == 3


def test_unknown_surface():
    with pytest.raises(ValueError, match="unknown surface"):
        paint_litres(100, 1, "glossy")


# ================= crew_days =================
def test_crew_days_exact_division():
    # remainder 0 branch, no wallpaper
    assert crew_days(800, 2, False) == 1


def test_crew_days_partial_day_rounds_up():
    # remainder != 0 branch, no wallpaper
    assert crew_days(1000, 2, False) == 2


def test_crew_days_wallpaper_adds_two():
    # wallpaper branch TRUE
    assert crew_days(800, 2, True) == 3


def test_crew_days_partial_with_wallpaper():
    assert crew_days(1000, 2, True) == 4


def test_crew_days_no_painters():
    with pytest.raises(ValueError, match="at least one painter"):
        crew_days(500, 0, False)


def test_crew_days_negative_painters():
    with pytest.raises(ValueError, match="at least one painter"):
        crew_days(500, -1, False)
