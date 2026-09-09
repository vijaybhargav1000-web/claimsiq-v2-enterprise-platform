from fastapi import FastAPI
from pydantic import BaseModel
import boto3

# ---------------------------------------
# Configuration
# ---------------------------------------
REGION = "ap-south-1"

KNOWLEDGE_BASE_ID = "Z6R9AL3KQH"

MODEL_ARN = (
    "arn:aws:bedrock:ap-south-1:948749907699:"
    "inference-profile/apac.amazon.nova-lite-v1:0"
)

# ---------------------------------------
# Bedrock Client
# ---------------------------------------
client = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)

# ---------------------------------------
# FastAPI App
# ---------------------------------------
app = FastAPI(
    title="ClaimsIQ Enterprise API",
    description="Enterprise RAG API using Amazon Bedrock Knowledge Base",
    version="1.0"
)

# ---------------------------------------
# Request Model
# ---------------------------------------
class QuestionRequest(BaseModel):
    question: str

# ---------------------------------------
# Response Model
# ---------------------------------------
class QuestionResponse(BaseModel):
    answer: str

# ---------------------------------------
# Root Endpoint
# ---------------------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to ClaimsIQ Enterprise API",
        "status": "Running"
    }

# ---------------------------------------
# Ask Endpoint
# ---------------------------------------
@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):

    try:

        response = client.retrieve_and_generate(

            input={
                "text": request.question
            },

            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": MODEL_ARN
                }
            }
        )

        answer = response["output"]["text"]

        if "Response:" in answer:
            answer = answer.split("Response:", 1)[1].strip()

        elif "Based on the retrieved results," in answer:
            answer = answer.split(
                "Based on the retrieved results,", 1
            )[1].strip()

        return QuestionResponse(
            answer=answer
        )

    except Exception as e:

        return QuestionResponse(
            answer=f"Error: {str(e)}"
        )