import json
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel, Field

from src.claimsiq_rag_answer import ask_claimsiq
from src.decisioning.audit import record_decision_audit
from src.decisioning.engine import evaluate_claim


GOLD_FILE = Path(__file__).resolve().parent.parent / "data" / "claims_gold.json"


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Natural-language ClaimsIQ question",
    )


class DecisionRequest(BaseModel):
    claim_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="ClaimsIQ claim identifier",
    )


def ask_claims(question: str):
    return ask_claimsiq(question)


def decide_claim(
    claim_id: str,
    correlation_id: str | None = None,
) -> Dict[str, Any]:
    if not GOLD_FILE.exists():
        raise FileNotFoundError(
            f"Gold claims dataset not found: {GOLD_FILE}"
        )

    with GOLD_FILE.open("r", encoding="utf-8") as file:
        claims = json.load(file)

    for claim in claims:
        if str(claim.get("claim_id")) == claim_id:
            decision_result = evaluate_claim(claim)

            record_decision_audit(
                decision_result=decision_result,
                claim_id=claim_id,
                correlation_id=correlation_id,
            )

            return decision_result

    raise ValueError(f"Claim not found: {claim_id}")