from typing import Any, Dict

DECISION_VERSION = "1.0"


def evaluate_claim(claim: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate a ClaimsIQ Gold-layer claim using deterministic business rules.

    Decision precedence:
        1. HIGH risk + HIGH processing priority -> ESCALATE
        2. UNDER_REVIEW -> MANUAL_REVIEW
        3. REJECTED -> REJECTED
        4. APPROVED -> APPROVED
        5. Otherwise -> STANDARD_REVIEW

    Motor Insurance policy rules are applied only when the claim explicitly
    identifies itself as Motor Insurance and provides compatible source fields.
    USD policy thresholds are not applied to claims denominated in other
    currencies.
    """

    claim_id = claim.get("claim_id")

    risk_level = str(claim.get("risk_level", "")).upper()
    priority = str(claim.get("processing_priority", "")).upper()
    status = str(claim.get("status", "")).upper()
    amount_band = str(claim.get("claim_amount_band", "")).upper()

    reason_codes = []
    reasons = []

    if risk_level == "HIGH":
        reason_codes.append("HIGH_RISK")
        reasons.append("HIGH risk claim")

    if priority == "HIGH":
        reason_codes.append("HIGH_PROCESSING_PRIORITY")
        reasons.append("HIGH processing priority")

    if amount_band == "HIGH_VALUE":
        reason_codes.append("HIGH_VALUE_CLAIM")
        reasons.append("HIGH_VALUE claim amount")

    if status == "UNDER_REVIEW":
        reason_codes.append("UNDER_REVIEW")
        reasons.append("Claim is UNDER_REVIEW")

    if risk_level == "HIGH" and priority == "HIGH":
        decision = "ESCALATE"
        reason_codes.append("HIGH_RISK_HIGH_PRIORITY")
        reasons.append(
            "HIGH risk combined with HIGH processing priority"
        )

    elif status == "UNDER_REVIEW":
        decision = "MANUAL_REVIEW"

    elif status == "REJECTED":
        decision = "REJECTED"

    elif status == "APPROVED":
        decision = "APPROVED"

    else:
        decision = "STANDARD_REVIEW"

    return {
        "claim_id": claim_id,
        "decision": decision,
        "decision_version": DECISION_VERSION,
        "reason_codes": reason_codes,
        "reasons": reasons,
    }
