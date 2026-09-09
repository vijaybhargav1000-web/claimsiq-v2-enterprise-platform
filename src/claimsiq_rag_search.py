import boto3
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

REGION = "ap-south-1"
AOSS_HOST = "316zxmoi289705x59odi.ap-south-1.aoss.amazonaws.com"
INDEX_NAME = "claimsiq-rag-index"

QUESTION = "Find high priority health claims under review"

# Load the same embedding model used during ingestion
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Generate query embedding
query_vector = model.encode(QUESTION).tolist()

print("Question:", QUESTION)
print("Query vector dimensions:", len(query_vector))

# AWS authentication
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, REGION, "aoss")

client = OpenSearch(
    hosts=[{"host": AOSS_HOST, "port": 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

# Semantic vector search
response = client.search(
    index=INDEX_NAME,
    body={
        "size": 3,
        "_source": [
            "claim_id",
            "claim_text",
            "claim_type",
            "region",
            "risk_level",
            "processing_priority"
        ],
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_vector,
                    "k": 3
                }
            }
        }
    }
)

hits = response["hits"]["hits"]

print("Matches:", len(hits))

for hit in hits:
    print("Claim ID:", hit["_source"]["claim_id"])
    print("Score:", hit["_score"])
    print("Claim:", hit["_source"]["claim_text"])
    print("Risk:", hit["_source"]["risk_level"])
    print("Priority:", hit["_source"]["processing_priority"])