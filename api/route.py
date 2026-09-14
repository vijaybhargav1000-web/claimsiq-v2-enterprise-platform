import json
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel, Field

from src.claimsiq_rag_answer import ask_claimsiq
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
    """
    Execute the ClaimsIQ RAG engine and return
    the deterministic verified business result.
    """
    return ask_claimsiq(question)


def decide_claim(claim_id: str) -> Dict[str, Any]:
    """
    Load one claim from the Gold-layer decision dataset
    and evaluate it using the deterministic decision engine.
    """

    if not GOLD_FILE.exists():
        raise FileNotFoundError(
            f"Gold claims dataset not found: {GOLD_FILE}"
        )

    with GOLD_FILE.open("r", encoding="utf-8") as file:
        claims = json.load(file)

    for claim in claims:
        if str(claim.get("claim_id")) == claim_id:
            return evaluate_claim(claim)

    raise ValueError(f"Claim not found: {claim_id}")
