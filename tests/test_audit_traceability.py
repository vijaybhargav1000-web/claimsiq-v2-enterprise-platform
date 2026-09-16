import uuid

from fastapi.testclient import TestClient

from api.app import app
from src.decisioning.audit import get_decision_audit


client = TestClient(app)


def test_decision_persists_correlation_id_in_audit():
    correlation_id = f"claimsiq-trace-test-{uuid.uuid4()}"
    claim_id = "CLM-2026-0005"

    response = client.post(
        "/decision",
        json={"claim_id": claim_id},
        headers={"X-Correlation-ID": correlation_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == correlation_id

    records = get_decision_audit()

    matching_records = [
        record
        for record in records
        if record.get("correlation_id") == correlation_id
        and record.get("claim_id") == claim_id
    ]

    assert len(matching_records) == 1

    audit_record = matching_records[0]

    assert audit_record["decision"] == response.json()["decision"]
    assert audit_record["decision_version"] == response.json()["decision_version"]
    assert audit_record["decision_source"] == "deterministic_decision_engine"
