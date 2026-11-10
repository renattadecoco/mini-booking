from .models import Booking


class BookingError(Exception):
    pass


class BookingService:
    def __init__(self, storage):
        self.storage = storage

    def add_room(self, room):
        self.storage.rooms[room.id] = room
        self.storage.save()

    def _overlaps(self, a_in, a_out, b_in, b_out):
        # Half-open ranges [check_in, check_out): back-to-back stays
        # (one check-out day == the next check-in day) do not overlap.
        return a_in < b_out and b_in < a_out

    def is_available(self, room_id, check_in, check_out):
        for b in self.storage.bookings:
            if b.room_id == room_id and self._overlaps(check_in, check_out, b.check_in, b.check_out):
                return False
        return True

    def book(self, room_id, guest, check_in, check_out, guests=1):
        room = self.storage.rooms.get(room_id)
        if room is None:
            raise BookingError(f"unknown room: {room_id}")
        if check_out <= check_in:
            raise BookingError("check_out must be after check_in")
        if guests > room.capacity:
            raise BookingError("guests above room capacity")
        if not self.is_available(room_id, check_in, check_out):
            raise BookingError("room not available")
        next_id = getattr(self.storage, "next_booking_id", None)
        if next_id is None:
            next_id = max((b.id for b in self.storage.bookings), default=0) + 1
        b = Booking(next_id, room_id, guest, check_in, check_out, guests)
        self.storage.bookings.append(b)
        self.storage.next_booking_id = next_id + 1
        self.storage.save()
        return b

    def cancel(self, booking_id):
        if not any(b.id == booking_id for b in self.storage.bookings):
            raise BookingError(f"unknown booking: {booking_id}")
        self.storage.bookings = [b for b in self.storage.bookings if b.id != booking_id]
        self.storage.save()

    def available_rooms(self, check_in, check_out, guests=1):
        """Return sorted ids of rooms free for [check_in, check_out) with capacity >= guests."""
        return sorted(
            room_id
            for room_id, room in self.storage.rooms.items()
            if room.capacity >= guests and self.is_available(room_id, check_in, check_out)
        )
