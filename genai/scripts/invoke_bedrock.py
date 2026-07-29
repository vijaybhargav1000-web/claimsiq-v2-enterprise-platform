import json
import boto3
from botocore.exceptions import ClientError

# -----------------------------
# Configuration
# -----------------------------
REGION = "ap-south-1"
MODEL_ID = "apac.amazon.nova-lite-v1:0"

# -----------------------------
# Bedrock Client
# -----------------------------
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=REGION
)

# -----------------------------
# Read Claim JSON
# -----------------------------
with open("../data/claim.json", "r", encoding="utf-8") as file:
    claim = json.load(file)

# -----------------------------
# Build Prompt
# -----------------------------
prompt = f"""
You are an experienced Insurance Claims Analyst.

Analyse the insurance claim below.

Claim Details

Claim ID: {claim['claim_id']}
Customer Name: {claim['customer_name']}
Policy Number: {claim['policy_number']}
Policy Type: {claim['policy_type']}
Incident Date: {claim['incident_date']}
Location: {claim['incident_location']}
Incident: {claim['incident']}
Estimated Damage: ${claim['estimated_damage']}
Driver Injury: {claim['driver_injury']}
Police Report: {claim['police_report']}
Vehicle: {claim['vehicle_model']}
Claim Status: {claim['claim_status']}

Return ONLY valid JSON.

Do not include markdown.
Do not include explanation.
Do not include ```json.

Return exactly this structure:

{{
    "claim_id": "",
    "claim_summary": "",
    "risk_level": "",
    "fraud_score": 0,
    "recommended_action": "",
    "missing_information": [],
    "reasoning": ""
}}
"""

# -----------------------------
# Invoke Bedrock
# -----------------------------
try:

    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    )

    output = response["output"]["message"]["content"][0]["text"]

    print("\n========== RAW AI RESPONSE ==========\n")
    print(output)

    # Try to parse JSON
    try:
        analysis = json.loads(output)

    except json.JSONDecodeError:

        print("\nBedrock did not return valid JSON.")
        print("Saving raw response instead.\n")

        analysis = {
            "raw_response": output
        }

    # Save response
    with open("../responses/analysis.json", "w", encoding="utf-8") as file:
        json.dump(
            analysis,
            file,
            indent=4
        )

    print("\nAnalysis saved successfully.")

except ClientError as error:
    print(error)