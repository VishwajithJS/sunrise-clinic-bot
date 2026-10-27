import streamlit as st

from bot import get_reply
from booking import (EMERGENCY_TEXT, check_date, check_name, check_phone,
                     is_emergency, save_booking, wants_to_book)

PAGES = ["FAQ", "Book an appointment", "Emergency information"]

st.set_page_config(page_title="Sunrise Clinic (demo)")
st.title("Sunrise Clinic (demo)")
st.caption("A demo chatbot. It does not give medical advice. In an emergency, call 112.")

if "history" not in st.session_state:
    st.session_state.history = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "FAQ"


def go_to_booking():
    st.session_state.page = "Book an appointment"


st.sidebar.radio("Choose", PAGES, key="page")


def faq_page():
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["text"])

    user_text = st.chat_input("Ask about services, hours or test preparation")
    if not user_text:
        return

    st.session_state.messages.append({"role": "user", "text": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    offer_booking = False
    if is_emergency(user_text):
        reply = EMERGENCY_TEXT
    elif wants_to_book(user_text):
        reply = ("I can't take bookings in the chat, but the booking form can. "
                 "Click the button below to open it.")
        offer_booking = True
    else:
        reply = get_reply(st.session_state.history, user_text)

    st.session_state.messages.append({"role": "assistant", "text": reply})
    with st.chat_message("assistant"):
        st.write(reply)
        if offer_booking:
            st.button("Open booking form", on_click=go_to_booking)


def booking_page():
    st.subheader("Book an appointment (demo)")
    st.info("If this is an emergency, call 112 instead of booking.")
    with st.form("booking_form"):
        name = st.text_input("Your name")
        phone = st.text_input("Your mobile number")
        date_text = st.text_input("Preferred date (DD-MM-YYYY)")
        submitted = st.form_submit_button("Submit request")

    if not submitted:
        return

    if any(is_emergency(t) for t in (name, phone, date_text)):
        st.error(EMERGENCY_TEXT)
        return

    name_value, name_error = check_name(name.strip())
    phone_value, phone_error = check_phone(phone.strip())
    date_value, date_error = check_date(date_text.strip())

    problems = [e for e in (name_error, phone_error, date_error) if e]
    if problems:
        for p in problems:
            st.error(p)
        return

    save_booking(name_value, phone_value, date_value)
    st.success(f"Your booking request for {date_value.strftime('%d-%m-%Y')} is saved. "
               "This is a demo, so no one will actually call.")


def emergency_page():
    st.error(EMERGENCY_TEXT)


if st.session_state.page == "FAQ":
    faq_page()
elif st.session_state.page == "Book an appointment":
    booking_page()
else:
    emergency_page()