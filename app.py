import streamlit as st

from utils.pdf_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.resume_context import extract_resume_context

from utils.gemini_service import (
    generate_question,
    evaluate_answer
)

from utils.generate_report import generate_pdf_report


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Interview Assistant")

TOTAL_QUESTIONS = 5


# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------

def initialize_session():

    defaults = {

        "question_number": 1,

        "scores": [],

        "answers": [],

        "feedbacks": [],

        "questions": [],

        "evaluated": False,

        "current_result": None,

        "skills": [],

        "resume_text": "",

        # NEW
        "resume_context": {},

        "question": ""

    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


initialize_session()


# --------------------------------------------------
# Reset Interview
# --------------------------------------------------

def reset_interview():

    keys = [

        "question_number",

        "scores",

        "answers",

        "feedbacks",

        "questions",

        "evaluated",

        "current_result",

        "skills",

        "resume_text",

        "resume_context",

        "question"

    ]

    for key in keys:

        if key in st.session_state:
            del st.session_state[key]

    initialize_session()


# --------------------------------------------------
# Difficulty Logic
# --------------------------------------------------

def get_difficulty(question_number):

    if question_number <= 2:
        return "Easy"

    elif question_number <= 4:
        return "Medium"

    else:
        return "Hard"


# --------------------------------------------------
# Resume Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)

if uploaded_file is None:

    st.info(
        "Please upload your resume to begin the interview."
    )

    st.stop()


# --------------------------------------------------
# Parse Resume
# --------------------------------------------------

if not st.session_state.resume_text:

    with st.spinner("Parsing Resume..."):

        # Extract Resume Text

        st.session_state.resume_text = extract_text_from_pdf(
            uploaded_file
        )

        # Extract Skills

        st.session_state.skills = extract_skills(
            st.session_state.resume_text
        )

        # Extract Resume Context

        st.session_state.resume_context = extract_resume_context(
            st.session_state.resume_text
        )


skills = st.session_state.skills

resume_context = st.session_state.resume_context
# --------------------------------------------------
# Resume Successfully Parsed
# --------------------------------------------------

st.success("✅ Resume Parsed Successfully!")

st.subheader("🛠 Detected Skills")

if skills:

    for skill in skills:
        st.write("✅", skill)

else:

    st.warning(
        "No predefined skills were detected from the resume."
    )


# --------------------------------------------------
# Resume Context (Debug)
# Remove this section later if you don't need it.
# --------------------------------------------------

with st.expander("📄 Resume Context"):

    st.write("### 📌 Projects")
    st.write(
        resume_context.get("projects", "Not Found")
    )

    st.write("### 💼 Experience")
    st.write(
        resume_context.get("experience", "Not Found")
    )

    st.write("### 🎓 Education")
    st.write(
        resume_context.get("education", "Not Found")
    )

    st.write("### 🏆 Certifications")
    st.write(
        resume_context.get("certifications", "Not Found")
    )

    st.write("### 🛠 Skills Section")
    st.write(
        resume_context.get("skills", "Not Found")
    )


# --------------------------------------------------
# Current Question
# --------------------------------------------------

difficulty = get_difficulty(
    st.session_state.question_number
)

st.divider()

st.subheader(
    f"📝 Question {st.session_state.question_number}/{TOTAL_QUESTIONS}"
)

st.caption(
    f"Difficulty : **{difficulty}**"
)


# --------------------------------------------------
# Generate Question (Only Once)
# --------------------------------------------------

if not st.session_state.question:

    with st.spinner(
        "Generating Resume-Aware Interview Question..."
    ):

        st.session_state.question = generate_question(

            skills=", ".join(skills),

            difficulty=difficulty,

            resume_context=resume_context

        )


question = st.session_state.question


st.info(question)


# --------------------------------------------------
# Candidate Answer
# --------------------------------------------------

user_answer = st.text_area(

    "Write your answer here",

    height=220,

    key=f"answer_{st.session_state.question_number}"

)
# --------------------------------------------------
# Evaluate Answer
# --------------------------------------------------

if not st.session_state.evaluated:

    if st.button(
        "✅ Evaluate Answer",
        use_container_width=True
    ):

        if user_answer.strip():

            with st.spinner(
                "Evaluating your answer..."
            ):

                result = evaluate_answer(
                    question,
                    user_answer
                )

            score = result.get("score", 0)

            feedback = result.get(
                "feedback",
                ""
            )

            verdict = result.get(
                "verdict",
                "Unknown"
            )

            # ------------------------------------------
            # Save Interview Data
            # ------------------------------------------

            st.session_state.questions.append(
                question
            )

            st.session_state.answers.append(
                user_answer
            )

            st.session_state.scores.append(
                score
            )

            st.session_state.feedbacks.append(
                feedback
            )

            st.session_state.current_result = result

            st.session_state.evaluated = True

            st.rerun()

        else:

            st.warning(
                "Please write your answer before evaluation."
            )


# --------------------------------------------------
# Show Evaluation Result
# --------------------------------------------------

if st.session_state.evaluated:

    result = st.session_state.current_result

    score = result["score"]

    feedback = result["feedback"]

    verdict = result["verdict"]

    st.divider()

    st.subheader("📊 Evaluation")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Score",
            f"{score}/10"
        )

        st.progress(score / 10)

    with col2:

        if verdict == "Pass":

            st.success("✅ Pass")

        elif verdict == "Fail":

            st.error("❌ Fail")

        else:

            st.warning(verdict)

    st.write("### 💬 Feedback")

    st.write(feedback)


    # --------------------------------------------------
    # Next Question
    # --------------------------------------------------

    if st.session_state.question_number < TOTAL_QUESTIONS:

        if st.button(
            "➡ Next Question",
            use_container_width=True
        ):

            st.session_state.question_number += 1

            st.session_state.question = ""

            st.session_state.current_result = None

            st.session_state.evaluated = False

            st.rerun()

    else:

        if st.button(
            "🏁 Finish Interview",
            use_container_width=True
        ):

            st.session_state.question_number += 1

            st.rerun()
