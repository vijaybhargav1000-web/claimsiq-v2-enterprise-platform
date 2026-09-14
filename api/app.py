from fastapi import FastAPI, HTTPException

from api.route import (
    AskRequest,
    DecisionRequest,
    ask_claims,
    decide_claim,
)
from src.decisioning.audit import get_decision_audit


app = FastAPI(
    title="ClaimsIQ API",
    description="ClaimsIQ RAG and deterministic claims decisioning API",
    version="3.0.0",
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "claimsiq-api",
        "version": "3.0.0",
    }


@app.post("/ask")
def ask(request: AskRequest):
    try:
        return ask_claims(request.question)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="ClaimsIQ processing failed.",
        ) from exc


@app.post("/decision")
def decision(request: DecisionRequest):
    try:
        return decide_claim(request.claim_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="ClaimsIQ decision processing failed.",
        ) from exc


@app.get("/audit")
def audit_history():
    try:
        records = get_decision_audit()

        return {
            "count": len(records),
            "records": records,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="ClaimsIQ audit history retrieval failed.",
        ) from exc