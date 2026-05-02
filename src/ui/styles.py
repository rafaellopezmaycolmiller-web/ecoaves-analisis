import streamlit as st


def load_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(34, 197, 94, 0.12), transparent 30%),
                linear-gradient(135deg, #07111f 0%, #0f172a 48%, #101827 100%);
            color: #f8fafc;
        }

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(2, 6, 23, 0.98), rgba(4, 18, 28, 0.98));
            border-right: 1px solid rgba(148, 163, 184, 0.16);
        }

        section[data-testid="stSidebar"] h2 {
            color: #f8fafc;
            font-weight: 900;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span {
            color: #cbd5e1;
        }

        div[role="radiogroup"] label {
            padding: 0.55rem 0.65rem;
            border-radius: 14px;
            transition: all 0.2s ease;
        }

        div[role="radiogroup"] label:hover {
            background: rgba(34, 197, 94, 0.12);
        }

        .block-container {
            max-width: 1450px;
            padding-top: 2.2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: #f8fafc;
            letter-spacing: -0.035em;
        }

        h3 {
            margin-top: 1rem;
            margin-bottom: 0.8rem;
        }

        .clean-hero {
            border-radius: 30px;
            padding: 3.2rem;
            min-height: 330px;
            border: 1px solid rgba(148, 163, 184, 0.22);
            box-shadow: 0 28px 70px rgba(0, 0, 0, 0.28);
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            overflow: hidden;
        }

        .clean-hero h1 {
            font-size: 4.1rem;
            line-height: 1;
            margin: 0.6rem 0 0.3rem 0;
            font-weight: 900;
            color: #ffffff;
            letter-spacing: -0.065em;
        }

        .clean-hero h2 {
            font-size: 2.1rem;
            line-height: 1.15;
            max-width: 850px;
            color: #86efac;
            margin: 0 0 1.2rem 0;
            font-weight: 850;
            letter-spacing: -0.045em;
        }

        .clean-hero p {
            max-width: 900px;
            color: #dbeafe;
            font-size: 1.08rem;
            line-height: 1.7;
        }

        .hero-badge {
            width: fit-content;
            padding: 0.45rem 0.85rem;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.18);
            border: 1px solid rgba(134, 239, 172, 0.35);
            color: #bbf7d0;
            font-weight: 800;
            font-size: 0.88rem;
        }

        .clean-kpi {
            min-height: 135px;
            padding: 1.35rem;
            border-radius: 22px;
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.92), rgba(15, 37, 49, 0.68));
            border: 1px solid rgba(148, 163, 184, 0.22);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
            margin-bottom: 1rem;
        }

        .clean-kpi span {
            color: #cbd5e1;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .clean-kpi h3 {
            color: #ffffff;
            font-size: 2.6rem;
            margin: 0.35rem 0 0.25rem 0;
            letter-spacing: -0.05em;
        }

        .clean-kpi p {
            color: #86efac;
            margin: 0;
            font-size: 0.86rem;
            font-weight: 700;
        }

        .clean-kpi.highlight {
            border-color: rgba(134, 239, 172, 0.35);
            background: linear-gradient(145deg, rgba(22, 101, 52, 0.42), rgba(15, 23, 42, 0.86));
        }

        .module-card {
            min-height: 250px;
            padding: 1.5rem;
            border-radius: 26px;
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.22);
            box-shadow: 0 18px 42px rgba(0, 0, 0, 0.20);
            margin-bottom: 0.8rem;
        }

        .module-icon {
            width: 58px;
            height: 58px;
            display: grid;
            place-items: center;
            border-radius: 18px;
            background: rgba(34, 197, 94, 0.14);
            border: 1px solid rgba(134, 239, 172, 0.24);
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }

        .module-card h3 {
            color: #ffffff;
            font-size: 1.55rem;
            margin-bottom: 0.8rem;
        }

        .module-card p {
            color: #cbd5e1;
            line-height: 1.65;
        }

        .executive-card,
        .status-card {
            min-height: 230px;
            padding: 1.6rem;
            border-radius: 26px;
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.22);
            box-shadow: 0 18px 42px rgba(0, 0, 0, 0.18);
        }

        .executive-card h3,
        .status-card h3 {
            margin-top: 0;
            color: #ffffff;
        }

        .executive-card p {
            color: #cbd5e1;
            line-height: 1.75;
        }

        .status-line {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.85rem 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.16);
        }

        .status-line span {
            color: #cbd5e1;
        }

        .status-line b {
            color: #86efac;
        }

        .section-card {
            border-radius: 20px;
            padding: 1.2rem;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.20);
            margin-bottom: 1rem;
        }

        .section-card h3 {
            margin-top: 0;
            color: #ffffff;
        }

        .section-card p {
            color: #cbd5e1;
            line-height: 1.6;
        }

        .tag {
            display: inline-block;
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            margin-right: 0.35rem;
            margin-top: 0.35rem;
            color: #86efac;
            border: 1px solid rgba(134, 239, 172, 0.26);
            background: rgba(34, 197, 94, 0.12);
            font-size: 0.82rem;
            font-weight: 700;
        }

        .alert-card {
            border-radius: 18px;
            padding: 1rem 1.1rem;
            border: 1px solid rgba(148, 163, 184, 0.18);
            margin-bottom: 0.75rem;
            background: rgba(15, 23, 42, 0.76);
        }

        .alert-card h4 {
            margin: 0 0 0.45rem 0;
            color: #ffffff;
            font-size: 0.98rem;
        }

        .alert-card p {
            margin: 0;
            color: #cbd5e1;
            line-height: 1.45;
            font-size: 0.9rem;
        }

        .alert-card.critical {
            background: linear-gradient(135deg, rgba(127, 29, 29, 0.46), rgba(15, 23, 42, 0.72));
            border-color: rgba(248, 113, 113, 0.25);
        }

        .alert-card.warning {
            background: linear-gradient(135deg, rgba(113, 63, 18, 0.42), rgba(15, 23, 42, 0.72));
            border-color: rgba(253, 224, 71, 0.22);
        }

        .alert-card.info {
            background: linear-gradient(135deg, rgba(30, 64, 175, 0.38), rgba(15, 23, 42, 0.72));
            border-color: rgba(96, 165, 250, 0.22);
        }

        .species-row {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.62rem 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.14);
        }

        .species-dot {
            width: 34px;
            height: 34px;
            display: grid;
            place-items: center;
            background: rgba(34, 197, 94, 0.14);
            border-radius: 999px;
        }

        .species-info {
            flex: 1;
            min-width: 0;
        }

        .species-info strong {
            color: #f8fafc;
            font-size: 0.9rem;
        }

        .bar-bg {
            margin-top: 0.35rem;
            height: 7px;
            background: rgba(148, 163, 184, 0.18);
            border-radius: 999px;
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #22c55e, #a3e635);
            border-radius: 999px;
        }

        .species-row span {
            color: #86efac;
            font-weight: 800;
        }

        .system-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
        }

        .system-grid div {
            padding: 0.9rem;
            border-radius: 16px;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.18);
            text-align: center;
            color: #f8fafc;
        }

        .system-grid span {
            color: #86efac;
            font-size: 0.8rem;
            font-weight: 700;
        }

        [data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
        }

        .stButton > button,
        .stDownloadButton > button {
            min-height: 48px;
            border-radius: 16px;
            border: 1px solid rgba(134, 239, 172, 0.28);
            background: linear-gradient(135deg, #166534, #0f766e);
            color: white;
            font-weight: 800;
            padding: 0.65rem 1.1rem;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: rgba(187, 247, 208, 0.65);
            color: white;
            filter: brightness(1.08);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )