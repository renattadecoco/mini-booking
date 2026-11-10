import os
import tempfile

from booking.models import Room
from booking.service import BookingService
from booking.storage import Storage


def make_service(test):
    d = tempfile.TemporaryDirectory()
    test.addCleanup(d.cleanup)
    path = os.path.join(d.name, "db.json")
    svc = BookingService(Storage(path))
    svc.add_room(Room("R2", "Suite", "150.00", 4))
    svc.add_room(Room("R1", "Standard", "100.00", 2))
    return svc, path
