from pydantic import BaseModel, Field

from src.claimsiq_rag_answer import ask_claimsiq


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Natural-language ClaimsIQ question",
    )


def ask_claims(question: str):
    """
    Execute the ClaimsIQ RAG engine and return
    the deterministic verified business result.
    """

    return ask_claimsiq(question)