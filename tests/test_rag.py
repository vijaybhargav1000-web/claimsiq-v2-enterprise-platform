import pytest
from types import SimpleNamespace

from src.claimsiq_rag_answer import ask_claimsiq


@pytest.mark.integration
def test_rag_high_risk_health_under_review():
    result = ask_claimsiq(
        "Find high risk health claims under review"
    )

    assert result["filters"] == {
        "claim_type": "HEALTH",
        "risk_level": "HIGH",
        "processing_priority": None,
        "status": "UNDER_REVIEW",
        "region": None,
    }

    assert result["matching_count"] == 1
    assert {
        claim["claim_id"]
        for claim in result["claims"]
    } == {"CLM-2026-0005"}


@pytest.mark.integration
def test_rag_high_priority_health_under_review():
    result = ask_claimsiq(
        "Find high priority health claims under review"
    )

    assert result["filters"] == {
        "claim_type": "HEALTH",
        "risk_level": None,
        "processing_priority": "HIGH",
        "status": "UNDER_REVIEW",
        "region": None,
    }

    assert result["matching_count"] == 2
    assert {
        claim["claim_id"]
        for claim in result["claims"]
    } == {
        "CLM-2026-0002",
        "CLM-2026-0005",
    }


@pytest.mark.integration
def test_rag_high_risk_health_normal_priority_returns_no_matches():
    result = ask_claimsiq(
        "Find high risk health claims with normal priority"
    )

    assert result["filters"] == {
        "claim_type": "HEALTH",
        "risk_level": "HIGH",
        "processing_priority": "NORMAL",
        "status": None,
        "region": None,
    }

    assert result["matching_count"] == 0
    assert result["claims"] == []


@pytest.mark.integration
def test_rag_claims_from_in_east():
    result = ask_claimsiq(
        "Find claims from IN-EAST"
    )

    assert result["filters"] == {
        "claim_type": None,
        "risk_level": None,
        "processing_priority": None,
        "status": None,
        "region": "IN-EAST",
    }

    assert result["matching_count"] == 2
    assert {
        claim["claim_id"]
        for claim in result["claims"]
    } == {
        "CLM-2026-0005",
        "CLM-2026-0009",
    }


def test_rag_raises_when_opensearch_response_is_malformed(
    monkeypatch,
):
    class FakeEmbeddingModel:
        def encode(self, question):
            return SimpleNamespace(
                tolist=lambda: [0.0] * 384
            )

    class FakeOpenSearchClient:
        def search(self, **kwargs):
            return {}

    monkeypatch.setattr(
        "src.claimsiq_rag_answer.get_embedding_model",
        lambda: FakeEmbeddingModel(),
    )

    monkeypatch.setattr(
        "src.claimsiq_rag_answer.get_opensearch_client",
        lambda: FakeOpenSearchClient(),
    )

    with pytest.raises(KeyError):
        ask_claimsiq("Find claims from IN-EAST")
