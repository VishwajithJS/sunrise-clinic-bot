import csv
import os
import re
from datetime import date, datetime, timedelta

BOOKINGS_FILE = "bookings.csv"

EMERGENCY_TEXT = (
    "If this is an emergency, call emergency services right now (112 in India). "
    "Do not wait for the clinic."
)

EMERGENCY_WORDS = ("breath", "chest pain", "bleed", "unconscious", "stroke",
                   "heart attack", "seizure", "overdose", "suicid", "kill myself")


def is_emergency(text):
    text = text.lower()
    return any(word in text for word in EMERGENCY_WORDS)


def check_name(text):
    if re.fullmatch(r"[A-Za-z][A-Za-z .'-]{1,49}", text):
        return text, None
    return None, "Please enter your name using letters only."


def check_phone(text):
    digits = re.sub(r"\D", "", text)
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    if re.fullmatch(r"[6-9]\d{9}", digits):
        return digits, None
    return None, "Please enter a 10-digit mobile number."


def check_date(text):
    try:
        chosen = datetime.strptime(text, "%d-%m-%Y").date()
    except ValueError:
        return None, "Please use the format DD-MM-YYYY, for example 12-10-2026."
    today = date.today()
    if chosen < today + timedelta(days=1) or chosen > today + timedelta(days=30):
        return None, "Please choose a date from tomorrow up to 30 days ahead."
    if chosen.weekday() == 6:
        return None, "The clinic is closed on Sunday. Please choose another day."
    return chosen, None


def ask(prompt, checker):
    while True:
        text = input(prompt).strip()
        if text.lower() == "cancel":
            return None
        if is_emergency(text):
            print(EMERGENCY_TEXT)
            return None
        value, error = checker(text)
        if error:
            print(error)
            continue
        return value


def save_booking(name, phone, chosen_date):
    is_new_file = not os.path.exists(BOOKINGS_FILE)
    with open(BOOKINGS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new_file:
            writer.writerow(["saved_at", "name", "phone", "preferred_date"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"),
                         name, phone, chosen_date.isoformat()])


def book_appointment():
    print("Booking (demo). Type 'cancel' at any time to stop.")
    name = ask("Your name: ", check_name)
    if name is None:
        print("Booking cancelled.")
        return
    phone = ask("Your mobile number: ", check_phone)
    if phone is None:
        print("Booking cancelled.")
        return
    chosen = ask("Preferred date (DD-MM-YYYY): ", check_date)
    if chosen is None:
        print("Booking cancelled.")
        return
    save_booking(name, phone, chosen)
    print(f"Your booking request for {chosen.strftime('%d-%m-%Y')} is saved. "
          "This is a demo, so no one will actually call.")