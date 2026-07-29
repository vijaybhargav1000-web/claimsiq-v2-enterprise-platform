import json
import boto3
from botocore.exceptions import ClientError

REGION = "ap-south-1"
MODEL_ID = "apac.amazon.nova-lite-v1:0"

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=REGION
)

with open("../data/claim.json", "r", encoding="utf-8") as f:
    claim = json.load(f)

prompt = f"""
You are an experienced Insurance Claims Analyst.

Analyse the following insurance claim.

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

Provide:

1. Claim Summary

2. Risk Level

3. Fraud Indicators

4. Missing Information

5. Recommended Next Action
"""

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

    print(output)

    with open("../responses/analysis.json", "w", encoding="utf-8") as f:

        json.dump(
            {
                "claim_id": claim["claim_id"],
                "analysis": output
            },
            f,
            indent=4
        )

    print("\nAnalysis saved successfully.")

except ClientError as e:
    print(e)