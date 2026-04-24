import os

import requests
import streamlit as st

# -----------------------------
# CONFIG
# -----------------------------
# Priority:
# 1. Streamlit secrets
# 2. Environment variable (Docker / Railway / Production)
# 3. Fallback to production API

DEFAULT_API_BASE_URL = "https://iseo-api.ai-coach-lab.com"

try:
    API_BASE_URL = st.secrets.get(
        "API_BASE_URL",
        os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL),
    ).rstrip("/")
except Exception:
    API_BASE_URL = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")

st.set_page_config(
    page_title="ISEO Dashboard",
    page_icon="🛡️",
    layout="wide",
)

# -----------------------------
# GLOBAL STYLES
# -----------------------------
st.markdown(
    """
    <style>
    div.stButton > button {
        background: linear-gradient(90deg, #ff4b4b, #ff6b6b);
        color: white;
        font-weight: 700;
        border-radius: 10px;
        height: 3em;
        border: none;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #ff6b6b, #ff4b4b);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# HELPER FUNCTION
# -----------------------------
def show_api_error(response):
    st.error(f"API Error: {response.status_code}")
    try:
        st.code(response.text)
    except Exception:
        st.write("No error details returned by API.")
    st.stop()


# -----------------------------
# SIDEBAR + LOGO
# -----------------------------
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

with st.sidebar:
    if os.path.exists(logo_path):
        st.image(logo_path, width=140)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.header("Configuration")

    api_base_url = st.text_input("API Base URL", value=API_BASE_URL).rstrip("/")
    top_k = st.number_input("Top K", min_value=1, max_value=10, value=3)
    actor = st.text_input("Actor", value="streamlit_user")

    st.divider()
    st.subheader("Quick Checks")

    if st.button("Check Health"):
        try:
            res = requests.get(f"{api_base_url}/health", timeout=15)

            if res.status_code != 200:
                show_api_error(res)

            st.success("API is healthy")
            st.json(res.json())

        except Exception as e:
            st.error(f"Health check failed: {e}")

# -----------------------------
# HEADER
# -----------------------------
st.title("ISEO - Intrinsic Safety and Ethics Optimizer")
st.caption(
    "Safety-aware AI orchestration with retrieval, grounded reasoning, policy enforcement, and evaluation."
)
st.divider()

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3 = st.tabs(["Run ISEO", "Evaluation", "API Debug"])

# =========================================================
# TAB 1 - RUN ISEO
# =========================================================
with tab1:
    st.subheader("Run Safety-Aware AI Flow")

    question = st.text_area(
        "Question",
        value="What is ISEO?",
        height=120,
    )

    if st.button("Run ISEO", use_container_width=True):
        payload = {
            "question": question,
            "actor": actor,
            "top_k": int(top_k),
        }

        try:
            with st.spinner("Running ISEO pipeline..."):
                res = requests.post(
                    f"{api_base_url}/iseo/run",
                    json=payload,
                    timeout=90,
                )

                if res.status_code != 200:
                    show_api_error(res)

                data = res.json()

            st.success("ISEO completed successfully")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Status", data.get("status", "N/A"))
            c2.metric("Risk", data.get("safety", {}).get("risk_level", "N/A"))
            c3.metric("Decision", data.get("safety", {}).get("decision", "N/A"))
            c4.metric("Score", data.get("safety", {}).get("risk_score", "N/A"))

            st.markdown("### Answer")
            st.write(data.get("answer", "No answer returned."))

            st.markdown("### Safety Assessment")
            st.json(data.get("safety", {}))

            st.markdown("### Execution Plan")
            steps = data.get("plan", {}).get("steps", [])
            if steps:
                for step in steps:
                    step_number = step.get("step_number", "-")
                    action = step.get("action", "No action returned")
                    purpose = step.get("purpose", "")

                    st.write(f"{step_number}: {action}")
                    if purpose:
                        st.caption(purpose)
            else:
                st.info("No plan steps returned.")

            st.markdown("### Citations")
            citations = data.get("citations", [])
            if citations:
                for c in citations:
                    with st.expander(c.get("title", "source")):
                        st.write(c.get("snippet", "No snippet returned."))
            else:
                st.info("No citations returned.")

            st.markdown("### Context Blocks")
            context_blocks = data.get("context_blocks", [])
            if context_blocks:
                for idx, block in enumerate(context_blocks, start=1):
                    with st.expander(f"Context Block {idx}"):
                        st.code(block)
            else:
                st.info("No context blocks returned.")

            st.markdown("### Raw JSON")
            st.json(data)

        except Exception as e:
            st.error(f"ISEO run failed: {e}")

# =========================================================
# TAB 2 - EVALUATION
# =========================================================
with tab2:
    st.subheader("Evaluation")

    if st.button("Run Evaluation"):
        try:
            with st.spinner("Running evaluation suite..."):
                res = requests.post(
                    f"{api_base_url}/evaluation/run",
                    params={"top_k": int(top_k)},
                    timeout=90,
                )

                if res.status_code != 200:
                    show_api_error(res)

                st.success("Evaluation completed successfully")
                st.json(res.json())

        except Exception as e:
            st.error(f"Evaluation failed: {e}")

    if st.button("Load Metrics"):
        try:
            res = requests.get(f"{api_base_url}/evaluation/metrics", timeout=30)

            if res.status_code != 200:
                show_api_error(res)

            st.success("Loaded latest metrics")
            st.json(res.json())

        except Exception as e:
            st.error(f"Metrics load failed: {e}")

    if st.button("Load Report"):
        try:
            res = requests.get(f"{api_base_url}/evaluation/report", timeout=30)

            if res.status_code != 200:
                show_api_error(res)

            st.success("Loaded latest report")
            st.json(res.json())

        except Exception as e:
            st.error(f"Report load failed: {e}")

# =========================================================
# TAB 3 - DEBUG
# =========================================================
with tab3:
    st.subheader("Debug")

    if st.button("Ingest Sample"):
        sample = {
            "docs": [
                {
                    "source": "local",
                    "title": "ISEO intro",
                    "content": "ISEO evaluates safety and ethics before answering.",
                }
            ]
        }

        try:
            res = requests.post(
                f"{api_base_url}/rag/ingest",
                json=sample,
                timeout=90,
            )

            if res.status_code != 200:
                show_api_error(res)

            st.success("Sample document ingested successfully")
            st.json(res.json())

        except Exception as e:
            st.error(f"Ingest failed: {e}")

    q = st.text_input("Retrieve Question", "What is ISEO?")

    if st.button("Retrieve"):
        try:
            res = requests.post(
                f"{api_base_url}/rag/retrieve",
                json={"question": q, "top_k": int(top_k)},
                timeout=90,
            )

            if res.status_code != 200:
                show_api_error(res)

            st.success("Retrieve completed successfully")
            st.json(res.json())

        except Exception as e:
            st.error(f"Retrieve failed: {e}")
