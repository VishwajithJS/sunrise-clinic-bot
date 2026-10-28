from datetime import date, timedelta

from booking import (check_date, check_name, check_phone, is_emergency,
                     wants_to_book)


def first_date(condition):
    """Return the first date in the next 30 days that satisfies condition."""
    for days in range(1, 31):
        d = date.today() + timedelta(days=days)
        if condition(d):
            return d


def fmt(d):
    return d.strftime("%d-%m-%Y")


# --- names ---
assert check_name("Vishwajith JS")[1] is None
assert check_name("R2D2")[0] is None
assert check_name("")[0] is None

# --- phone numbers ---
assert check_phone("9876543210")[0] == "9876543210"
assert check_phone("+91 98765 43210")[0] == "9876543210"
assert check_phone("1234567890")[0] is None   # must start with 6-9
assert check_phone("98765")[0] is None

# --- dates ---
ok_day = first_date(lambda d: d.weekday() != 6)
sunday = first_date(lambda d: d.weekday() == 6)
assert check_date(fmt(ok_day))[1] is None
assert check_date(fmt(sunday))[0] is None                       # closed on Sunday
assert check_date(fmt(date.today()))[0] is None                 # today is too soon
assert check_date(fmt(date.today() + timedelta(days=60)))[0] is None
assert check_date("32-13-2026")[0] is None
assert check_date("tomorrow")[0] is None

# --- emergencies (must trigger) ---
for text in ["i cant breath", "hart attack", "chest pan", "I have chest pain",
             "he is unconscious", "severe bleeding"]:
    assert is_emergency(text), f"missed emergency: {text}"

# --- not emergencies (must NOT trigger) ---
for text in ["Are you open on Sundays?", "do you do chest xray",
             "How do I prepare for a blood test?"]:
    assert not is_emergency(text), f"false alarm: {text}"

# --- booking trigger ---
assert wants_to_book("i want to book")
assert wants_to_book("Book me for Friday")
assert not wants_to_book("Do I need to book for an ECG?")

print("All tests passed")