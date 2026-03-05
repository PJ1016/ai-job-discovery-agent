import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

print(f"Endpoint: {endpoint}")
print(f"API Key (first 5 chars): {api_key[:5] if api_key else 'None'}...")

client = AzureOpenAI(
    api_key=api_key,
    api_version="2024-02-01",
    azure_endpoint=endpoint
)

try:
    print("\nAttempting to list models...")
    models = client.models.list()
    print("Success! Models found:")
    for model in models:
        print(f"- {model.id}")
except Exception as e:
    print(f"\nCaught Error during models.list(): {type(e).__name__}")
    print(f"Error Message: {e}")
    if hasattr(e, 'response'):
        print(f"Status Code: {e.response.status_code}")
        print(f"Response Body: {e.response.text}")

try:
    print(f"\nAttempting completion with {os.getenv('AZURE_OPENAI_DEPLOYMENT')}...")
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=5
    )
    print("Completion Success!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"\nCaught Error during completion: {type(e).__name__}")
    print(f"Error Message: {e}")

