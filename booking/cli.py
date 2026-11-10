import argparse
import sys
from datetime import date

from .pricing import quote
from .service import BookingError, BookingService
from .storage import Storage


def main(argv=None, out=None):
    out = out or sys.stdout
    p = argparse.ArgumentParser(prog="booking")
    p.add_argument("--db", required=True)
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("book")
    b.add_argument("room")
    b.add_argument("guest")
    b.add_argument("check_in")
    b.add_argument("check_out")
    b.add_argument("--guests", type=int, default=1)
    c = sub.add_parser("cancel")
    c.add_argument("id", type=int)
    a = sub.add_parser("available")
    a.add_argument("check_in")
    a.add_argument("check_out")
    a.add_argument("--guests", type=int, default=1)
    q = sub.add_parser("quote")
    q.add_argument("room")
    q.add_argument("check_in")
    q.add_argument("check_out")
    args = p.parse_args(argv)

    try:
        svc = BookingService(Storage(args.db))
        if args.cmd == "book":
            bk = svc.book(args.room, args.guest, date.fromisoformat(args.check_in),
                          date.fromisoformat(args.check_out), args.guests)
            print(f"booked {bk.id}", file=out)
        elif args.cmd == "cancel":
            svc.cancel(args.id)
            print(f"cancelled {args.id}", file=out)
        elif args.cmd == "available":
            rooms = svc.available_rooms(date.fromisoformat(args.check_in),
                                        date.fromisoformat(args.check_out), args.guests)
            for room_id in rooms:
                print(room_id, file=out)
        elif args.cmd == "quote":
            room = svc.storage.rooms.get(args.room)
            if room is None:
                raise BookingError(f"unknown room: {args.room}")
            total = quote(room, date.fromisoformat(args.check_in),
                          date.fromisoformat(args.check_out))
            print(f"{total:.2f}", file=out)
    except (BookingError, ValueError) as e:
        print(f"error: {e}", file=out)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
