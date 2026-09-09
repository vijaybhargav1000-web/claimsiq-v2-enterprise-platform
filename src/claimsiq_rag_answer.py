import boto3
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from transformers import AutoTokenizer, AutoModelForCausalLM

# ============================================================
# ClaimsIQ Configuration
# ============================================================

REGION = "ap-south-1"
AOSS_HOST = "316zxmoi289705x59odi.ap-south-1.aoss.amazonaws.com"
INDEX_NAME = "claimsiq-rag-index"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GENERATION_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

QUESTION = "Find high priority health claims under review"


# ============================================================
# 1. Load embedding model
# ============================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(EMBEDDING_MODEL)


# ============================================================
# 2. Create query embedding
# ============================================================

query_vector = embedding_model.encode(QUESTION).tolist()

print("Query vector dimensions:", len(query_vector))


# ============================================================
# 3. Connect to OpenSearch Serverless
# ============================================================

print("Connecting to OpenSearch Serverless...")

credentials = boto3.Session().get_credentials()

auth = AWSV4SignerAuth(
    credentials,
    REGION,
    "aoss"
)

client = OpenSearch(
    hosts=[{"host": AOSS_HOST, "port": 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)


# ============================================================
# 4. Semantic retrieval
# ============================================================

print("Searching ClaimsIQ knowledge...")

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
            "processing_priority"
        ],
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_vector,
                    "k": 5
                }
            }
        }
    }
)

hits = response["hits"]["hits"]

print("Retrieved claims:", len(hits))


# ============================================================
# 5. Business-rule validation
# ============================================================

matching_claims = []

for hit in hits:

    claim = hit["_source"]

    claim_type = str(claim.get("claim_type", "")).upper()
    processing_priority = str(
        claim.get("processing_priority", "")
    ).upper()

    claim_text = str(
        claim.get("claim_text", "")
    ).upper()

    # The current question requires:
    # HEALTH + UNDER_REVIEW + HIGH priority

    is_health = claim_type == "HEALTH"
    is_high_priority = processing_priority == "HIGH"
    is_under_review = "UNDER_REVIEW" in claim_text

    if is_health and is_under_review and is_high_priority:
        matching_claims.append(claim)


# ============================================================
# 6. Display validation result
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS RULE VALIDATION")
print("=" * 70)

print("Required claim type: HEALTH")
print("Required status: UNDER_REVIEW")
print("Required priority: HIGH")

print("\nMatching claims:", len(matching_claims))

for claim in matching_claims:

    print(
        f'{claim["claim_id"]} | '
        f'{claim["claim_type"]} | '
        f'{claim["region"]} | '
        f'Risk={claim["risk_level"]} | '
        f'Priority={claim["processing_priority"]}'
    )


# ============================================================
# 7. Build verified context for the LLM
# ============================================================

if matching_claims:

    context_parts = []

    for claim in matching_claims:

        context_parts.append(
            f"""
Claim ID: {claim["claim_id"]}
Claim Type: {claim["claim_type"]}
Region: {claim["region"]}
Risk Level: {claim["risk_level"]}
Processing Priority: {claim["processing_priority"]}
Details: {claim["claim_text"]}
"""
        )

    verified_context = "\n".join(context_parts)

else:

    verified_context = "No claims matched the requested criteria."


# ============================================================
# 8. Build generation prompt
# ============================================================

prompt = f"""
You are the ClaimsIQ insurance claims assistant.

Answer the user's question using ONLY the verified claims below.

Do not invent facts.
Do not add claims that are not listed.
Do not remove matching claims.

User question:
{QUESTION}

Verified matching claims:
{verified_context}

Give a concise business answer.
Mention every matching Claim ID and briefly explain why it matches.
"""


# ============================================================
# 9. Load Qwen generation model
# ============================================================

print("\nLoading generation model...")

tokenizer = AutoTokenizer.from_pretrained(
    GENERATION_MODEL
)

model = AutoModelForCausalLM.from_pretrained(
    GENERATION_MODEL
)


# ============================================================
# 10. Create Qwen chat messages
# ============================================================

messages = [
    {
        "role": "system",
        "content": (
            "You are a precise ClaimsIQ insurance assistant. "
            "Only use verified information provided to you."
        )
    },
    {
        "role": "user",
        "content": prompt
    }
]


# ============================================================
# 11. Tokenize using Qwen chat template
# ============================================================

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt"
)


# ============================================================
# 12. Generate answer
# ============================================================

print("Generating answer...")

outputs = model.generate(
    **inputs,
    max_new_tokens=200,
    do_sample=False
)


# ============================================================
# 13. Decode only newly generated tokens
# ============================================================

generated_tokens = outputs[
    0
][
    inputs["input_ids"].shape[-1]:
]

answer = tokenizer.decode(
    generated_tokens,
    skip_special_tokens=True
)


# ============================================================
# 14. Final answer
# ============================================================

print("\n" + "=" * 70)
print("CLAIMSIQ RAG ANSWER")
print("=" * 70)

print(answer)


# ============================================================
# 15. Retrieved source records
# ============================================================

print("\n" + "=" * 70)
print("VERIFIED SOURCES")
print("=" * 70)

for claim in matching_claims:

    print(
        f'{claim["claim_id"]} | '
        f'{claim["claim_type"]} | '
        f'{claim["region"]} | '
        f'Risk={claim["risk_level"]} | '
        f'Priority={claim["processing_priority"]}'
    )