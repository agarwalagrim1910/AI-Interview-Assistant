from google import genai
from dotenv import load_dotenv
import os
import json
import time
import random

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

    fallback_questions = {
        "Easy": [
            "What is a Python list?",
            "What is overfitting in machine learning?",
            "What is a primary key in SQL?",
            "What is the difference between a list and tuple in Python?",
            "What is normalization in machine learning?"
        ],

        "Medium": [
            "Explain the difference between Array and Linked List.",
            "What is the difference between Random Forest and Decision Tree?",
            "Why is normalization used in machine learning?",
            "Explain the working of a hash table.",
            "What are the advantages of using SQL indexes?"
        ],

        "Hard": [
            "Explain the bias-variance tradeoff.",
            "How does gradient descent work?",
            "Explain how transformers work in NLP.",
            "What is backpropagation in neural networks?",
            "How does XGBoost improve over traditional decision trees?"
        ]
    }

    for attempt in range(5):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            question = response.text.strip()

            if not question:
                raise Exception("Empty response")

            return question

        except Exception as e:

            print(
                f"Question generation failed "
                f"(Attempt {attempt + 1}/5): {e}"
            )

            if attempt < 4:
                time.sleep(4)

    print(
        f"Using fallback {difficulty} question."
    )

    return random.choice(
        fallback_questions[difficulty]
    )


# Evaluate answer and return structured JSON
def evaluate_answer(question, answer):

    prompt = f"""
You are a senior technical interviewer.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return ONLY valid JSON.

Example:

{{
    "score": 8,
    "feedback": "Good understanding of the concept but lacks depth.",
    "verdict": "Pass"
}}

Rules:
- score must be between 0 and 10
- verdict must be either Pass or Fail
- feedback should be concise
"""

    for attempt in range(5):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            cleaned_response = (
                response.text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(cleaned_response)

        except Exception as e:

            print(
                f"Evaluation failed "
                f"(Attempt {attempt + 1}/5): {e}"
            )

            if attempt < 4:
                time.sleep(4)

    return {
        "score": 0,
        "feedback": "Unable to evaluate answer right now.",
        "verdict": "Unknown"
    }