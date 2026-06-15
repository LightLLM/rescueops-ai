import pandas as pd
import streamlit as st

from agent import analyze_incident
from splunk_client import SplunkClient

st.set_page_config(page_title="RescueOps AI", page_icon="🚨", layout="wide")

st.title("🚨 RescueOps AI")
st.subheader("Agentic Incident Commander for Splunk")

st.markdown(
    """
RescueOps AI investigates incidents using Splunk data and generates a timeline,
root-cause hypothesis, recommended actions, and postmortem draft.

**Demo scenario:** an e-commerce checkout outage occurs shortly after deployment `v2.3.1`.
"""
)

with st.sidebar:
    st.header("Demo Controls")
    st.caption("Make sure your Splunk `.env` settings are configured and the synthetic logs are uploaded to index `rescueops`.")
    run = st.button("Run AI Incident Investigation", type="primary")

if "results" not in st.session_state:
    st.session_state.results = None

if run:
    try:
        with st.spinner("Querying Splunk and running incident agents..."):
            splunk = SplunkClient()
            error_summary = splunk.incident_error_summary()
            timeline = splunk.incident_timeline()
            deployments = splunk.deployment_events()
            latency = splunk.high_latency_services()

            analysis = analyze_incident(
                error_summary=error_summary,
                timeline=timeline,
                deployment_events=deployments,
                latency_services=latency,
            )

            st.session_state.results = {
                "error_summary": error_summary,
                "timeline": timeline,
                "deployments": deployments,
                "latency": latency,
                "analysis": analysis,
            }
    except Exception as exc:
        st.error("Could not connect to Splunk or run searches. Check `.env`, Splunk status, and uploaded data.")
        st.exception(exc)

if st.session_state.results:
    results = st.session_state.results
    analysis = results["analysis"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Incident Status", "Active")
    col2.metric("RCA Confidence", analysis["confidence"])
    col3.metric("Primary Service", analysis["summary"].split(" ")[0])

    st.divider()
    st.header("AI Incident Summary")
    st.success(analysis["summary"])

    st.header("Likely Root Cause")
    st.warning(analysis["root_cause"])

    st.header("Recommended Human-Approved Actions")
    for action in analysis["recommendations"]:
        st.checkbox(action, value=False)

    st.divider()
    st.header("Splunk Evidence")
    tab1, tab2, tab3, tab4 = st.tabs(["Error Summary", "Timeline", "Deployment Events", "Latency"])

    with tab1:
        st.dataframe(pd.DataFrame(results["error_summary"]), use_container_width=True)
    with tab2:
        st.dataframe(pd.DataFrame(results["timeline"]), use_container_width=True)
    with tab3:
        st.dataframe(pd.DataFrame(results["deployments"]), use_container_width=True)
    with tab4:
        st.dataframe(pd.DataFrame(results["latency"]), use_container_width=True)

    st.divider()
    st.header("Postmortem Draft")
    st.code(analysis["postmortem"], language="markdown")
else:
    st.info("Click **Run AI Incident Investigation** in the sidebar after uploading the dataset into Splunk.")
