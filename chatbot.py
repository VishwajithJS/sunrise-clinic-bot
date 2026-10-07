from bot import get_reply
from booking import book_appointment, EMERGENCY_TEXT, is_emergency

MENU = """
=== Sunrise Clinic (demo) ===
1. FAQ (ask a question)
2. Book an appointment
3. Emergency information
0. Exit
"""


def faq(history):
    print("Ask about services, hours or test preparation. Type 'back' to return to the menu.")
    while True:
        text = input("You: ").strip()
        if text.lower() == "back":
            return
        if not text:
            continue
        if is_emergency(text):
            print("Bot:", EMERGENCY_TEXT)
            continue
        print("Bot:", get_reply(history, text))


def main():
    history = []
    while True:
        print(MENU)
        choice = input("Choose 0 to 3: ").strip()
        if choice == "1":
            faq(history)
        elif choice == "2":
            book_appointment()
        elif choice == "3":
            print(EMERGENCY_TEXT)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Please enter 0, 1, 2 or 3.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n Goodbye!")
