from src.claimsiq_rag_answer import (
    parse_business_filters,
    matches_business_filters,
)


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