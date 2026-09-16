import boto3
import pandas as pd
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

from config.settings import (
    AWS_REGION,
    AOSS_HOST,
    AOSS_INDEX_NAME,
    EMBEDDING_MODEL,
)

df = pd.read_parquet("claimsiq-gold.parquet")

model = SentenceTransformer(EMBEDDING_MODEL)

credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, AWS_REGION, "aoss")

client = OpenSearch(
    hosts=[{"host": AOSS_HOST, "port": 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

for _, row in df.iterrows():

    claim_text = (
        f"Claim {row['claim_id']} for policy {row['policy_id']} "
        f"is a {row['claim_type']} claim in {row['region']}. "
        f"Claim amount is {row['claim_amount']} {row['currency']}. "
        f"Status is {row['status']}. "
        f"Channel is {row['channel']}. "
        f"Risk level is {row['risk_level']}. "
        f"Processing priority is {row['processing_priority']}."
    )

    vector = model.encode(claim_text).tolist()

    document = {
        "claim_id": row["claim_id"],
        "claim_text": claim_text,
        "claim_type": row["claim_type"],
        "region": row["region"],
        "risk_level": row["risk_level"],
        "processing_priority": row["processing_priority"],
        "embedding": vector,
    }

    response = client.index(
        index=AOSS_INDEX_NAME,
        body=document,
    )

    print(
        "Indexed:",
        row["claim_id"],
        "| Result:",
        response["result"],
        "| Dimensions:",
        len(vector),
    )

print("Total claims processed:", len(df))
