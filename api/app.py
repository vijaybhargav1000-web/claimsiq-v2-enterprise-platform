import logging
import uuid

from fastapi import FastAPI, HTTPException, Request

from api.route import (
    AskRequest,
    DecisionRequest,
    ask_claims,
    decide_claim,
)
from src.decisioning.audit import get_decision_audit


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s %(levelname)s "
        "service=claimsiq-api %(message)s"
    ),
)

logger = logging.getLogger("claimsiq-api")


app = FastAPI(
    title="ClaimsIQ API",
    description="ClaimsIQ RAG and deterministic claims decisioning API",
    version="3.0.0",
)


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID")

    if not correlation_id:
        correlation_id = str(uuid.uuid4())

    logger.info(
        "request_started method=%s path=%s correlation_id=%s",
        request.method,
        request.url.path,
        correlation_id,
    )

    try:
        response = await call_next(request)

        response.headers["X-Correlation-ID"] = correlation_id

        logger.info(
            "request_completed method=%s path=%s status_code=%s correlation_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            correlation_id,
        )

        return response

    except Exception:
        logger.exception(
            "request_failed method=%s path=%s correlation_id=%s",
            request.method,
            request.url.path,
            correlation_id,
        )
        raise


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
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="ClaimsIQ RAG processing failed.",
        ) from exc


@app.post("/decision")
def decision(
    request: DecisionRequest,
    http_request: Request,
):
    try:
        correlation_id = http_request.headers.get("X-Correlation-ID")

        return decide_claim(
            request.claim_id,
            correlation_id=correlation_id,
        )

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