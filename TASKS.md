# Tasks

Rules: do not change anything in `tests/`. No third-party dependencies. Keep module names and public
function/class names as they are. Open one pull request per task (or one branch per task if PRs are not possible).

1. **Storage round-trip** (`booking/storage.py`): saving and reloading must keep bookings intact
   (dates stay `datetime.date`). Cancellations must be persisted.
2. **Booking rules** (`booking/service.py`): back-to-back stays are allowed (check-out day = next check-in day);
   reject unknown rooms, `check_out <= check_in`, and guests above room capacity with `BookingError`;
   `cancel` of an unknown id raises `BookingError`; booking ids must never be reused, also after cancel + reload.
3. **Availability search** (`BookingService.available_rooms`): sorted room ids free for the whole range and big enough.
4. **Pricing** (`booking/pricing.py`): implement `quote` following its docstring.
5. **CLI** (`booking/cli.py`): add the `available` and `quote` commands and the error handling described in `tests/test_cli.py`.

Finish with a short CHANGES.md (what changed per task) and the full test output.
