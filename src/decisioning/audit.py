import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


AUDIT_DIR = Path(__file__).resolve().parents[2] / "audit"
AUDIT_FILE = AUDIT_DIR / "decisions.jsonl"


def record_decision_audit(
    decision_result: Dict[str, Any],
    claim_id: str,
) -> Dict[str, Any]:
    """
    Persist a ClaimsIQ decision as an audit event.

    Each decision is stored as one JSON object per line so that
    individual decision events remain easy to inspect and process.
    """

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    audit_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "claim_id": claim_id,
        "decision": decision_result.get("decision"),
        "decision_version": decision_result.get("decision_version"),
        "reason_codes": decision_result.get("reason_codes", []),
        "reasons": decision_result.get("reasons", []),
        "decision_source": "deterministic_decision_engine",
    }

    with AUDIT_FILE.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            json.dumps(
                audit_record,
                ensure_ascii=False,
            )
            + "\n"
        )

    return audit_record


def get_decision_audit() -> List[Dict[str, Any]]:
    """
    Read all persisted ClaimsIQ decision audit events.

    Returns an empty list when no audit file exists.
    """

    if not AUDIT_FILE.exists():
        return []

    records = []

    with AUDIT_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            records.append(
                json.loads(line)
            )

    return records