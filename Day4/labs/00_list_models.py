import os
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

load_dotenv()
apis = ['GOOGLE_API_KEY', 'OPEN_AI_KEY']
for client in apis:
    print("Listing available models for your API key...\n")
    if client == 'GOOGLE_API_KEY':
        client = genai.Client(api_key=os.getenv(client))
        for model in client.models.list():
            # Only show models that support 'generateContent'
            if 'generateContent' in model.supported_actions:
                print(f"-> Model ID: {model.name}")
    else:
        client = OpenAI(api_key=os.getenv(client))
        
        for model in client.models.list():
            print(f"-> Model ID: {model.id}")

    # This lists every model available to you
    