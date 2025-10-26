import os, requests, streamlit as st

API = os.getenv("API_BASE", "http://api:8000")

st.title("📈 Twelve Insight Dashboard")
ticker = st.text_input("Enter ticker:", "AAPL")

cols = st.columns(2)
with cols[0]:
    if st.button("Get Latest"):
        r = requests.get(f"{API}/latest", params={"ticker": ticker}).json()
        st.json(r)
with cols[1]:
    if st.button("Get Trend"):
        r = requests.get(f"{API}/trend", params={"ticker": ticker, "window": 100}).json()
        st.json(r)
