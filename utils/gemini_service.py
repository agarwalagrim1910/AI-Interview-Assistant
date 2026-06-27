from google import genai
from dotenv import load_dotenv

import os
import json
import time
import random
print("Loaded NEW gemini_service.py")

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# --------------------------------------------------
# Build RAG-Based Interview Prompt
# --------------------------------------------------

def build_question_prompt(
    skills: str,
    difficulty: str,
    retrieved_context: str
) -> str:
    """
    Builds the interview prompt using
    retrieved resume context from the
    RAG pipeline.
    """

    if not retrieved_context.strip():

        retrieved_context = (
            "No relevant resume context was retrieved."
        )

    return f"""
You are a Senior Technical Interviewer.

You are interviewing candidates for top
technology companies such as:

- Google
- Microsoft
- Amazon
- Meta
- NVIDIA
- OpenAI
- AI Startups

========================================
Candidate Skills
========================================

{skills}

========================================
Relevant Resume Context
========================================

{retrieved_context}

========================================
Interview Difficulty
========================================

{difficulty}

Instructions

The resume context above was retrieved
using semantic search from the candidate's
resume.

Generate ONLY ONE interview question.

If the retrieved context contains projects:

- Prioritize project-based questions.
- Ask implementation questions.
- Ask design decisions.
- Ask technology choices.
- Ask challenges faced.
- Ask improvements.

If no projects exist:

Generate a technical question using
the candidate's skills.

Difficulty Rules

Easy

- Fundamentals
- Definitions
- Basic implementation
- Beginner friendly

Medium

- Practical implementation
- Comparisons
- Trade-offs
- Debugging
- Design decisions

Hard

- Architecture
- Scalability
- Optimization
- Production deployment
- Performance
- Edge cases

Rules

- Ask ONLY ONE question.

- Never answer your own question.

- Keep it under 
80 words.

- Make it sound like a real interviewer.

Return ONLY the interview question.
"""


# --------------------------------------------------
# Skill-Aware Fallback Questions
# --------------------------------------------------

def get_fallback_questions(skills: str):
    """
    Returns fallback interview questions based
    on the detected skills.
    """

    skills = skills.lower()

    if any(skill in skills for skill in [
        "python",
        "django",
        "flask"
    ]):

        return [

            "Explain the difference between List and Tuple in Python.",

            "What are Python decorators?",

            "Explain deep copy and shallow copy.",

            "How does exception handling work in Python?",

            "What are generators and why are they useful?"

        ]

    elif any(skill in skills for skill in [

        "machine learning",
        "deep learning",
        "tensorflow",
        "keras",
        "pytorch",
        "bert"

    ]):

        return [

            "Explain the Bias-Variance Tradeoff.",

            "Why did you choose BERT instead of traditional NLP techniques?",

            "What is overfitting and how can it be prevented?",

            "How would you deploy a Machine Learning model into production?",

            "Explain the difference between training, validation and testing datasets."

        ]

    elif any(skill in skills for skill in [

        "sql",
        "mysql",
        "postgresql"

    ]):

        return [

            "Explain SQL Indexes.",

            "Difference between DELETE, TRUNCATE and DROP.",

            "How do JOIN operations work?",

            "What is Normalization?",

            "What is a Primary Key?"

        ]

    elif any(skill in skills for skill in [

        "java"

    ]):

        return [

            "Explain JVM, JDK and JRE.",

            "How does HashMap work internally?",

            "Difference between ArrayList and LinkedList.",

            "Explain Java Multithreading.",

            "What is Polymorphism?"

        ]

    return [

        "Tell me about one technical project you are proud of.",

        "Describe one technical challenge you solved.",

        "Which technology do you enjoy working with the most and why?",

        "How do you approach debugging?",

        "Explain one difficult problem you solved recently."

    ]


# --------------------------------------------------
# Generate Interview Question
# --------------------------------------------------

def generate_question(
    skills,
    difficulty="Easy",
    retrieved_context=""
):
    print("NEW generate_question called")
    """
    Generates one interview question using
    retrieved RAG context.
    """

    prompt = build_question_prompt(

        skills=skills,

        difficulty=difficulty,

        retrieved_context=retrieved_context

    )

    fallback_questions = get_fallback_questions(
        skills
    )

    for attempt in range(5):

        try:

            response = client.models.generate_content(

                model="gemini-2.5-flash",

                contents=prompt

            )

            question = response.text.strip()

            question = question.replace("*", "")

            if not question:

                raise Exception(
                    "Gemini returned an empty response."
                )

            return question
        except Exception as e:

            print(
                f"[Question Generation] Attempt "
                f"{attempt+1}/5 failed:"
            )

            print(e)

            if attempt < 4:

                time.sleep(3)

    print(
        "Using fallback interview question..."
    )

    return random.choice(
        fallback_questions
    )


# --------------------------------------------------
# Build Evaluation Prompt
# --------------------------------------------------

def build_evaluation_prompt(
    question: str,
    answer: str
) -> str:
    """
    Creates the evaluation prompt for Gemini.
    """

    return f"""
You are a Senior Technical Interviewer.

Your task is to evaluate a candidate's interview answer.

========================================
Interview Question
========================================

{question}

========================================
Candidate Answer
========================================

{answer}

Evaluate the answer based on the following:

1. Technical Accuracy
2. Depth of Knowledge
3. Clarity of Explanation
4. Completeness
5. Practical Understanding

Scoring Guidelines

9-10
Excellent answer with strong technical depth.

7-8
Good answer with only minor gaps.

5-6
Average understanding.
Important concepts are missing.

3-4
Weak understanding.

0-2
Incorrect or irrelevant answer.

Return ONLY valid JSON.

Example

{{
    "score": 8,
    "feedback": "Good explanation with solid understanding. Include more implementation details and practical examples.",
    "verdict": "Pass"
}}

Rules

- score must be an integer between 0 and 10.

- verdict must be either
  "Pass"
  or
  "Fail".

- feedback should be concise.

Return ONLY JSON.
"""
# --------------------------------------------------
# Evaluate Candidate Answer
# --------------------------------------------------

def evaluate_answer(
    question,
    answer
):
    """
    Evaluates the candidate's answer using Gemini.
    Returns a JSON response containing
    score, feedback and verdict.
    """

    prompt = build_evaluation_prompt(
        question,
        answer
    )

    for attempt in range(5):

        try:

            response = client.models.generate_content(

                model="gemini-2.5-flash",

                contents=prompt

            )

            cleaned = (

                response.text

                .replace("```json", "")

                .replace("```", "")

                .strip()

            )

            result = json.loads(cleaned)

            score = int(
                result.get("score", 0)
            )

            score = max(
                0,
                min(score, 10)
            )

            verdict = result.get(
                "verdict",
                "Unknown"
            )

            feedback = result.get(
                "feedback",
                "No feedback provided."
            )

            return {

                "score": score,

                "feedback": feedback,

                "verdict": verdict

            }

        except Exception as e:

            print(
                f"[Evaluation] Attempt "
                f"{attempt+1}/5 failed:"
            )

            print(e)

            if attempt < 4:

                time.sleep(3)

    return {

        "score": 0,

        "feedback":
        "Unable to evaluate the answer at the moment.",

        "verdict": "Unknown"

    }