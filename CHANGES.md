# CHANGES

## Task 1 — Storage round-trip (`booking/storage.py`)
- Save booking dates as ISO strings instead of raw `date` objects, so JSON
  saving no longer fails; load parses them back with `date.fromisoformat`,
  so reloaded bookings keep `datetime.date` dates.
- Persist a `next_booking_id` high-water mark in the JSON file (derived from
  the highest stored id when the field is absent), so ids are never reused
  after a reload.

## Task 2 — Booking rules (`booking/service.py`)
- Overlap is now half-open (`[check_in, check_out)`), so back-to-back stays
  (check-out day = next check-in day) are allowed while real overlaps are
  still rejected.
- `book` now raises `BookingError` for an unknown room, `check_out <=
  check_in`, and guests above the room's capacity, before checking
  availability.
- `cancel` of an unknown id raises `BookingError` and a successful cancel
  is now persisted with `storage.save()`.
- Booking ids come from the storage high-water mark (`next_booking_id`)
  instead of `len(bookings) + 1`, so ids are never reused after a cancel,
  including after a reload.

## Task 3 — Availability search (`booking/service.py`)
- Implemented `available_rooms`: returns sorted room ids that are free for
  the whole `[check_in, check_out)` range and have `capacity >= guests`.

## Task 4 — Pricing (`booking/pricing.py`)
- Implemented `quote` per its docstring: each night costs `base_rate`,
  nights starting Friday or Saturday cost `base_rate * 1.25`, stays of 7+
  nights get 10% off the total, `ValueError` if `check_out <= check_in`,
  and the result is a `Decimal` rounded to 2 places with `ROUND_HALF_UP`.

## Task 5 — CLI (`booking/cli.py`)
- Added the `available` command (prints one free room id per line, nothing
  when none are free; `--guests` filter) and the `quote` command (prints
  the total with 2 decimal places).
- Added error handling: `BookingError` and `ValueError` (including bad
  ISO dates and unknown rooms) print `error: <message>` and return exit
  code 1 instead of raising.
