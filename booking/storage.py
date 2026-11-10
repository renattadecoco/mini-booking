import json
import os
from dataclasses import asdict
from datetime import date

from .models import Booking, Room


class Storage:
    """JSON file storage for rooms and bookings."""

    def __init__(self, path):
        self.path = path
        self.rooms = {}
        self.bookings = []
        self.next_booking_id = 1
        if os.path.exists(path):
            self.load()

    def load(self):
        with open(self.path) as f:
            data = json.load(f)
        self.rooms = {r["id"]: Room(**r) for r in data.get("rooms", [])}
        bookings = []
        for b in data.get("bookings", []):
            b = dict(b)
            if isinstance(b.get("check_in"), str):
                b["check_in"] = date.fromisoformat(b["check_in"])
            if isinstance(b.get("check_out"), str):
                b["check_out"] = date.fromisoformat(b["check_out"])
            bookings.append(Booking(**b))
        self.bookings = bookings
        # Never reuse ids: honour a persisted high-water mark, otherwise
        # derive it from the highest id already stored.
        saved = data.get("next_booking_id")
        highest = max((b.id for b in self.bookings), default=0)
        self.next_booking_id = max(saved or 0, highest + 1, 1)

    def save(self):
        # Keep the high-water mark ahead of every id currently stored.
        highest = max((b.id for b in self.bookings), default=0)
        self.next_booking_id = max(self.next_booking_id, highest + 1, 1)
        bookings = []
        for b in self.bookings:
            d = asdict(b)
            d["check_in"] = b.check_in.isoformat()
            d["check_out"] = b.check_out.isoformat()
            bookings.append(d)
        data = {
            "rooms": [asdict(r) for r in self.rooms.values()],
            "bookings": bookings,
            "next_booking_id": self.next_booking_id,
        }
        with open(self.path, "w") as f:
            json.dump(data, f)
