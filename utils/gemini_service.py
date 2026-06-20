from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_questions(skills):

    prompt = f"""
    Generate 10 interview questions for a candidate
    having these skills:

    {skills}

    Return only questions.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text