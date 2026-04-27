import streamlit as st


def load_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: #0f172a;
            color: #f8fafc;
        }

        section[data-testid="stSidebar"] {
            background-color: #020617;
            border-right: 1px solid #1e293b;
        }

        h1, h2, h3 {
            color: #f8fafc;
            font-weight: 800;
        }

        .hero-card {
            background: linear-gradient(135deg, #064e3b 0%, #0f172a 55%, #1e293b 100%);
            padding: 36px;
            border-radius: 24px;
            border: 1px solid #334155;
            box-shadow: 0 18px 40px rgba(0,0,0,0.35);
            margin-bottom: 28px;
        }

        .hero-title {
            font-size: 44px;
            font-weight: 900;
            margin-bottom: 8px;
            color: #ffffff;
        }

        .hero-subtitle {
            font-size: 18px;
            color: #cbd5e1;
            max-width: 900px;
            line-height: 1.6;
        }

        .section-card {
            background: #111827;
            border: 1px solid #334155;
            border-radius: 20px;
            padding: 24px;
            margin-top: 20px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.20);
        }

        .tag {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(16, 185, 129, 0.15);
            color: #6ee7b7;
            border: 1px solid rgba(110, 231, 183, 0.35);
            font-size: 13px;
            margin-right: 8px;
            margin-bottom: 8px;
        }

        div[data-testid="stMetric"] {
            background: #111827;
            border: 1px solid #334155;
            padding: 18px;
            border-radius: 18px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.20);
        }

        div[data-testid="stMetricValue"] {
            color: #ffffff;
            font-size: 30px;
            font-weight: 900;
        }

        div[data-testid="stMetricLabel"] {
            color: #94a3b8;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )