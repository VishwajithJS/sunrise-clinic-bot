from google import genai
from google.genai import types

client = genai.Client()

config = types.GenerateContentConfig(
    system_instruction="You are a friendly front-desk assistant for Sunrise Clinic, a demo clinic. Keep answers short.",
    max_output_tokens=5,
)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="What is your job?",
    config=config,
)
print(response.text)
print(response.usage_metadata)
print(response.candidates[0].finish_reason)