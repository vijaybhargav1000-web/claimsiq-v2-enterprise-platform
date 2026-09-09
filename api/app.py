from fastapi import FastAPI, HTTPException

from api.route import AskRequest, ask_claims


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