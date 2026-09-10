import os


AWS_REGION = os.getenv(
    "CLAIMSIQ_AWS_REGION",
    "ap-south-1",
)

AOSS_HOST = os.getenv(
    "CLAIMSIQ_AOSS_HOST",
    "316zxmoi289705x59odi.ap-south-1.aoss.amazonaws.com",
)

AOSS_INDEX_NAME = os.getenv(
    "CLAIMSIQ_AOSS_INDEX",
    "claimsiq-rag-index",
)

EMBEDDING_MODEL = os.getenv(
    "CLAIMSIQ_EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

API_HOST = os.getenv(
    "CLAIMSIQ_API_HOST",
    "127.0.0.1",
)

API_PORT = int(
    os.getenv(
        "CLAIMSIQ_API_PORT",
        "8000",
    )
)