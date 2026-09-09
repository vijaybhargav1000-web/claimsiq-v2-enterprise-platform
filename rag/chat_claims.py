import boto3

# -----------------------------
# Configuration
# -----------------------------
REGION = "ap-south-1"

KNOWLEDGE_BASE_ID = "Z6R9AL3KQH"

MODEL_ARN = (
    "arn:aws:bedrock:ap-south-1:948749907699:"
    "inference-profile/apac.amazon.nova-lite-v1:0"
)

# -----------------------------
# Bedrock Client
# -----------------------------
client = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)

# Bedrock creates the session automatically
session_id = None

# -----------------------------
# Welcome Message
# -----------------------------
print("=" * 60)
print("🤖 Welcome to ClaimsIQ AI Assistant")
print("Type 'exit' to quit")
print("=" * 60)

# -----------------------------
# Chat Loop
# -----------------------------
while True:

    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        print("\n👋 Goodbye!")
        break

    # Build request
    request = {
        "input": {
            "text": question
        },
        "retrieveAndGenerateConfiguration": {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": MODEL_ARN
            }
        }
    }

    # Reuse session after Bedrock creates one
    if session_id:
        request["sessionId"] = session_id

    try:
        print("\n⏳ Sending request to Bedrock...")

        response = client.retrieve_and_generate(**request)

        print("✅ Response received.")

        # Save Bedrock-generated session
        if "sessionId" in response:
            session_id = response["sessionId"]

        # Get answer
        answer = response["output"]["text"]

        # Optional cleanup for nicer display
        if "Response:" in answer:
            answer = answer.split("Response:", 1)[1].strip()

        elif "Based on the retrieved results," in answer:
            answer = answer.split(
                "Based on the retrieved results,", 1
            )[1].strip()

        print("\nClaimsIQ:\n")
        print(answer)

    except Exception as e:
        print("\n❌ Error occurred:")
        print(e)