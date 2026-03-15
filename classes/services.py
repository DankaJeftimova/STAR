from google import genai
from django.conf import settings

def call_gemini(prompt):
    
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    
    return response.text