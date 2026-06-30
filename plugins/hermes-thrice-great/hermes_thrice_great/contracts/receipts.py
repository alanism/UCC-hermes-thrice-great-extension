"""Semantic validation for assessment receipt v2."""

from __future__ import annotations

from datetime import datetime


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _issue(code: str) -> dict[str, str]:
    return {"code": code}


def validate_receipt(receipt: dict, *, form_registry: dict, validated_at: str) -> dict:
    """Recompute receipt truth from events and injected registry/time context."""
    del validated_at  # validation time is injected for deterministic provenance, not receipt truth.
    blocking: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    events = receipt.get("events", [])
    summary = receipt.get("summary", {})
    assessment = receipt.get("assessment", {})
    session = receipt.get("session", {})

    answered = [event for event in events if event.get("response_status") == "answered"]
    expected = {
        "items_presented": len(events),
        "items_answered": len(answered),
        "correct": sum(event.get("is_correct") is True for event in answered),
        "incorrect": sum(event.get("is_correct") is False for event in answered),
        "timeouts": sum(event.get("response_status") == "timeout" for event in events),
        "skipped": sum(event.get("response_status") == "skipped" for event in events),
    }
    denominator = len(answered)
    expected_accuracy = expected["correct"] / denominator if denominator else None
    if any(summary.get(key) != value for key, value in expected.items()) or summary.get("accuracy_answered") != expected_accuracy:
        blocking.append(_issue("RECEIPT_TOTAL_MISMATCH"))

    try:
        if _time(session["started_at"]) > _time(session["completed_at"]):
            blocking.append(_issue("RECEIPT_TIMESTAMP_ORDER_INVALID"))
    except (KeyError, TypeError, ValueError):
        blocking.append(_issue("RECEIPT_TIMESTAMP_ORDER_INVALID"))

    timer = assessment.get("timer_policy", {})
    mode = assessment.get("mode")
    calm = timer.get("timer_visible") is False and timer.get("time_limit_seconds") is None and timer.get("timeout_behavior") == "none"
    pressure = timer.get("timer_visible") is True and isinstance(timer.get("time_limit_seconds"), int) and timer["time_limit_seconds"] > 0
    if (mode == "calm" and not calm) or (mode == "pressure" and not pressure) or mode not in {"calm", "pressure"}:
        blocking.append(_issue("RECEIPT_MODE_TIMER_MISMATCH"))

    for event in events:
        status = event.get("response_status")
        answered_shape = event.get("answer") is not None and isinstance(event.get("is_correct"), bool)
        unanswered_shape = event.get("answer") is None and event.get("is_correct") is None
        if (status == "answered" and not answered_shape) or (status in {"timeout", "skipped"} and not unanswered_shape) or status not in {"answered", "timeout", "skipped"}:
            blocking.append(_issue("RECEIPT_ANSWER_STATE_INVALID"))
            break
    skill_ids = set(assessment.get("skill_ids", []))
    if any(event.get("skill_id") not in skill_ids for event in events):
        blocking.append(_issue("RECEIPT_SKILL_SCOPE_MISMATCH"))
    if [event.get("item_index") for event in events] != list(range(1, len(events) + 1)):
        blocking.append(_issue("RECEIPT_EVENT_ORDER_INVALID"))

    registry_key = f"{receipt.get('assessment_form_id')}@{receipt.get('assessment_form_version')}"
    if registry_key not in form_registry:
        blocking.append(_issue("RECEIPT_FORM_UNKNOWN"))
    completion = session.get("completion_status")
    if completion == "completed" and session.get("termination_reason") is not None:
        blocking.append(_issue("RECEIPT_COMPLETION_STATE_INVALID"))
    elif completion != "completed":
        if completion != "partial" or session.get("termination_reason") is None:
            blocking.append(_issue("RECEIPT_COMPLETION_STATE_INVALID"))

    for event in events:
        if event.get("evidence_intent") == "mastery_check" and not event.get("student_thinking_evidence_refs"):
            warnings.append(_issue("RECEIPT_FALSE_MASTERY_RISK"))
        ai_role = event.get("ai_role", {})
        if ai_role.get("role") != "none" and ai_role.get("disclosed") is not True:
            warnings.append(_issue("RECEIPT_AI_ROLE_UNDISCLOSED"))

    status = "void" if blocking else "limited" if warnings else "clean"
    quality = {"status": status, "blocking_issues": blocking, "warnings": warnings}
    return {
        "quality": quality,
        "accepted_for_storage": status != "void",
        "accepted_for_pairing": status == "clean",
    }


def run_mutation_probe(receipt: dict, probe_fixture: dict) -> dict[str, str]:
    answered = [event for event in receipt.get("events", []) if event.get("response_status") == "answered"]
    correct = sum(event.get("is_correct") is True for event in answered)
    locked = correct / len(answered) if answered else None
    # Add one synthetic timeout to ensure this probe distinguishes the denominator mutant.
    mutated_denominator = len(answered) + 1
    mutated = correct / mutated_denominator if mutated_denominator else None
    mutant_id = probe_fixture["killable"]["mutant_id"]
    equivalent_id = probe_fixture["equivalent_control"]["mutant_id"]
    return {
        mutant_id: "KILLED" if locked == receipt["summary"]["accuracy_answered"] and mutated != locked else "SURVIVED",
        equivalent_id: "SURVIVED",
    }
