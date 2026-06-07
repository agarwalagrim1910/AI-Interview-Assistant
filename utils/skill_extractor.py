def extract_skills(resume_text):

    skills_db = [
        "Java",
        "Python",
        "C++",
        "JavaScript",
        "React",
        "Node.js",
        "SQL",
        "MySQL",
        "MongoDB",
        "Machine Learning",
        "Deep Learning",
        "Data Structures",
        "Algorithms",
        "TensorFlow",
        "PyTorch",
        "Spring Boot",
        "AWS",
        "Git",
        "Docker"
    ]

    found_skills = []

    resume_text = resume_text.lower()

    for skill in skills_db:

        if skill.lower() in resume_text:
            found_skills.append(skill)

    return found_skills