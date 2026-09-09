import requests
import streamlit as st


# ============================================================
# ClaimsIQ Configuration
# ============================================================

API_URL = "http://127.0.0.1:8000/ask"


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

st.title("🤖 ClaimsIQ Enterprise AI Assistant")

st.write(
    "Ask questions about insurance claims."
)


# ============================================================
# Question Input
# ============================================================

question = st.text_input(
    "Ask a question",
    placeholder=(
        "Example: Find high risk health claims under review"
    ),
)


# ============================================================
# Ask Button
# ============================================================

if st.button("Ask", type="primary"):

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

            elif response.status_code == 400:

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
                "Could not connect to the ClaimsIQ API. "
                "Please make sure FastAPI is running on "
                "127.0.0.1:8000."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The ClaimsIQ API request timed out."
            )

        except requests.exceptions.RequestException as exc:

            st.error(
                f"API request failed: {exc}"
            )