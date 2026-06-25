from google import genai
from dotenv import load_dotenv

import os
import json
import time
import random

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# --------------------------------------------------
# Build Resume Context
# --------------------------------------------------

def build_resume_context(resume_context: dict) -> str:
    """
    Converts the extracted resume dictionary into
    a clean, structured text block for Gemini.
    """

    if not resume_context:
        return "No resume context available."

    sections = []

    field_names = {
        "projects": "Projects",
        "experience": "Experience",
        "education": "Education",
        "skills": "Skills",
        "certifications": "Certifications"
    }

    for key, title in field_names.items():

        value = resume_context.get(key, "")

        if value and value.strip():

            sections.append(
                f"{title}:\n{value.strip()}"
            )

    if not sections:

        return "No structured resume information found."

    return "\n\n".join(sections)


# --------------------------------------------------
# Build Interview Prompt
# --------------------------------------------------

def build_question_prompt(
    skills: str,
    difficulty: str,
    resume_context: dict
) -> str:
    """
    Creates the prompt used for question generation.
    """

    context = build_resume_context(resume_context)

    return f"""
You are a Senior Technical Interviewer working at one of the world's leading technology companies such as Google, Microsoft, Amazon, Meta or an AI startup.

Your task is to conduct a realistic technical interview.

===========================
Candidate Skills
===========================

{skills}

===========================
Candidate Resume
===========================

{context}

===========================
Difficulty Level
===========================

{difficulty}

Interview Guidelines

1. If the resume contains projects,
   ALWAYS prioritize asking about those projects.

2. Ask implementation-focused questions.

3. Ask WHY certain technologies were chosen.

4. Ask about architecture,
   design decisions,
   optimization,
   scalability,
   challenges,
   improvements.

5. Avoid generic textbook questions whenever
   sufficient resume information exists.

6. If projects are unavailable,
   generate a question using the candidate's skills.

Difficulty Rules

Easy
- Fundamentals
- Definitions
- Basic implementation

Medium
- Practical implementation
- Comparisons
- Trade-offs
- Debugging

Hard
- Architecture
- Scalability
- Optimization
- Production deployment
- Edge cases

Rules

• Ask ONLY ONE question.

• Never answer your own question.

• Keep it under 80 words.

• Make it sound like a real interviewer.

Return ONLY the interview question.
"""# --------------------------------------------------
# Skill-Aware Fallback Questions
# --------------------------------------------------

def get_fallback_questions(skills: str):
    """
    Returns fallback questions based on the
    candidate's detected skills.
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

            "Explain the difference between deep copy and shallow copy.",

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

            "Why do we split data into training and testing sets?",

            "Explain the Bias-Variance Tradeoff.",

            "Why did you choose BERT over traditional NLP techniques?",

            "What is overfitting and how can it be prevented?",

            "How would you deploy a Machine Learning model into production?"
        ]

    elif any(skill in skills for skill in [
        "sql",
        "mysql",
        "postgresql"
    ]):

        return [

            "What is normalization?",

            "Explain SQL indexes.",

            "Difference between DELETE, TRUNCATE and DROP.",

            "How do JOIN operations work?",

            "What is a Primary Key?"
        ]

    elif any(skill in skills for skill in [
        "java"
    ]):

        return [

            "Explain JVM, JRE and JDK.",

            "How does HashMap work internally?",

            "Difference between ArrayList and LinkedList.",

            "Explain Java Multithreading.",

            "What is Polymorphism?"
        ]

    else:

        return [

            "Tell me about one technical project you are proud of.",

            "Explain one technical challenge you solved.",

            "Describe your favorite technology and why you like it.",

            "How do you approach debugging?",

            "Explain one difficult problem you solved recently."
        ]


# --------------------------------------------------
# Generate Interview Question
# --------------------------------------------------

def generate_question(
    skills,
    difficulty="Easy",
    resume_context=None
):
    """
    Generates one resume-aware interview question.
    """

    prompt = build_question_prompt(

        skills=skills,

        difficulty=difficulty,

        resume_context=resume_context
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

===========================
Interview Question
===========================

{question}

===========================
Candidate Answer
===========================

{answer}

Evaluate the answer on the following criteria:

1. Technical Accuracy
2. Depth of Knowledge
3. Clarity of Explanation
4. Completeness
5. Practical Understanding

Scoring Guidelines

9-10
Excellent answer with strong technical depth.

7-8
Good answer with minor gaps.

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
    Evaluates the candidate answer using Gemini.
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

            # -----------------------------
            # Validation
            # -----------------------------

            score = int(result.get("score", 0))

            score = max(0, min(score, 10))

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