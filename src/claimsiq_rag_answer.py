import sys

import boto3
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


# ============================================================
# ClaimsIQ Configuration
# ============================================================

REGION = "ap-south-1"
AOSS_HOST = "316zxmoi289705x59odi.ap-south-1.aoss.amazonaws.com"
INDEX_NAME = "claimsiq-rag-index"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# ============================================================
# Cached application resources
# ============================================================

_embedding_model = None
_opensearch_client = None


def get_embedding_model():
    """
    Load the embedding model once and reuse it.
    """

    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    return _embedding_model


def get_opensearch_client():
    """
    Create the authenticated OpenSearch Serverless
    client once and reuse it.
    """

    global _opensearch_client

    if _opensearch_client is None:

        credentials = boto3.Session().get_credentials()

        if credentials is None:
            raise RuntimeError(
                "AWS credentials were not found."
            )

        auth = AWSV4SignerAuth(
            credentials,
            REGION,
            "aoss"
        )

        _opensearch_client = OpenSearch(
            hosts=[
                {
                    "host": AOSS_HOST,
                    "port": 443
                }
            ],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )

    return _opensearch_client


# ============================================================
# Business filter parser
# ============================================================

def parse_business_filters(question):
    """
    Convert supported natural-language business criteria
    into deterministic structured filters.
    """

    text = question.upper()

    filters = {
        "claim_type": None,
        "risk_level": None,
        "processing_priority": None,
        "status": None,
        "region": None,
    }

    # --------------------------------------------------------
    # Claim type
    # --------------------------------------------------------

    claim_types = [
        "HEALTH",
        "AUTO",
        "HOME",
        "TRAVEL",
    ]

    for claim_type in claim_types:

        if claim_type in text:
            filters["claim_type"] = claim_type
            break

    # --------------------------------------------------------
    # Risk level
    # --------------------------------------------------------

    if "HIGH RISK" in text:

        filters["risk_level"] = "HIGH"

    elif "MEDIUM RISK" in text:

        filters["risk_level"] = "MEDIUM"

    elif "LOW RISK" in text:

        filters["risk_level"] = "LOW"

    # --------------------------------------------------------
    # Processing priority
    # --------------------------------------------------------

    if "HIGH PRIORITY" in text:

        filters["processing_priority"] = "HIGH"

    elif "MEDIUM PRIORITY" in text:

        filters["processing_priority"] = "MEDIUM"

    elif "LOW PRIORITY" in text:

        filters["processing_priority"] = "LOW"

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    if (
        "UNDER REVIEW" in text
        or "UNDER_REVIEW" in text
    ):

        filters["status"] = "UNDER_REVIEW"

    # --------------------------------------------------------
    # Region
    # --------------------------------------------------------

    regions = [
        "IN-SOUTH",
        "IN-WEST",
        "IN-NORTH",
        "IN-EAST",
    ]

    for region in regions:

        if region in text:
            filters["region"] = region
            break

    return filters


# ============================================================
# Deterministic claim matching
# ============================================================

def matches_business_filters(claim, filters):
    """
    Apply deterministic business rules to a retrieved claim.
    """

    claim_type = str(
        claim.get("claim_type", "")
    ).upper()

    risk_level = str(
        claim.get("risk_level", "")
    ).upper()

    processing_priority = str(
        claim.get("processing_priority", "")
    ).upper()

    status = str(
        claim.get("status", "")
    ).upper()

    region = str(
        claim.get("region", "")
    ).upper()

    if (
        filters["claim_type"] is not None
        and claim_type != filters["claim_type"]
    ):
        return False

    if (
        filters["risk_level"] is not None
        and risk_level != filters["risk_level"]
    ):
        return False

    if (
        filters["processing_priority"] is not None
        and processing_priority
        != filters["processing_priority"]
    ):
        return False

    if (
        filters["status"] is not None
        and status != filters["status"]
    ):
        return False

    if (
        filters["region"] is not None
        and region != filters["region"]
    ):
        return False

    return True


# ============================================================
# ClaimsIQ RAG engine
# ============================================================

def ask_claimsiq(question):
    """
    Execute the ClaimsIQ retrieval and deterministic
    business-rule validation pipeline.

    Returns a structured response suitable for an API/UI.
    """

    if not isinstance(question, str):
        raise ValueError(
            "Question must be a string."
        )

    question = question.strip()

    if not question:
        raise ValueError(
            "Question cannot be empty."
        )

    # --------------------------------------------------------
    # 1. Interpret business filters
    # --------------------------------------------------------

    filters = parse_business_filters(question)

    # --------------------------------------------------------
    # 2. Generate query embedding
    # --------------------------------------------------------

    embedding_model = get_embedding_model()

    query_vector = embedding_model.encode(
        question
    ).tolist()

    if len(query_vector) != 384:
        raise RuntimeError(
            "Unexpected embedding dimensions: "
            f"{len(query_vector)}"
        )

    # --------------------------------------------------------
    # 3. Retrieve semantically relevant claims
    # --------------------------------------------------------

    client = get_opensearch_client()

    response = client.search(
        index=INDEX_NAME,
        body={
            "size": 5,
            "_source": [
                "claim_id",
                "claim_text",
                "claim_type",
                "region",
                "risk_level",
                "processing_priority",
                "status",
            ],
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_vector,
                        "k": 5,
                    }
                }
            },
        },
    )

    hits = response["hits"]["hits"]

    # --------------------------------------------------------
    # 4. Deterministic business validation
    # --------------------------------------------------------

    matching_claims = []

    for hit in hits:

        claim = hit["_source"]

        if matches_business_filters(
            claim,
            filters
        ):
            matching_claims.append(claim)

    # --------------------------------------------------------
    # 5. Build authoritative answer
    # --------------------------------------------------------

    if matching_claims:

        answer = (
            f"Found {len(matching_claims)} "
            "matching claims."
        )

    else:

        answer = (
            "No claims matched the interpreted "
            "business criteria."
        )

    # --------------------------------------------------------
    # 6. Return structured result
    # --------------------------------------------------------

    return {
        "question": question,
        "filters": filters,
        "retrieved_count": len(hits),
        "matching_count": len(matching_claims),
        "answer": answer,
        "claims": matching_claims,
        "llm_narrative": None,
        "source_of_truth": (
            "deterministic_business_rules"
        ),
    }


# ============================================================
# CLI mode
#
# This preserves the ability to run the script directly
# while preventing execution during import.
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) > 1:

        question = " ".join(
            sys.argv[1:]
        ).strip()

    else:

        question = input(
            "ClaimsIQ question: "
        ).strip()

    result = ask_claimsiq(question)

    print("\n" + "=" * 70)
    print("CLAIMSIQ VERIFIED BUSINESS ANSWER")
    print("=" * 70)

    print(result["answer"])

    print(
        "\nQuery interpretation:"
    )

    for key, value in result["filters"].items():

        print(
            f"{key}: "
            f"{value or 'ANY'}"
        )

    print(
        "\nRetrieved claims:",
        result["retrieved_count"]
    )

    print(
        "Matching claims:",
        result["matching_count"]
    )

    print(
        "\nVerified sources:"
    )

    for claim in result["claims"]:

        print(
            f'- {claim["claim_id"]} | '
            f'{claim["claim_type"]} | '
            f'{claim["region"]} | '
            f'Risk={claim["risk_level"]} | '
            f'Priority={claim["processing_priority"]} | '
            f'Status={claim["status"]}'
        )