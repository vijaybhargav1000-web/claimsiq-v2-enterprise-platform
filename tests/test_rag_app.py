from fastapi.testclient import TestClient

from rag.app import app


client = TestClient(app)


def test_bedrock_rag_returns_controlled_error(monkeypatch):
    def failing_retrieve_and_generate(**kwargs):
        raise RuntimeError("Bedrock unavailable")

    monkeypatch.setattr(
        "rag.app.client.retrieve_and_generate",
        failing_retrieve_and_generate,
    )

    response = client.post(
        "/ask",
        json={"question": "Find high risk health claims"},
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "ClaimsIQ Bedrock RAG processing failed."
    }


def test_bedrock_rag_success(monkeypatch):
    def successful_retrieve_and_generate(**kwargs):
        return {
            "output": {
                "text": "Response: Claim requires manual review."
            }
        }

    monkeypatch.setattr(
        "rag.app.client.retrieve_and_generate",
        successful_retrieve_and_generate,
    )

    response = client.post(
        "/ask",
        json={"question": "Analyze claim CLM10001"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Claim requires manual review."
    }

def test_bedrock_rag_rejects_empty_question():
    response = client.post(
        "/ask",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_bedrock_rag_rejects_question_over_2000_characters():
    response = client.post(
        "/ask",
        json={"question": "x" * 2001},
    )

    assert response.status_code == 422

def test_bedrock_rag_returns_controlled_error_for_malformed_response(monkeypatch):
    def malformed_retrieve_and_generate(**kwargs):
        return {}

    monkeypatch.setattr(
        "rag.app.client.retrieve_and_generate",
        malformed_retrieve_and_generate,
    )

    response = client.post(
        "/ask",
        json={"question": "Analyze claim CLM10001"},
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "ClaimsIQ Bedrock RAG processing failed."
    }
