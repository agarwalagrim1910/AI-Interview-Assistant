import streamlit as st
from utils.pdf_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.question_generator import generate_questions


st.title("AI Interview Assistant")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)

if uploaded_file is not None:

    text = extract_text_from_pdf(uploaded_file)

    st.success("Resume Parsed Successfully!")

    st.subheader("Detected Skills")

    skills = extract_skills(text)

    for skill in skills:
        st.write("✅", skill)
    questions = generate_questions(skills)

    st.subheader("Interview Questions")

    for i, question in enumerate(questions, start=1):
        st.write(f"{i}. {question}") 
    
           

    st.subheader("Resume Content")

    st.text(text)