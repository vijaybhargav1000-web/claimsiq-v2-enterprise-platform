import json
import boto3
from botocore.exceptions import ClientError

REGION = "ap-south-1"
MODEL_ID = "apac.amazon.nova-lite-v1:0"

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=REGION
)

with open("../prompts/claim_analysis.txt", "r", encoding="utf-8") as file:
    prompt = file.read()

request_body = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "text": prompt
                }
            ]
        }
    ]
}

try:
    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=request_body["messages"]
    )

    output = response["output"]["message"]["content"][0]["text"]

    print("\n========== AI RESPONSE ==========\n")
    print(output)

    with open("../responses/sample_response.json", "w", encoding="utf-8") as file:
        json.dump(
            {
                "model": MODEL_ID,
                "response": output
            },
            file,
            indent=4
        )

    print("\nResponse saved successfully.")

except ClientError as error:
    print(error)