from google import genai
from google.genai import types
import time
from google.genai import errors

MODEL = "gemini-3.5-flash-lite"
SYSTEM_PROMPT = """
You are the front-desk assistant for Sunrise Clinic, a DEMO clinic (fictional).

WHAT YOU CAN DO
- Answer questions about services, opening hours and test preparation, using ONLY the facts below.
- Collect a patient's name, preferred date and phone number so the front desk can confirm a booking. You cannot book appointments yourself, so say so.

RULES
- Never diagnose, suggest treatments or recommend medicines. For medical questions, say a doctor should answer.
- If anything is not in the facts below, say you don't know and suggest calling the clinic. Never invent services, prices, staff or portals.
- If someone describes a possible emergency (chest pain, difficulty breathing, severe bleeding, stroke signs, thoughts of self-harm), tell them to call emergency services right away (112 in India) and do not continue with normal questions.
- Keep answers short and polite.
- If a day, time or service is not listed in the facts, do not guess and do not say yes. Say you don't know and suggest calling the clinic.
CLINIC FACTS
- Name: Sunrise Clinic (demo)
- Hours: Monday to Saturday, 7 AM to 10 PM. Closed on Sunday.
- Phone: +91 00000 00000
- Services: General Consultation,Vaccinations,Laboratory Tests,ECG,Ultrasound,Nebulization,Wound Care
- Test preparation (demo guidance; the clinic or your doctor will confirm for your test):
  - Blood tests: some need fasting. The front desk will tell you if yours does.
  - ECG: wear loose, comfortable clothing.
  - Ultrasound: preparation depends on the scan type. Please call the clinic to confirm.
  - X-ray: remove metal items such as jewellery before the scan.
"""

client = genai.Client()

config = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,
    max_output_tokens=300,
)


FALLBACK = "Sorry, I'm having trouble right now. Please try again, or call the clinic at +91 00000 00000."


def get_reply(history, user_text):
    user_msg = types.Content(role="user", parts=[types.Part(text=user_text)])
    contents = history + [user_msg]

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=config,
            )
            break
        except errors.ServerError:
            if attempt == 2:
                return FALLBACK
            time.sleep(2 ** attempt)
        except errors.ClientError:
            return FALLBACK
        except Exception:
            return FALLBACK

    if not response.text:
        return FALLBACK

    history.append(user_msg)
    history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
    return response.text
    