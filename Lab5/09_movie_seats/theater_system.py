"""Reserve numbered seats and store the local cinema seating plan."""
import hashlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

shows = {"SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
         "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []}}


def _valid_seat(seat, count):
    return isinstance(seat, int) and not isinstance(seat, bool) and (
        1 <= seat <= count)


def reserve_seat(show_id, seat_number, system_logs=None):
    """Return True when the requested seat is reserved."""
    show = shows.get(show_id)
    valid = (show is not None and _valid_seat(seat_number, show["seats"])
             and seat_number not in show["booked"])
    if valid:
        show["booked"].append(seat_number)
    if system_logs is not None:
        action = "Reserved" if valid else "Rejected"
        system_logs.append(f"{action} seat {seat_number} for {show_id}")
    return valid


def release_seat(show_id, seat_number):
    """Release a booked seat and report whether a booking changed."""
    show = shows.get(show_id)
    if (show is None or not _valid_seat(seat_number, show["seats"])
            or seat_number not in show["booked"]):
        return False
    show["booked"].remove(seat_number)
    return True


def ticket_code(show_id, seat_number):
    """Return a short, repeatable display reference for a show and seat."""
    reference = json.dumps([show_id, seat_number]).encode("utf-8")
    return hashlib.sha256(reference).hexdigest()[:8]


def dump_reservations(file="seats.json"):
    """Replace a seating plan only after the new JSON has been written."""
    target = Path(file)
    with NamedTemporaryFile(mode="w", dir=target.parent, encoding="utf-8",
                            delete=False) as stream:
        temporary = Path(stream.name)
        try:
            json.dump(shows, stream, indent=2)
            stream.flush()
        except (OSError, TypeError, ValueError):
            stream.close()
            temporary.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def _valid_show(show):
    if not isinstance(show, dict) or not isinstance(show.get("title"), str):
        return False
    count = show.get("seats")
    booked = show.get("booked")
    return (isinstance(count, int) and not isinstance(count, bool)
            and count > 0 and isinstance(booked, list)
            and all(_valid_seat(seat, count) for seat in booked)
            and len(booked) == len(set(booked)))


def load_reservations(file="seats.json"):
    """Load a valid seating plan, leaving current data intact on error."""
    with Path(file).open(encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, dict) or not all(map(_valid_show, data.values())):
        raise ValueError("Invalid seating plan")
    shows.clear()
    shows.update(data)


def print_seating_summary():
    """Display the remaining capacity for each show."""
    for show in shows.values():
        free = show["seats"] - len(show["booked"])
        print(f"{show['title']}: {free} seats free, booked = {show['booked']}")


# Preserve the entry point used by the starter's callers.
printSeatingSummary = print_seating_summary


def main():
    """Book a seat for SHOW-2 and save the updated seating plan."""
    if Path("seats.json").exists():
        load_reservations()
    raw = input("Seat number to book for SHOW-2 (Enter for 4): ") or "4"
    try:
        seat = int(raw)
    except ValueError:
        print("Enter a whole seat number.")
        return
    if reserve_seat("SHOW-2", seat):
        dump_reservations()
        print("Ticket code:", ticket_code("SHOW-2", seat))
    else:
        print("Seat unavailable or outside the seating plan.")
    print_seating_summary()


if __name__ == "__main__":
    main()
