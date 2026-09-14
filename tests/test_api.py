from fastapi.testclient import TestClient

from api.app import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "claimsiq-api"
    assert data["version"] == "3.0.0"


def test_audit_endpoint_returns_audit_history():
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
    response = client.get("/audit")

    assert response.status_code == 200

    data = response.json()

    claim_ids = [
        record["claim_id"]
        for record in data["records"]
    ]

    assert "CLM-2026-0005" in claim_ids

def test_correlation_id_is_preserved():
    correlation_id = "claimsiq-test-001"

    response = client.get(
        "/health",
        headers={
            "X-Correlation-ID": correlation_id,
        },
    )

    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == correlation_id


def test_correlation_id_is_generated_when_missing():
    response = client.get("/health")

    assert response.status_code == 200

    correlation_id = response.headers.get(
        "X-Correlation-ID"
    )

    assert correlation_id
    assert len(correlation_id) == 36