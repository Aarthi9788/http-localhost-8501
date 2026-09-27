from google import genai
from app.config import get_settings

settings = get_settings()

print("Testing Gemini API...")
print("Model:", settings.gemini_model)

if not settings.gemini_api_key:
    print("ERROR: GEMINI_API_KEY is missing.")
    raise SystemExit

client = genai.Client(
    api_key=settings.gemini_api_key
)

try:
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents="Reply with exactly: LegalEase API test successful"
    )

    print("\nSUCCESS!")
    print(response.text)

except Exception as error:
    print("\nGEMINI ERROR:")
    print(type(error).__name__)
    print(error)