import json

from src.decisioning import audit


def test_record_decision_audit_creates_valid_jsonl(tmp_path, monkeypatch):
    audit_dir = tmp_path / "audit"
    audit_file = audit_dir / "decisions.jsonl"

    monkeypatch.setattr(audit, "AUDIT_DIR", audit_dir)
    monkeypatch.setattr(audit, "AUDIT_FILE", audit_file)

    decision_result = {
        "claim_id": "CLM-2026-0005",
        "decision": "ESCALATE",
        "decision_version": "1.0",
        "reason_codes": [
            "HIGH_RISK",
            "HIGH_PROCESSING_PRIORITY",
        ],
        "reasons": [
            "HIGH risk claim",
            "HIGH processing priority",
        ],
    }

    result = audit.record_decision_audit(
        decision_result=decision_result,
        claim_id="CLM-2026-0005",
    )

    assert result["claim_id"] == "CLM-2026-0005"
    assert result["decision"] == "ESCALATE"
    assert result["decision_version"] == "1.0"
    assert result["reason_codes"] == [
        "HIGH_RISK",
        "HIGH_PROCESSING_PRIORITY",
    ]
    assert result["reasons"] == [
        "HIGH risk claim",
        "HIGH processing priority",
    ]
    assert result["decision_source"] == (
        "deterministic_decision_engine"
    )
    assert result["timestamp"]

    assert audit_file.exists()

    lines = audit_file.read_text(
        encoding="utf-8"
    ).splitlines()

    assert len(lines) == 1

    stored_record = json.loads(lines[0])

    assert stored_record == result


def test_record_decision_audit_appends_multiple_events(
    tmp_path,
    monkeypatch,
):
    audit_dir = tmp_path / "audit"
    audit_file = audit_dir / "decisions.jsonl"

    monkeypatch.setattr(audit, "AUDIT_DIR", audit_dir)
    monkeypatch.setattr(audit, "AUDIT_FILE", audit_file)

    first_result = audit.record_decision_audit(
        decision_result={
            "decision": "APPROVED",
            "decision_version": "1.0",
            "reason_codes": [],
            "reasons": [],
        },
        claim_id="CLM-2026-0004",
    )

    second_result = audit.record_decision_audit(
        decision_result={
            "decision": "ESCALATE",
            "decision_version": "1.0",
            "reason_codes": ["HIGH_RISK"],
            "reasons": ["HIGH risk claim"],
        },
        claim_id="CLM-2026-0005",
    )

    lines = audit_file.read_text(
        encoding="utf-8"
    ).splitlines()

    assert len(lines) == 2

    stored_first = json.loads(lines[0])
    stored_second = json.loads(lines[1])

    assert stored_first == first_result
    assert stored_second == second_result

    assert stored_first["claim_id"] == "CLM-2026-0004"
    assert stored_first["decision"] == "APPROVED"

    assert stored_second["claim_id"] == "CLM-2026-0005"
    assert stored_second["decision"] == "ESCALATE"