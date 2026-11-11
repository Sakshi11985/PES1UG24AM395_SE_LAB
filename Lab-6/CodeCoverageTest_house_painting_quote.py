import pytest
from house_painting_quote import painting_quote, paint_litres, crew_days


# ---------- painting_quote ----------
def test_exterior_enamel():
    assert painting_quote("enamel", 500, 2, True) == 32500


def test_unknown_paint():
    with pytest.raises(ValueError, match="unknown paint"):
        painting_quote("gloss", 500, 1, False)


def test_invalid_area():
    with pytest.raises(ValueError, match="invalid job"):
        painting_quote("emulsion", 0, 1, False)


def test_distemper_exterior_rejected():
    with pytest.raises(ValueError, match="interiors only"):
        painting_quote("distemper", 500, 1, True)


def test_large_area_discount():
    # 3000 * 20 * 1 = 60000, 10% off -> 54000
    assert painting_quote("emulsion", 3000, 1, False) == 54000


def test_minimum_charge_applied():
    # 100 * 12 * 1 = 1200 < 5000 -> minimum quote
    assert painting_quote("distemper", 100, 1, False) == 5000


def test_interior_normal_quote():
    # 500 * 20 * 2 = 20000 (no exterior surcharge, no discount, above minimum)
    assert painting_quote("emulsion", 500, 2, False) == 20000


# ---------- paint_litres ----------
def test_smooth_litres():
    assert paint_litres(200, 1, "smooth") == 2


def test_rough_litres_rounds_up():
    # 130 sqft * 1 coat / 60 = 2 remainder 10 -> 3 litres
    assert paint_litres(130, 1, "rough") == 3


def test_unknown_surface():
    with pytest.raises(ValueError, match="unknown surface"):
        paint_litres(100, 1, "glossy")


# ---------- crew_days ----------
def test_crew_days_with_wallpaper_removal():
    # per_day = 800, 1000 -> 1 full day + 1 partial = 2, +2 for wallpaper = 4
    assert crew_days(1000, 2, True) == 4


def test_crew_days_exact_no_wallpaper():
    # 800 sqft / 800 per day = exactly 1 day
    assert crew_days(800, 2, False) == 1


def test_crew_days_no_painters():
    with pytest.raises(ValueError, match="at least one painter"):
        crew_days(500, 0, False)
