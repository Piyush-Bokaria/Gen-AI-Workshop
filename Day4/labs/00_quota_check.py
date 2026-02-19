import os
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
client2 = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

# The list of models we want to "test" for quota
models_to_test = [
    "gemini-2.0-flash",
    "gemini-2.5-flash", 
    "gemini-2.5-flash-lite",
    "gpt-4o-mini",
    "04-mini",
    "gpt-4.1-mini"
]

print("🔍 Testing Model Availability...\n")

for model_id in models_to_test[:3]:
    try:
        response = client.models.generate_content(
            model=model_id,
            contents="hi"
        )
        print(f"✅ {model_id}: AVAILABLE")
    except Exception as e:
        if "429" in str(e):
            print(f"❌ {model_id}: QUOTA EXHAUSTED (429)")
        else:
            print(f"❓ {model_id}: OTHER ERROR ({e})")

for model_id in models_to_test[3:]:
    try:
        response = client2.models.retrieve(model=model_id)
        print(f"✅ {model_id}: AVAILABLE")
    except Exception as e:
        msg = str(e)
        if "429" in str(e):
            print(f"❌ {model_id}: QUOTA EXHAUSTED (429)")
        elif "404" in msg or "not found" in msg.lower():
            print(f"❌ {model_id}: NOT FOUND / NO ACCESS")
        else:
            print(f"❓ {model_id}: OTHER ERROR ({e})")