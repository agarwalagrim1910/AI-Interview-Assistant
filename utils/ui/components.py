import streamlit as st
import plotly.graph_objects as go


# ==========================================================
# Section Title
# ==========================================================

def section_title(title):
    st.markdown(f"## {title}")


# ==========================================================
# Metric Card
# ==========================================================

def metric_card(title, value):
    st.metric(
        label=title,
        value=value
    )


# ==========================================================
# Skill Badges
# ==========================================================

def skill_badges(skills):
    if not skills:
        st.info("No skills found.")
        return

    html = ""

    for skill in skills:
        html += f"""
        <span class="skill-badge">
            {skill}
        </span>
        """

    st.markdown(html, unsafe_allow_html=True)


# ==========================================================
# Progress Card
# ==========================================================

def progress_card(title, score):
    st.markdown(f"**{title}**")
    st.progress(score / 100)

    if score >= 80:
        emoji = "🟢"
    elif score >= 60:
        emoji = "🟡"
    else:
        emoji = "🔴"

    st.caption(f"{emoji} {score}%")


# ==========================================================
# Generic Score Gauge
# ==========================================================

def score_gauge(score, title):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={
                "suffix": "%",
                "font": {"size": 42}
            },
            title={
                "text": title,
                "font": {"size": 22}
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "bar": {
                    "color": "#2563EB"
                },
                "steps": [
                    {
                        "range": [0, 50],
                        "color": "#FECACA"
                    },
                    {
                        "range": [50, 75],
                        "color": "#FDE68A"
                    },
                    {
                        "range": [75, 100],
                        "color": "#BBF7D0"
                    }
                ],
                "threshold": {
                    "line": {
                        "color": "#DC2626",
                        "width": 4
                    },
                    "value": score
                }
            }
        )
    )

    fig.update_layout(
        height=320,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================================
# Review Card
# ==========================================================

def review_card(title, items, icon):
    st.markdown(f"### {icon} {title}")

    if not items:
        st.info(f"No {title.lower()} available.")
        return

    for item in items:
        st.markdown(
            f"""
            <div class="review-card">
                {item}
            </div>
            """,
            unsafe_allow_html=True,
        )