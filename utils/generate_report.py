from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import darkblue


def generate_pdf_report(
    skills,
    questions,
    answers,
    scores,
    feedbacks
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = darkblue

    heading_style = styles["Heading2"]

    normal = styles["BodyText"]

    elements = []

    # -----------------------
    # Title
    # -----------------------

    elements.append(
        Paragraph(
            "AI Interview Report",
            title_style
        )
    )

    elements.append(Spacer(1, 20))

    # -----------------------
    # Skills
    # -----------------------

    elements.append(
        Paragraph(
            "<b>Detected Skills</b>",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            ", ".join(skills),
            normal
        )
    )

    elements.append(Spacer(1, 20))

    # -----------------------
    # Questions
    # -----------------------

    for i in range(len(questions)):

        elements.append(
            Paragraph(
                f"<b>Question {i+1}</b>",
                heading_style
            )
        )

        elements.append(
            Paragraph(
                f"<b>Question:</b> {questions[i]}",
                normal
            )
        )

        elements.append(
            Paragraph(
                f"<b>Answer:</b> {answers[i]}",
                normal
            )
        )

        elements.append(
            Paragraph(
                f"<b>Score:</b> {scores[i]}/10",
                normal
            )
        )

        elements.append(
            Paragraph(
                f"<b>Feedback:</b> {feedbacks[i]}",
                normal
            )
        )

        elements.append(
            Spacer(1, 15)
        )

    # -----------------------
    # Average Score
    # -----------------------

    average = sum(scores) / len(scores)

    elements.append(
        Paragraph(
            "<b>Overall Performance</b>",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            f"Average Score : {average:.2f}/10",
            normal
        )
    )

    if average >= 7:

        verdict = "Interview Ready"

    else:

        verdict = "Needs More Practice"

    elements.append(
        Paragraph(
            f"Final Verdict : <b>{verdict}</b>",
            normal
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer