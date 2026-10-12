"""Streamlit review-first agent console."""
import os
import requests
import streamlit as st

st.set_page_config(page_title="Coding Agent Control Center", layout="wide")
st.title("Autonomous Coding Agent · Review Console")
st.caption("Issue investigation · Code retrieval · Open-weight model proposal · Human review")
st.warning("Prototype: does not modify code, run untrusted tests, or submit GitHub PRs.")
api = os.getenv("API_URL", "http://localhost:8000")
title = st.text_input("Issue title", "Fix zero-value handling")
details = st.text_area("Issue body", "The calculator should correctly return 0 when the input is zero.")
if st.button("Investigate"):
    try:
        response = requests.post(api + "/api/issues/analyze",
                                 json={"title": title, "description": details}, timeout=130)
        response.raise_for_status()
        result = response.json()
        st.subheader("Relevant code")
        st.json(result["evidence"])
        st.subheader("Proposed repair")
        st.write(result["recommendation"]["proposal"])
        st.info("Human approval required; no changes applied.")
    except requests.RequestException as exc:
        st.error(str(exc))
