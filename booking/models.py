from dataclasses import dataclass
from datetime import date


@dataclass
class Room:
    id: str
    name: str
    base_rate: str  # price per night as a decimal string, e.g. "100.00"
    capacity: int


@dataclass
class Booking:
    id: int
    room_id: str
    guest: str
    check_in: date
    check_out: date
    guests: int = 1

    def nights(self):
        return (self.check_out - self.check_in).days
