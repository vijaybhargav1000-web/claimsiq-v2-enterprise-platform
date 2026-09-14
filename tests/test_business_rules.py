from src.claimsiq_rag_answer import (
    parse_business_filters,
    matches_business_filters,
)
from src.decisioning.engine import evaluate_claim


def test_high_risk_health_under_review():
    claims = [
        {
            "claim_id": "CLM-2026-0005",
            "claim_type": "HEALTH",
            "risk_level": "HIGH",
            "processing_priority": "HIGH",
            "status": "UNDER_REVIEW",
            "region": "IN-EAST",
        },
        {
            "claim_id": "CLM-2026-0002",
            "claim_type": "HEALTH",
            "risk_level": "MEDIUM",
            "processing_priority": "HIGH",
            "status": "UNDER_REVIEW",
            "region": "IN-WEST",
        },
    ]

    filters = parse_business_filters(
        "Find high risk health claims under review"
    )

    matches = [
        claim
        for claim in claims
        if matches_business_filters(claim, filters)
    ]

    assert len(matches) == 1
    assert matches[0]["claim_id"] == "CLM-2026-0005"


def test_high_priority_health_under_review():
    claims = [
        {
            "claim_id": "CLM-2026-0002",
            "claim_type": "HEALTH",
            "risk_level": "MEDIUM",
            "processing_priority": "HIGH",
            "status": "UNDER_REVIEW",
            "region": "IN-WEST",
        },
        {
            "claim_id": "CLM-2026-0005",
            "claim_type": "HEALTH",
            "risk_level": "HIGH",
            "processing_priority": "HIGH",
            "status": "UNDER_REVIEW",
            "region": "IN-EAST",
        },
    ]

    filters = parse_business_filters(
        "Find high priority health claims under review"
    )

    matches = [
        claim
        for claim in claims
        if matches_business_filters(claim, filters)
    ]

    assert len(matches) == 2
    assert {claim["claim_id"] for claim in matches} == {
        "CLM-2026-0002",
        "CLM-2026-0005",
    }


def test_high_risk_health_under_review_does_not_match_medium_risk():
    claim = {
        "claim_id": "CLM-2026-0002",
        "claim_type": "HEALTH",
        "risk_level": "MEDIUM",
        "processing_priority": "HIGH",
        "status": "UNDER_REVIEW",
        "region": "IN-WEST",
    }

    filters = parse_business_filters(
        "Find high risk health claims under review"
    )

    assert matches_business_filters(claim, filters) is False


def test_high_risk_health_normal_priority_does_not_match():
    claim = {
        "claim_id": "CLM-2026-0005",
        "claim_type": "HEALTH",
        "risk_level": "HIGH",
        "processing_priority": "HIGH",
        "status": "UNDER_REVIEW",
        "region": "IN-EAST",
    }

    filters = parse_business_filters(
        "Find high risk health claims with normal priority"
    )

    assert filters["claim_type"] == "HEALTH"
    assert filters["risk_level"] == "HIGH"
    assert filters["processing_priority"] == "NORMAL"

    assert matches_business_filters(claim, filters) is False


# ---------------------------------------------------------------------------
# Decision Engine Tests
# ---------------------------------------------------------------------------


def test_decision_high_risk_high_priority_escalates():
    claim = {
        "claim_id": "CLM-2026-0005",
        "risk_level": "HIGH",
        "processing_priority": "HIGH",
        "status": "UNDER_REVIEW",
        "claim_amount_band": "HIGH_VALUE",
    }

    result = evaluate_claim(claim)

    assert result["claim_id"] == "CLM-2026-0005"
    assert result["decision"] == "ESCALATE"
    assert result["decision_version"] == "1.0"

    assert "HIGH_RISK" in result["reason_codes"]
    assert "HIGH_PROCESSING_PRIORITY" in result["reason_codes"]
    assert "HIGH_VALUE_CLAIM" in result["reason_codes"]
    assert "UNDER_REVIEW" in result["reason_codes"]
    assert "HIGH_RISK_HIGH_PRIORITY" in result["reason_codes"]


def test_decision_under_review_becomes_manual_review():
    claim = {
        "claim_id": "CLM-2026-0002",
        "risk_level": "MEDIUM",
        "processing_priority": "HIGH",
        "status": "UNDER_REVIEW",
        "claim_amount_band": "LOW_VALUE",
    }

    result = evaluate_claim(claim)

    assert result["decision"] == "MANUAL_REVIEW"
    assert result["decision_version"] == "1.0"
    assert "UNDER_REVIEW" in result["reason_codes"]


def test_decision_rejected_claim():
    claim = {
        "claim_id": "CLM-2026-0006",
        "risk_level": "LOW",
        "processing_priority": "NORMAL",
        "status": "REJECTED",
        "claim_amount_band": "LOW_VALUE",
    }

    result = evaluate_claim(claim)

    assert result["decision"] == "REJECTED"
    assert result["decision_version"] == "1.0"


def test_decision_approved_claim():
    claim = {
        "claim_id": "CLM-2026-0004",
        "risk_level": "LOW",
        "processing_priority": "NORMAL",
        "status": "APPROVED",
        "claim_amount_band": "LOW_VALUE",
    }

    result = evaluate_claim(claim)

    assert result["decision"] == "APPROVED"
    assert result["decision_version"] == "1.0"


def test_decision_standard_review_for_other_claim():
    claim = {
        "claim_id": "CLM-2026-0001",
        "risk_level": "LOW",
        "processing_priority": "NORMAL",
        "status": "SUBMITTED",
        "claim_amount_band": "LOW_VALUE",
    }

    result = evaluate_claim(claim)

    assert result["decision"] == "STANDARD_REVIEW"
    assert result["decision_version"] == "1.0"


def test_decision_precedence_escalation_over_manual_review():
    claim = {
        "claim_id": "CLM-2026-0008",
        "risk_level": "HIGH",
        "processing_priority": "HIGH",
        "status": "UNDER_REVIEW",
        "claim_amount_band": "HIGH_VALUE",
    }

    result = evaluate_claim(claim)

    # ESCALATE must win over the lower-priority UNDER_REVIEW rule.
    assert result["decision"] == "ESCALATE"


def test_decision_reason_codes_are_structured():
    claim = {
        "claim_id": "CLM-2026-0005",
        "risk_level": "HIGH",
        "processing_priority": "HIGH",
        "status": "UNDER_REVIEW",
        "claim_amount_band": "HIGH_VALUE",
    }

    result = evaluate_claim(claim)

    assert isinstance(result["reason_codes"], list)
    assert isinstance(result["reasons"], list)
    assert len(result["reason_codes"]) == len(result["reasons"])


def test_decision_missing_optional_fields_does_not_crash():
    claim = {
        "claim_id": "CLM-2026-TEST-001",
    }

    result = evaluate_claim(claim)

    assert result["claim_id"] == "CLM-2026-TEST-001"
    assert result["decision"] == "STANDARD_REVIEW"
    assert result["decision_version"] == "1.0"
    assert result["reason_codes"] == []
    assert result["reasons"] == []