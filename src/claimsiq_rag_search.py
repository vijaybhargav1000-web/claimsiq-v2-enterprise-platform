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

print("Question:", QUESTION)
print("Query vector dimensions:", len(query_vector))
print("Matches:", len(hits))

for hit in hits:
    claim = hit["_source"]
    print("Claim ID:", claim["claim_id"])
    print("Score:", hit["_score"])
    print("Claim:", claim["claim_text"])
    print("Risk:", claim["risk_level"])
    print("Priority:", claim["processing_priority"])
