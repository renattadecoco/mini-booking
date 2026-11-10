from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP


def quote(room, check_in, check_out):
    """Return the total price for a stay as a Decimal rounded to 2 places (ROUND_HALF_UP).

    - Each night costs room.base_rate.
    - A night that starts on a Friday or Saturday costs base_rate * 1.25.
    - Stays of 7 nights or more get 10% off the total.
    - Raise ValueError if check_out <= check_in.
    """
    if check_out <= check_in:
        raise ValueError("check_out must be after check_in")
    rate = Decimal(room.base_rate)
    total = Decimal("0")
    nights = 0
    day = check_in
    while day < check_out:
        if day.weekday() in (4, 5):  # Friday, Saturday
            total += rate * Decimal("1.25")
        else:
            total += rate
        nights += 1
        day += timedelta(days=1)
    if nights >= 7:
        total *= Decimal("0.90")
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