# --------------------------------------------------
# Final Interview Report
# --------------------------------------------------

if st.session_state.question_number > TOTAL_QUESTIONS:

    st.balloons()

    st.header("🎉 Interview Completed")

    average_score = (
        sum(st.session_state.scores)
        / len(st.session_state.scores)
    )

    st.metric(
        label="Average Score",
        value=f"{average_score:.2f}/10"
    )

    st.progress(
        min(average_score / 10, 1.0)
    )

    st.divider()

    st.subheader("📋 Interview Summary")

    for i in range(
        len(st.session_state.questions)
    ):

        with st.expander(
            f"Question {i+1}"
        ):

            st.write(
                f"**Question:** {st.session_state.questions[i]}"
            )

            st.write(
                f"**Your Answer:** {st.session_state.answers[i]}"
            )

            st.write(
                f"**Score:** {st.session_state.scores[i]}/10"
            )

            st.write(
                f"**Feedback:** {st.session_state.feedbacks[i]}"
            )

    st.divider()

    st.subheader("🏆 Final Verdict")

    if average_score >= 8:

        st.success(
            "🌟 Excellent Performance! You are interview ready."
        )

    elif average_score >= 7:

        st.success(
            "✅ Good Job! Keep practicing a few advanced topics."
        )

    elif average_score >= 5:

        st.warning(
            "📚 Fair Performance. Practice more before interviews."
        )

    else:

        st.error(
            "❌ Needs Significant Improvement."
        )

    # --------------------------------------------------
    # Generate PDF Report
    # --------------------------------------------------

    pdf = generate_pdf_report(

        skills=st.session_state.skills,

        questions=st.session_state.questions,

        answers=st.session_state.answers,

        scores=st.session_state.scores,

        feedbacks=st.session_state.feedbacks

    )

    st.download_button(

        label="📥 Download Interview Report",

        data=pdf,

        file_name="AI_Interview_Report.pdf",

        mime="application/pdf",

        use_container_width=True

    )

    st.divider()

    if st.button(

        "🔄 Start New Interview",

        use_container_width=True

    ):

        reset_interview()

        st.rerun()