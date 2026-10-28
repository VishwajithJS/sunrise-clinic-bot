import time
from datetime import date, timedelta

import streamlit as st

from bot import get_reply
from booking import (EMERGENCY_TEXT, check_date, check_name, check_phone,
                     is_emergency, save_booking, wants_to_book)

FAQ_PAGE = "💬 Ask a question"
BOOK_PAGE = "📅 Book an appointment"
EMERGENCY_PAGE = "🚨 Emergency information"
PAGES = [FAQ_PAGE, BOOK_PAGE, EMERGENCY_PAGE]

SUGGESTIONS = [
    "Are you open on Sundays?",
    "Which services do you offer?",
    "How do I prepare for a blood test?",
]

st.set_page_config(page_title="Sunrise Clinic (demo)", page_icon="🌅")

st.markdown(
    """
    <style>
    .hero {
        background: linear-gradient(120deg, #E8590C, #F59F00);
        padding: 1.2rem 1.5rem;
        border-radius: 14px;
        margin-bottom: 1rem;
    }
    .hero h1 { margin: 0; font-size: 1.8rem; color: white !important; }
    .hero p { margin: 0.3rem 0 0 0; color: white !important; opacity: 0.95; }
    div[data-testid="stChatMessage"] {
        border-radius: 12px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
    }
    .stButton > button { border-radius: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "history" not in st.session_state:
    st.session_state.history = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = FAQ_PAGE


def go_to_booking():
    st.session_state.page = BOOK_PAGE


def ask_suggestion(question):
    st.session_state.pending = question


def clear_chat():
    st.session_state.history = []
    st.session_state.messages = []


def typewriter(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.03)


# ---------- sidebar ----------
with st.sidebar:
    st.header("🌅 Sunrise Clinic")
    st.caption("A DEMO clinic (fictional)")
    st.radio("Menu", PAGES, key="page", label_visibility="collapsed")
    st.divider()
    st.markdown("**Hours**  \nMonday to Saturday, 7 AM to 10 PM  \nClosed on Sunday")
    st.markdown("**Phone**  \n+91 00000 00000")
    st.divider()
    st.button("Clear chat", on_click=clear_chat)

# ---------- header ----------
st.markdown(
    '<div class="hero"><h1>🌅 Sunrise Clinic</h1>'
    "<p>Demo front-desk assistant. It does not give medical advice. "
    "In an emergency, call 112.</p></div>",
    unsafe_allow_html=True,
)


# ---------- pages ----------
def welcome():
    c1, c2, c3 = st.columns(3)
    c1.metric("Open", "Mon to Sat")
    c2.metric("Hours", "7 AM to 10 PM")
    c3.metric("Closed", "Sunday")
    st.markdown("**Try asking:**")
    for q in SUGGESTIONS:
        st.button(q, key=f"suggestion_{q}", on_click=ask_suggestion, args=(q,))


def faq_page():
    typed = st.chat_input("Ask about services, hours or test preparation")
    pending = st.session_state.pop("pending", None)
    user_text = typed or pending

    if not st.session_state.messages and not user_text:
        welcome()

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["text"])

    if not user_text:
        return

    st.session_state.messages.append({"role": "user", "text": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        if is_emergency(user_text):
            reply = EMERGENCY_TEXT
            st.error(reply)
        elif wants_to_book(user_text):
            reply = ("I can't take bookings in the chat, but the booking form can. "
                     "Click the button below to open it.")
            st.write(reply)
            st.button("Open booking form", on_click=go_to_booking)
        else:
            with st.spinner("Typing..."):
                reply = get_reply(st.session_state.history, user_text)
            st.write_stream(typewriter(reply))

    st.session_state.messages.append({"role": "assistant", "text": reply})


def booking_page():
    st.subheader("📅 Book an appointment")
    st.info("Demo only. If this is an emergency, call 112 instead of booking.")

    tomorrow = date.today() + timedelta(days=1)
    with st.form("booking_form"):
        name = st.text_input("Your name")
        phone = st.text_input("Your mobile number", placeholder="10-digit number")
        chosen = st.date_input(
            "Preferred date",
            value=tomorrow,
            min_value=tomorrow,
            max_value=date.today() + timedelta(days=30),
            format="DD-MM-YYYY",
        )
        submitted = st.form_submit_button("Submit request")

    if not submitted:
        return

    if any(is_emergency(t) for t in (name, phone)):
        st.error(EMERGENCY_TEXT)
        return

    name_value, name_error = check_name(name.strip())
    phone_value, phone_error = check_phone(phone.strip())
    date_value, date_error = check_date(chosen.strftime("%d-%m-%Y"))

    problems = [e for e in (name_error, phone_error, date_error) if e]
    if problems:
        for p in problems:
            st.error(p)
        return

    save_booking(name_value, phone_value, date_value)
    st.toast("Booking request saved", icon="✅")
    st.success(f"Your booking request for {date_value.strftime('%d-%m-%Y')} is saved. "
               "This is a demo, so no one will actually call.")


def emergency_page():
    st.error(EMERGENCY_TEXT)
    st.markdown("This assistant cannot assess symptoms or give medical advice. "
                "For anything urgent, contact emergency services or go to the nearest hospital.")


if st.session_state.page == FAQ_PAGE:
    faq_page()
elif st.session_state.page == BOOK_PAGE:
    booking_page()
else:
    emergency_page()