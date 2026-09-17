from fastapi.testclient import TestClient
import pytest

from api.app import app
from src.decisioning import audit


client = TestClient(app)


@pytest.fixture(autouse=True)
def isolated_audit_file(tmp_path, monkeypatch):
    audit_dir = tmp_path / "audit"
    audit_file = audit_dir / "decisions.jsonl"

    monkeypatch.setattr(audit, "AUDIT_DIR", audit_dir)
    monkeypatch.setattr(audit, "AUDIT_FILE", audit_file)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "claimsiq-api"
    assert data["version"] == "3.0.0"


def test_audit_endpoint_returns_audit_history():
    decision_response = client.post("/decision", json={"claim_id": "CLM-2026-0005"})
    assert decision_response.status_code == 200

    response = client.get("/audit")

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "records" in data
    assert data["count"] == len(data["records"])
    assert data["count"] >= 1

    record = data["records"][0]

    assert "timestamp" in record
    assert "claim_id" in record
    assert "decision" in record
    assert "decision_version" in record
    assert "reason_codes" in record
    assert "reasons" in record
    assert "decision_source" in record


def test_audit_endpoint_contains_known_decision():
    decision_response = client.post("/decision", json={"claim_id": "CLM-2026-0005"})
    assert decision_response.status_code == 200

    response = client.get("/audit")

    assert response.status_code == 200

    data = response.json()

    claim_ids = [
        record["claim_id"]
        for record in data["records"]
    ]

    assert "CLM-2026-0005" in claim_ids


def test_audit_endpoint_filters_by_claim_id():
    decision_response = client.post(
        "/decision",
        json={"claim_id": "CLM-2026-0005"},
    )
    assert decision_response.status_code == 200

    response = client.get(
        "/audit",
        params={"claim_id": "CLM-2026-0005"},
        headers={"X-Correlation-ID": "claimsiq-audit-test-001"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == len(data["records"])
    assert data["count"] >= 1

    assert all(
        record["claim_id"] == "CLM-2026-0005"
        for record in data["records"]
    )

    assert response.headers["X-Correlation-ID"] == (
        "claimsiq-audit-test-001"
    )


def test_correlation_id_is_preserved():
    correlation_id = "claimsiq-test-001"

    response = client.get(
        "/health",
        headers={"X-Correlation-ID": correlation_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == correlation_id


def test_correlation_id_is_generated_when_missing():
    response = client.get("/health")

    assert response.status_code == 200

    correlation_id = response.headers.get("X-Correlation-ID")

    assert correlation_id
    assert len(correlation_id) == 36


def test_ask_endpoint_returns_controlled_error_when_rag_fails(monkeypatch):
    def failing_ask_claims(question):
        raise RuntimeError("OpenSearch unavailable")

    monkeypatch.setattr(
        "api.app.ask_claims",
        failing_ask_claims,
    )

    response = client.post(
        "/ask",
        json={"question": "Find high priority health claims under review"},
        headers={"X-Correlation-ID": "claimsiq-rag-failure-001"},
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "ClaimsIQ RAG processing failed."
    }
    assert response.headers["X-Correlation-ID"] == (
        "claimsiq-rag-failure-001"
    )


def test_decision_endpoint_returns_404_for_unknown_claim():
    correlation_id = "claimsiq-api-negative-001"

    response = client.post(
        "/decision",
        json={"claim_id": "CLM-DOES-NOT-EXIST"},
        headers={"X-Correlation-ID": correlation_id},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Claim not found: CLM-DOES-NOT-EXIST"
    }
    assert response.headers["X-Correlation-ID"] == correlation_id


def test_ask_endpoint_rejects_empty_question():
    response = client.post(
        "/ask",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_ask_endpoint_rejects_question_over_2000_characters():
    response = client.post(
        "/ask",
        json={"question": "x" * 2001},
    )

    assert response.status_code == 422


def test_decision_endpoint_rejects_empty_claim_id():
    response = client.post(
        "/decision",
        json={"claim_id": ""},
    )

    assert response.status_code == 422


def test_decision_endpoint_rejects_claim_id_over_100_characters():
    response = client.post(
        "/decision",
        json={"claim_id": "x" * 101},
    )

    assert response.status_code == 422
