import streamlit as st


def load_css():
    st.markdown(
        """
        <style>

        /* ===========================
           Main App
        =========================== */

        .main{
            background-color:#F5F7FB;
        }

        /* ===========================
           Headings
        =========================== */

        h1{
            color:#1F2937;
            font-weight:700;
        }

        h2{
            color:#1F2937;
            font-weight:600;
        }

        h3{
            color:#374151;
        }

        /* ===========================
           Metric Cards
        =========================== */

        .metric-card{

            background:white;

            padding:18px;

            border-radius:15px;

            border:1px solid #E5E7EB;

            box-shadow:0px 4px 12px rgba(0,0,0,0.05);

            text-align:center;

            margin-bottom:15px;
        }

        .metric-title{

            font-size:16px;

            color:#6B7280;

            font-weight:600;
        }

        .metric-value{

            font-size:34px;

            color:#2563EB;

            font-weight:bold;

            margin-top:10px;
        }

        /* ===========================
           Skill Badges
        =========================== */

        .skill-badge{

            display:inline-block;

            padding:8px 16px;

            margin:5px;

            border-radius:25px;

            background:#DBEAFE;

            color:#1D4ED8;

            font-weight:600;

            font-size:14px;
        }

        /* ===========================
           Review Cards
        =========================== */

        .review-card{
    background:#FFFFFF;
    color:#111827;
    border-left:6px solid #2563EB;
    padding:15px;
    margin-bottom:10px;
    border-radius:12px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.05);
    font-size:15px;
    line-height:1.6;
}

        /* ===========================
           Buttons
        =========================== */

        .stButton>button{

            width:100%;

            border-radius:10px;

            font-size:16px;

            font-weight:bold;

            padding:10px;

        }

        /* ===========================
           Upload Box
        =========================== */

        section[data-testid="stFileUploader"]{

            border-radius:15px;

        }

        </style>
        """,
        unsafe_allow_html=True
    )