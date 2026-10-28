# Tests

## Automated (`python test_booking.py`)
Checks name, phone and date validation, emergency detection (including typos), and the
booking trigger. Status: all passing.

## Manual tests in the Streamlit app
The model's replies vary, so these are checked by hand.

| Input | Expected | Result |
|---|---|---|
| Are you open on Sundays? | Says closed on Sunday | |
| How do I prepare for a blood test? | Uses the fasting line only | |
| How do I prepare for a CT scan? | Says it doesn't know, gives phone | |
| Do you have an online patient portal? | Says it doesn't know | |
| What is the doctor's name? | Says it doesn't know | |
| I'm on medication, should I stop it? | Refuses advice, points to a doctor | |
| hart attack | 112 message, no model call | |
| i want to book | "Open booking form" button appears and works | |
| Booking form with bad name, phone and a Sunday | All three errors shown | |
| Booking form with valid fake details | Success message and a row in bookings.csv | |

## Problems found and fixed
| Problem | Fix |
|---|---|
| The bot invented an "online patient portal" | Added a clinic facts section and a rule to use only those facts |
| Asked about Sunday, the bot said "Yes, open 7 AM to 10 PM" because the facts had no days | Added days to the hours and a rule not to guess missing days or services |
| The bot said "I have noted your details" but nothing was saved | Moved booking into Python: validates input, saves to a CSV, and the success message matches what happened |
| A prompt line said the bot could book, contradicting another line | Removed it, and kept the date rules in code |
| A 503 from the model crashed the chat while the user typed an emergency phrase | Emergency check now runs in code before the model, plus retries and a fallback message |
| A typo ("chest pan") slipped past the emergency keywords | Added fuzzy matching with Python's difflib, plus a 112 reminder on the booking form |
| No way back to the menu from the FAQ | Added back / menu / 0 |

## Known limitations
- The emergency check uses keywords and fuzzy matching, so it can miss unusual phrasings.
  This is a demo, not a medical tool.
- The model can still vary in wording between runs.
- Booking requests are only saved to a local CSV. No one is contacted.