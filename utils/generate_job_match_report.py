from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.units import inch


def generate_job_match_report(result, output_path):

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(output_path)

    story = []

    # ======================================================
    # Title
    # ======================================================

    title = Paragraph(
        "<b><font size=20>Job Description Match Report</font></b>",
        styles["Title"]
    )

    story.append(title)

    story.append(Spacer(1, 0.3 * inch))

    # ======================================================
    # Match Score
    # ======================================================

    story.append(

        Paragraph(

            f"<b>Overall Match Score:</b> {result['match_score']}%",

            styles["Heading2"]

        )

    )

    story.append(Spacer(1, 0.3 * inch))

    # ======================================================
    # Statistics
    # ======================================================

    data = [

        [

            "Resume Skills",

            len(result["resume_skills"])

        ],

        [

            "Job Skills",

            len(result["jd_skills"])

        ],

        [

            "Matched Skills",

            len(result["matched_skills"])

        ],

        [

            "Missing Skills",

            len(result["missing_skills"])

        ]

    ]

    table = Table(
        data,
        colWidths=[220, 120]
    )

    table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica")

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))

    # ======================================================
    # Resume Skills
    # ======================================================

    story.append(

        Paragraph(
            "<b>Resume Skills</b>",
            styles["Heading2"]
        )

    )

    story.append(

        Paragraph(
            ", ".join(result["resume_skills"]),
            styles["BodyText"]
        )

    )

    story.append(Spacer(1, 0.2 * inch))

    # ======================================================
    # Job Description Skills
    # ======================================================

    story.append(

        Paragraph(
            "<b>Job Description Skills</b>",
            styles["Heading2"]
        )

    )

    story.append(

        Paragraph(
            ", ".join(result["jd_skills"]),
            styles["BodyText"]
        )

    )

    story.append(Spacer(1, 0.2 * inch))

    # ======================================================
    # Matched Skills
    # ======================================================

    story.append(

        Paragraph(
            "<b>Matched Skills</b>",
            styles["Heading2"]
        )

    )

    story.append(

        Paragraph(
            ", ".join(result["matched_skills"]),
            styles["BodyText"]
        )

    )

    story.append(Spacer(1, 0.2 * inch))

    # ======================================================
    # Missing Skills
    # ======================================================

    story.append(

        Paragraph(
            "<b>Missing Skills</b>",
            styles["Heading2"]
        )

    )

    story.append(

        Paragraph(
            ", ".join(result["missing_skills"]),
            styles["BodyText"]
        )

    )

    story.append(Spacer(1, 0.3 * inch))

    # ======================================================
    # Gemini Analysis
    # ======================================================

    analysis = result["gemini_analysis"]

    story.append(

        Paragraph(
            "<b>Overall Feedback</b>",
            styles["Heading2"]
        )

    )

    story.append(

        Paragraph(
            analysis.get(
                "overall_feedback",
                "N/A"
            ),
            styles["BodyText"]
        )

    )

    sections = [

        ("Strengths", "strengths"),

        ("Missing Skill Analysis", "missing_skill_analysis"),

        ("Resume Improvements", "resume_improvements")

    ]

    for heading, key in sections:

        story.append(
            Spacer(1, 0.2 * inch)
        )

        story.append(

            Paragraph(
                f"<b>{heading}</b>",
                styles["Heading2"]
            )

        )

        for item in analysis.get(key, []):

            story.append(

                Paragraph(
                    f"• {item}",
                    styles["BodyText"]
                )

            )

    story.append(
        Spacer(1, 0.3 * inch)
    )

    story.append(

        Paragraph(
            "<b>Application Recommendation</b>",
            styles["Heading2"]
        )

    )

    story.append(

        Paragraph(

            analysis.get(

                "application_recommendation",

                "N/A"

            ),

            styles["BodyText"]

        )

    )

    story.append(
        Spacer(1, 0.5 * inch)
    )

    story.append(

        Paragraph(
            "<i>Generated by AI Interview Assistant</i>",
            styles["Italic"]
        )

    )

    doc.build(story)