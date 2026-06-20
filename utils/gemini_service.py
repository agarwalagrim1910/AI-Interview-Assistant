from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Generate interview question based on difficulty
def generate_question(skills, difficulty="Easy"):

    prompt = f"""
Generate ONE interview question.

Candidate Skills:
{skills}

Difficulty Level:
{difficulty}

Rules:

Easy:
- Basic concepts
- Definitions
- Fundamentals
- Suitable for freshers

Medium:
- Practical understanding
- Real-world scenarios
- Comparisons between concepts

Hard:
- Advanced concepts
- Optimization techniques
- Deep technical understanding

Additional Rules:
- Ask only ONE question
- Make it concise
- Relevant to the given skills
- Suitable for a technical interview

Return only the question.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


# Evaluate answer based on question
def evaluate_answer(question, answer):

    prompt = f"""
You are a senior technical interviewer.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer on:

1. Correctness (0-10)
2. Clarity (0-10)
3. Technical Depth (0-10)

Provide feedback in the following format:

Score:
Strengths:
Weaknesses:
Improvement Suggestions:
Interview Verdict (Pass/Fail)

Keep feedback concise and professional.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text