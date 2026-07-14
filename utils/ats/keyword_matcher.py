from utils.skill_database import SKILL_DATABASE


def match_keywords(resume_text):
    """
    Detects ATS keywords using the central skill database.
    """

    resume = resume_text.lower()

    detected = []

    missing = []

    for skills in SKILL_DATABASE.values():

        for skill in skills:

            if skill.lower() in resume:

                detected.append(skill)

            else:

                missing.append(skill)

    return {

        "detected": sorted(set(detected)),

        "missing": sorted(set(missing))

    }