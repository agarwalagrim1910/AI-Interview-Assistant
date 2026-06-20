from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Generate interview questions
def generate_questions(skills):

    prompt = f"""
    Generate 10 technical interview questions for a candidate
    having these skills:

    {skills}

    Return only the questions in numbered format.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# Evaluate candidate answer
def evaluate_answer(answer):

    prompt = f"""
    You are an expert technical interviewer.

    Evaluate the following interview answer.

    Candidate Answer:
    {answer}

    Provide:

    1. Score out of 10
    2. Strengths
    3. Weaknesses
    4. Improved Answer

    Keep the feedback professional and concise.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text