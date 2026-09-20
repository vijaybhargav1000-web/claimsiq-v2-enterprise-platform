import os

import requests
import streamlit as st


# ============================================================
# ClaimsIQ Configuration
# ============================================================

API_URL = os.getenv(
    "CLAIMSIQ_API_URL",
    "http://127.0.0.1:8000/ask",
)

DECISION_API_URL = API_URL.rsplit("/", 1)[0] + "/decision"


# ============================================================
# Streamlit Page Configuration
# ============================================================

st.set_page_config(
    page_title="ClaimsIQ AI",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# Header
# ============================================================

st.title("🤖 ClaimsIQ Enterprise AI Platform")

st.write(
    "AI-powered claims search and deterministic claims decisioning."
)


# ============================================================
# Tabs
# ============================================================

search_tab, decision_tab, audit_tab = st.tabs(
    [
        "🔎 AI Claims Search",
        "⚖️ Claim Decisioning",
        "📋 Audit History",
    ]
)


# ============================================================
# AI Claims Search
# ============================================================

with search_tab:

    st.subheader("Ask ClaimsIQ")

    question = st.text_input(
        "Ask a question",
        placeholder=(
            "Example: Find high risk health claims under review"
        ),
        key="claims_question",
    )

    if st.button(
        "Ask",
        type="primary",
        key="ask_button",
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            try:

                with st.spinner(
                    "Searching ClaimsIQ knowledge..."
                ):

                    response = requests.post(
                        API_URL,
                        json={
                            "question": question
                        },
                        timeout=120,
                    )

                # ------------------------------------------------
                # Successful API response
                # ------------------------------------------------

                if response.status_code == 200:

                    result = response.json()

                    # ============================================
                    # Verified Answer
                    # ============================================

                    st.success("Verified Answer")

                    st.write(
                        result["answer"]
                    )

                    # ============================================
                    # Query Interpretation
                    # ============================================

                    st.subheader(
                        "🔎 Query Interpretation"
                    )

                    filters = result["filters"]

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Claim Type",
                            filters["claim_type"] or "ANY",
                        )

                    with col2:
                        st.metric(
                            "Risk Level",
                            filters["risk_level"] or "ANY",
                        )

                    with col3:
                        st.metric(
                            "Priority",
                            filters["processing_priority"]
                            or "ANY",
                        )

                    col4, col5 = st.columns(2)

                    with col4:
                        st.metric(
                            "Status",
                            filters["status"] or "ANY",
                        )

                    with col5:
                        st.metric(
                            "Region",
                            filters["region"] or "ANY",
                        )

                    # ============================================
                    # Retrieval Summary
                    # ============================================

                    st.subheader(
                        "📊 Retrieval Summary"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Retrieved Claims",
                            result["retrieved_count"],
                        )

                    with col2:
                        st.metric(
                            "Matching Claims",
                            result["matching_count"],
                        )

                    # ============================================
                    # Matching Claims
                    # ============================================

                    st.subheader(
                        "📋 Matching Claims"
                    )

                    claims = result["claims"]

                    if claims:

                        for claim in claims:

                            with st.container(
                                border=True
                            ):

                                st.markdown(
                                    f"### {claim['claim_id']}"
                                )

                                col1, col2, col3 = st.columns(3)

                                with col1:

                                    st.write(
                                        "**Claim Type**"
                                    )

                                    st.write(
                                        claim["claim_type"]
                                    )

                                    st.write(
                                        "**Region**"
                                    )

                                    st.write(
                                        claim["region"]
                                    )

                                with col2:

                                    st.write(
                                        "**Risk Level**"
                                    )

                                    st.write(
                                        claim["risk_level"]
                                    )

                                    st.write(
                                        "**Priority**"
                                    )

                                    st.write(
                                        claim[
                                            "processing_priority"
                                        ]
                                    )

                                with col3:

                                    st.write(
                                        "**Status**"
                                    )

                                    st.write(
                                        claim["status"]
                                    )

                                st.write(
                                    "**Details**"
                                )

                                st.write(
                                    claim["claim_text"]
                                )

                    else:

                        st.info(
                            "No matching claims found."
                        )

                    # ============================================
                    # Source of Truth
                    # ============================================

                    st.subheader(
                        "🔐 Source of Truth"
                    )

                    st.info(
                        result["source_of_truth"]
                    )

                # ------------------------------------------------
                # API validation error
                # ------------------------------------------------

                elif response.status_code in (400, 422):

                    try:

                        detail = response.json().get(
                            "detail",
                            "Invalid request.",
                        )

                    except ValueError:

                        detail = response.text

                    st.warning(detail)

                # ------------------------------------------------
                # API server error
                # ------------------------------------------------

                else:

                    st.error(
                        "ClaimsIQ API returned an error."
                    )

                    st.code(
                        response.text
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the ClaimsIQ API."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The ClaimsIQ API request timed out."
                )

            except requests.exceptions.RequestException as exc:

                st.error(
                    f"API request failed: {exc}"
                )


# ============================================================
# Claim Decisioning
# ============================================================

with decision_tab:

    st.subheader("⚖️ Deterministic Claim Decisioning")

    st.write(
        "Evaluate a Gold-layer claim using the ClaimsIQ "
        "deterministic decision engine."
    )

    claim_id = st.text_input(
        "Claim ID",
        placeholder="Example: CLM-2026-0005",
        key="decision_claim_id",
    )

    if st.button(
        "Evaluate Claim",
        type="primary",
        key="decision_button",
    ):

        if not claim_id.strip():

            st.warning(
                "Please enter a Claim ID."
            )

        else:

            try:

                with st.spinner(
                    "Evaluating claim..."
                ):

                    response = requests.post(
                        DECISION_API_URL,
                        json={
                            "claim_id": claim_id.strip()
                        },
                        timeout=30,
                    )

                # ------------------------------------------------
                # Successful decision
                # ------------------------------------------------

                if response.status_code == 200:

                    result = response.json()

                    decision = result["decision"]

                    # ============================================
                    # Decision
                    # ============================================

                    st.success(
                        f"Decision: {decision}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Claim ID",
                            result["claim_id"],
                        )

                    with col2:

                        st.metric(
                            "Decision Version",
                            result["decision_version"],
                        )

                    # ============================================
                    # Reason Codes
                    # ============================================

                    st.subheader(
                        "🏷️ Reason Codes"
                    )

                    reason_codes = result.get(
                        "reason_codes",
                        [],
                    )

                    if reason_codes:

                        for code in reason_codes:

                            st.code(
                                code,
                                language="text",
                            )

                    else:

                        st.info(
                            "No decision reason codes were triggered."
                        )

                    # ============================================
                    # Explainability
                    # ============================================

                    st.subheader(
                        "🧠 Decision Explanation"
                    )

                    reasons = result.get(
                        "reasons",
                        [],
                    )

                    if reasons:

                        for reason in reasons:

                            st.write(
                                f"• {reason}"
                            )

                    else:

                        st.info(
                            "No additional explanation available."
                        )

                # ------------------------------------------------
                # Claim not found
                # ------------------------------------------------

                elif response.status_code == 404:

                    try:

                        detail = response.json().get(
                            "detail",
                            "Claim not found.",
                        )

                    except ValueError:

                        detail = response.text

                    st.warning(detail)

                # ------------------------------------------------
                # Other API errors
                # ------------------------------------------------

                else:

                    st.error(
                        "ClaimsIQ decision API returned an error."
                    )

                    st.code(
                        response.text
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the ClaimsIQ API."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The ClaimsIQ decision request timed out."
                )

            except requests.exceptions.RequestException as exc:

                st.error(
                    f"API request failed: {exc}"
                )

# ============================================================
# Audit History
# ============================================================

with audit_tab:

    st.subheader("📋 ClaimsIQ Decision Audit History")

    st.write(
        "Review persisted decision events generated by the "
        "ClaimsIQ deterministic decision engine."
    )

    if st.button(
        "Refresh Audit History",
        type="primary",
        key="audit_refresh_button",
    ):

        try:

            with st.spinner("Loading audit history..."):

                audit_url = API_URL.rsplit("/", 1)[0] + "/audit"

                response = requests.get(
                    audit_url,
                    timeout=30,
                )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    f"Audit history loaded: {result['count']} event(s)"
                )

                records = result.get("records", [])

                if records:

                    for record in reversed(records):

                        with st.container(border=True):

                            st.markdown(
                                f"### {record.get('claim_id', 'UNKNOWN')}"
                            )

                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.write("**Decision**")
                                st.write(
                                    record.get("decision", "UNKNOWN")
                                )

                            with col2:
                                st.write("**Decision Version**")
                                st.write(
                                    record.get(
                                        "decision_version",
                                        "UNKNOWN",
                                    )
                                )

                            with col3:
                                st.write("**Timestamp**")
                                st.write(
                                    record.get(
                                        "timestamp",
                                        "UNKNOWN",
                                    )
                                )

                            st.write("**Reason Codes**")

                            reason_codes = record.get(
                                "reason_codes",
                                [],
                            )

                            if reason_codes:

                                for code in reason_codes:
                                    st.code(
                                        code,
                                        language="text",
                                    )

                            else:
                                st.info(
                                    "No decision reason codes."
                                )

                            st.write("**Decision Explanation**")

                            reasons = record.get(
                                "reasons",
                                [],
                            )

                            if reasons:

                                for reason in reasons:
                                    st.write(
                                        f"• {reason}"
                                    )

                            else:
                                st.info(
                                    "No additional explanation available."
                                )

                            st.write("**Decision Source**")

                            st.code(
                                record.get(
                                    "decision_source",
                                    "UNKNOWN",
                                ),
                                language="text",
                            )

                else:

                    st.info(
                        "No decision audit events found."
                    )

            else:

                st.error(
                    "ClaimsIQ audit API returned an error."
                )

                st.code(
                    response.text
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the ClaimsIQ API."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The ClaimsIQ audit request timed out."
            )

        except requests.exceptions.RequestException as exc:

            st.error(
                f"Audit API request failed: {exc}"
            )