import boto3
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

REGION = "ap-south-1"
AOSS_HOST = "316zxmoi289705x59odi.ap-south-1.aoss.amazonaws.com"
INDEX_NAME = "claimsiq-rag-index"

QUESTION = "Find high priority health claims under review"

# 1. Load the same embedding model used for the indexed claims
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 2. Convert the user's question into a vector
query_vector = model.encode(QUESTION).tolist()

# 3. Authenticate to OpenSearch Serverless
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, REGION, "aoss")

client = OpenSearch(
    hosts=[{"host": AOSS_HOST, "port": 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

# 4. Retrieve the top 3 semantically relevant claims
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

# 5. Build grounded context
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