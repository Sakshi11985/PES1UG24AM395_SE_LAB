"""
House painting quote parser (fixed / hardened version - Lab 7).

Every function now accepts ANY input without crashing.
Invalid input returns None instead of raising an exception.
"""

MAX_INPUT_LENGTH = 1000      # guard against huge inputs (DoS)
MAX_NUMBER_DIGITS = 9        # keeps every number well below Python's int-string limit


def _parse_whole_number(text):
    """
    Returns a non-negative whole number from text, or None if it is not one.
    Only plain ASCII digits 0-9 are accepted, so inputs such as '-5', '+5',
    '1_000', '2.5', superscript digits or non-English digits are rejected.
    """
    if not isinstance(text, str):
        return None
    text = text.strip()
    if not text or len(text) > MAX_NUMBER_DIGITS:
        return None
    if not (text.isascii() and text.isdigit()):
        return None
    return int(text)


def clean_colour_name(name):
    """
    Turns a colour name into a lower-case code, e.g. 'Ocean Blue' -> 'ocean_blue'.
    Returns None for non-string, empty, blank or overly long input.
    """
    if not isinstance(name, str):
        return None
    name = name.strip()
    if not name or len(name) > MAX_INPUT_LENGTH:
        return None
    # split() + join collapses repeated spaces/tabs into a single underscore
    return "_".join(name.lower().split())


def room_area(text):
    """
    Converts 'LENGTHxWIDTH' into an area in square feet, e.g. '12x10' -> 120.
    Returns None unless the input is exactly two positive whole numbers
    separated by a single 'x' or 'X'.
    """
    if not isinstance(text, str) or len(text) > MAX_INPUT_LENGTH:
        return None
    parts = text.lower().split("x")
    if len(parts) != 2:
        return None
    length = _parse_whole_number(parts[0])
    width = _parse_whole_number(parts[1])
    if length is None or width is None or length == 0 or width == 0:
        return None
    return length * width


def total_wall_area(text):
    """
    Adds up wall areas separated by semicolons, e.g. '120;95;110' -> 325.
    Empty entries (e.g. '120;;95' or a trailing ';') are skipped.
    Returns None if the input is not a string, has no valid areas,
    or contains any entry that is not a whole number.
    """
    if not isinstance(text, str) or len(text) > MAX_INPUT_LENGTH:
        return None
    total = 0
    found_any = False
    for part in text.split(";"):
        if part.strip() == "":
            continue                     # skip empty entries
        area = _parse_whole_number(part)
        if area is None:
            return None                  # one bad entry -> whole input invalid
        total += area
        found_any = True
    return total if found_any else None


def main():
    print("==== Running clean_colour_name ====")
    value = input("Enter a paint colour name (e.g. Ocean Blue): ")
    result = clean_colour_name(value)
    print("Colour code:", result if result is not None else "Invalid colour name")

    print("\n==== Running room_area ====")
    value = input("Enter room size as LENGTHxWIDTH in feet (e.g. 12x10): ")
    result = room_area(value)
    print("Room area (sq ft):", result if result is not None else "Invalid room size")

    print("\n==== Running total_wall_area ====")
    value = input("Enter wall areas separated by ; (e.g. 120;95;110): ")
    result = total_wall_area(value)
    print("Total wall area (sq ft):", result if result is not None else "Invalid wall areas")


if __name__ == "__main__":
    main()