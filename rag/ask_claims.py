import boto3

REGION = "ap-south-1"

KNOWLEDGE_BASE_ID = "Z6R9AL3KQH"

MODEL_ARN = (
    "arn:aws:bedrock:ap-south-1:948749907699:"
    "inference-profile/apac.amazon.nova-lite-v1:0"
)

client = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)

question = input("Ask ClaimsIQ: ")

response = client.retrieve_and_generate(
    input={
        "text": question
    },
    retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": KNOWLEDGE_BASE_ID,
            "modelArn": MODEL_ARN
        }
    }
)

print("\nAI Answer\n")
print(response["output"]["text"])