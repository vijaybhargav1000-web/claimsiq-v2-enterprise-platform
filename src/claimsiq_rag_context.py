import boto3
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

from config.settings import (
    AWS_REGION,
    AOSS_HOST,
    AOSS_INDEX_NAME,
    EMBEDDING_MODEL,
)

QUESTION = "Find high priority health claims under review"

model = SentenceTransformer(EMBEDDING_MODEL)

query_vector = model.encode(QUESTION).tolist()

credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, AWS_REGION, "aoss")

client = OpenSearch(
    hosts=[{"host": AOSS_HOST, "port": 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

response = client.search(
    index=AOSS_INDEX_NAME,
    body={
        "size": 3,
        "_source": [
            "claim_id",
            "claim_text",
            "claim_type",
            "region",
            "risk_level",
            "processing_priority",
        ],
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_vector,
                    "k": 3,
                }
            }
        },
    },
)

hits = response["hits"]["hits"]

context_parts = []

for i, hit in enumerate(hits, start=1):
    claim = hit["_source"]

    context_parts.append(
        f"""Claim {i}
Claim ID: {claim["claim_id"]}
Claim Type: {claim["claim_type"]}
Region: {claim["region"]}
Risk Level: {claim["risk_level"]}
Processing Priority: {claim["processing_priority"]}
Details: {claim["claim_text"]}"""
    )

context = "\n\n".join(context_parts)

print("=" * 70)
print("USER QUESTION")
print("=" * 70)
print(QUESTION)

print("\n" + "=" * 70)
print("RETRIEVED CONTEXT")
print("=" * 70)
print(context)

print("\n" + "=" * 70)
print("CONTEXT READY FOR GENERATION")
print("=" * 70)
