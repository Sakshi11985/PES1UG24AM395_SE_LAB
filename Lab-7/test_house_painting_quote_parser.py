from hypothesis import given, settings, strategies as st
from house_painting_quote_parser import clean_colour_name, room_area, total_wall_area

# Extra strategies so Hypothesis reaches the number-parsing code paths,
# not only random text (which almost never looks like "12x10" or "120;95").
number_like = st.text(alphabet="0123456789-+ ._x;X\u00b2\u0663", max_size=20)
any_input = st.text() | st.none() | number_like


@settings(max_examples=300)
@given(any_input)
def test_clean_colour_name_no_crash(s):
    try:
        clean_colour_name(s)
    except Exception as e:
        assert False, f"clean_colour_name crashed on {s!r}: {type(e).__name__}: {e}"


@settings(max_examples=300)
@given(any_input)
def test_room_area_no_crash(s):
    try:
        room_area(s)
    except Exception as e:
        assert False, f"room_area crashed on {s!r}: {type(e).__name__}: {e}"


@settings(max_examples=300)
@given(any_input)
def test_total_wall_area_no_crash(s):
    try:
        total_wall_area(s)
    except Exception as e:
        assert False, f"total_wall_area crashed on {s!r}: {type(e).__name__}: {e}"


# ---- Extra property tests: valid input must still give the correct answer ----

@given(st.integers(min_value=1, max_value=10_000), st.integers(min_value=1, max_value=10_000))
def test_room_area_valid_input_correct(length, width):
    assert room_area(f"{length}x{width}") == length * width
    assert room_area(f"{length}X{width}") == length * width


@given(st.lists(st.integers(min_value=0, max_value=10_000), min_size=1, max_size=10))
def test_total_wall_area_valid_input_correct(areas):
    text = ";".join(str(a) for a in areas)
    assert total_wall_area(text) == sum(areas)


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ", min_size=1))
def test_clean_colour_name_output_format(s):
    result = clean_colour_name(s)
    if s.strip() == "":
        assert result is None
    else:
        assert result == result.lower()
        assert " " not in result