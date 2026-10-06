from bot import get_reply

MENU = """
=== Sunrise Clinic (demo) ===
1. FAQ (ask a question)
2. Book an appointment
3. Emergency information
4. Test details
5. Rate us
6. About us
0. Exit
"""

EMERGENCY_TEXT = (
    "If this is an emergency, call emergency services right now (112 in India). "
    "Do not wait for the clinic."
)

ABOUT_TEXT = (
    "Sunrise Clinic is a DEMO clinic (fictional).\n"
    "Hours: Monday to Saturday, 7 AM to 10 PM. Closed on Sunday.\n"
    "Phone: +91 00000 00000\n"
    "Services: General Consultation, Vaccinations, Laboratory Tests, ECG, "
    "Ultrasound, Nebulization, Wound Care"
)

TEST_DETAILS = {
    "Blood tests": "Some need fasting. The front desk will tell you if yours does.",
    "ECG": "Wear loose, comfortable clothing.",
    "Ultrasound": "Preparation depends on the scan type. Please call the clinic to confirm.",
    "X-ray": "Remove metal items such as jewellery before the scan.",
}


def faq(history):
    print("Ask about services, hours or test preparation. Type 'back' to return to the menu.")
    while True:
        text = input("You: ").strip()
        if text.lower() == "back":
            return
        if not text:
            continue
        print("Bot:", get_reply(history, text))


def show_test_details():
    print("Demo guidance. The clinic or your doctor will confirm for your test.")
    for name, info in TEST_DETAILS.items():
        print(f"- {name}: {info}")


def book_appointment():
    print("Booking is coming soon.")


def rate_us():
    print("Ratings are coming soon.")


def main():
    history = []
    while True:
        print(MENU)
        choice = input("Choose 0 to 6: ").strip()
        if choice == "1":
            faq(history)
        elif choice == "2":
            book_appointment()
        elif choice == "3":
            print(EMERGENCY_TEXT)
        elif choice == "4":
            show_test_details()
        elif choice == "5":
            rate_us()
        elif choice == "6":
            print(ABOUT_TEXT)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Please enter a number from 0 to 6.")


if __name__ == "__main__":
    main()