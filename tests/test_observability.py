import logging

from fastapi.testclient import TestClient

from api.app import app


client = TestClient(app)


def test_unexpected_exception_logs_correlation_id(monkeypatch, caplog):
    correlation_id = "claimsiq-observability-failure-001"

    def failing_ask_claims(question):
        raise RuntimeError("simulated unexpected failure")

    monkeypatch.setattr(
        "api.app.ask_claims",
        failing_ask_claims,
    )

    with caplog.at_level(logging.INFO, logger="claimsiq-api"):
        response = client.post(
            "/ask",
            json={"question": "Find high priority health claims"},
            headers={"X-Correlation-ID": correlation_id},
        )

    assert response.status_code == 500
    assert response.headers["X-Correlation-ID"] == correlation_id

    assert any(
        "request_completed" in record.message
        and correlation_id in record.message
        and "status_code=500" in record.message
        for record in caplog.records
    )
