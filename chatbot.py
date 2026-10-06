from bot import get_reply

history = []

while True:
    user_text = input("You: ")
    if user_text.strip().lower() in ("quit", "exit"):
        break
    print("Bot:", get_reply(history, user_text))