from google import genai
from dotenv import load_dotenv

import os
import json
import time
import random
from utils.prompt_builder import build_interview_prompt
print("Loaded NEW gemini_service.py")

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

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
    retrieved_context="",
    previous_questions=None,
    performance_context=""
):
    print("NEW generate_question called")

    """
    Generates one interview question using
    RAG + adaptive performance context.
    """

    if previous_questions is None:

        previous_questions = []


    prompt = build_interview_prompt(

        skills=skills,

        difficulty=difficulty,

        retrieved_context=retrieved_context,

        previous_questions=previous_questions,

        performance_context=performance_context

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

            question = question.replace(
                "*",
                ""
            )


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
# --------------------------------------------------
# Job Match Analysis
# --------------------------------------------------

def generate_job_match_analysis(
    match_result
):
    """
    Generates AI feedback for Resume vs Job Description matching.
    """

    prompt = f"""
You are an experienced Technical Recruiter.

Analyze the resume-job matching result below.

Match Score:
{match_result["match_score"]}%

Matched Skills:
{', '.join(match_result["matched_skills"])}

Missing Skills:
{', '.join(match_result["missing_skills"])}

Resume Skills:
{', '.join(match_result["resume_skills"])}

Job Description Skills:
{', '.join(match_result["jd_skills"])}

Return ONLY valid JSON.

Example:

{{
    "overall_feedback": "The resume is a good match for this role.",

    "strengths": [
        "...",
        "..."
    ],

    "missing_skill_analysis": [
        "...",
        "..."
    ],

    "resume_improvements": [
        "...",
        "..."
    ],

    "application_recommendation":
        "Apply Now"
}}

Rules:

- Return ONLY JSON.
- Do not include markdown.
- Keep feedback concise.
"""

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

            return json.loads(cleaned)

        except Exception as e:

            print(
                f"[Job Match] Attempt {attempt+1}/5 failed:"
            )

            print(e)

            if attempt < 4:
                time.sleep(3)

    return {

        "overall_feedback":
        "Unable to generate AI analysis.",

        "strengths": [],

        "missing_skill_analysis": [],

        "resume_improvements": [],

        "application_recommendation":
        "Analysis unavailable"

    }