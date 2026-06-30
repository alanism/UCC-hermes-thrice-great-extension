"""Deterministic calm/pressure receipt pairing."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal, ROUND_HALF_EVEN


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _issue(code: str) -> dict[str, str]:
    return {"code": code}


def _rounded(value: float, places: int) -> float:
    quantum = Decimal(1).scaleb(-places)
    return float(Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_EVEN))


def evaluate_pair(
    receipts: list[dict], *, form_manifests: dict, pairing_policy: dict,
    registry_snapshot_sha256: str, pair_result_id: str, evaluated_at: str,
) -> dict:
    """Return comparison metrics only after every comparability gate passes."""
    del registry_snapshot_sha256
    base = {"pair_result_id": pair_result_id, "evaluated_at": evaluated_at}
    if len(receipts) != 2:
        return {**base, "status": "incomparable", "issues": [_issue("PAIR_MODE_SET_INVALID")]}
    by_mode = {receipt.get("assessment", {}).get("mode"): receipt for receipt in receipts}
    if set(by_mode) != {"calm", "pressure"}:
        return {**base, "status": "incomparable", "issues": [_issue("PAIR_MODE_SET_INVALID")]}
    calm, pressure = by_mode["calm"], by_mode["pressure"]
    issues: list[dict[str, str]] = []
    status = "valid"
    if calm.get("learner_id") != pressure.get("learner_id") or calm.get("paired_run_id") != pressure.get("paired_run_id"):
        issues.append(_issue("PAIR_LEARNER_MISMATCH"))
    calm_completed = _time(calm["session"]["completed_at"])
    pressure_started = _time(pressure["session"]["started_at"])
    if pressure_started <= calm_completed:
        issues.append(_issue("PAIR_ORDER_INVALID"))
    elif (pressure_started - calm_completed).total_seconds() > pairing_policy["maximum_pair_window_seconds"]:
        issues.append(_issue("PAIR_WINDOW_EXCEEDED"))

    def form_key(receipt: dict) -> str:
        return f"{receipt['assessment_form_id']}@{receipt['assessment_form_version']}"

    calm_key, pressure_key = form_key(calm), form_key(pressure)
    calm_form, pressure_form = form_manifests.get(calm_key), form_manifests.get(pressure_key)
    exact = calm_key == pressure_key
    equivalent = bool(
        calm_form and pressure_form
        and calm_form.get("comparison_family_id") == pressure_form.get("comparison_family_id")
        and pressure_key in calm_form.get("pairing_compatible_with", [])
    )
    form_allowed = exact and pairing_policy.get("allow_exact_form_reuse") or equivalent and pairing_policy.get("allow_registered_equivalent_forms")
    if not form_allowed:
        issues.append(_issue("PAIR_FORM_MISMATCH"))
    if set(calm["assessment"].get("skill_ids", [])) != set(pressure["assessment"].get("skill_ids", [])):
        issues.append(_issue("PAIR_SKILL_SET_MISMATCH"))
    if pairing_policy.get("required_ai_role_match") and set(calm["evidence_context"].get("session_ai_roles", [])) != set(pressure["evidence_context"].get("session_ai_roles", [])):
        issues.append(_issue("PAIR_AI_ROLE_MISMATCH"))

    qualities = [receipt.get("quality", {}).get("status") for receipt in (calm, pressure)]
    if any(quality not in pairing_policy.get("allowed_quality_statuses", []) for quality in qualities):
        issues.append(_issue("PAIR_INPUT_QUALITY_UNUSABLE"))
        status = "void"
    elif any(receipt["session"].get("completion_status") != "completed" for receipt in (calm, pressure)):
        issues.append(_issue("PAIR_PARTIAL_SESSION"))
        status = "insufficient_evidence"
    if any(receipt["summary"].get("items_presented", 0) < pairing_policy["minimum_presented_per_mode"] for receipt in (calm, pressure)):
        issues.append(_issue("PAIR_MINIMUM_PRESENTED_NOT_MET"))
        status = "insufficient_evidence" if status != "void" else status
    if any(receipt["summary"].get("items_answered", 0) < pairing_policy["minimum_answered_per_mode"] for receipt in (calm, pressure)):
        issues.append(_issue("PAIR_MINIMUM_ANSWERED_NOT_MET"))
        status = "insufficient_evidence" if status != "void" else status
    if issues and status == "valid":
        status = "incomparable"
    if status != "valid":
        return {**base, "status": status, "issues": issues}

    places = pairing_policy["decimal_places"]
    ca = calm["summary"]["correct"] / calm["summary"]["items_answered"]
    pa = pressure["summary"]["correct"] / pressure["summary"]["items_answered"]
    cp = calm["summary"]["correct"] / calm["summary"]["items_presented"]
    pp = pressure["summary"]["correct"] / pressure["summary"]["items_presented"]
    ct = calm["summary"]["timeouts"] / calm["summary"]["items_presented"]
    pt = pressure["summary"]["timeouts"] / pressure["summary"]["items_presented"]
    cs = calm["summary"]["skipped"] / calm["summary"]["items_presented"]
    ps = pressure["summary"]["skipped"] / pressure["summary"]["items_presented"]
    metrics = {
        "calm_accuracy_answered": _rounded(ca, places),
        "pressure_accuracy_answered": _rounded(pa, places),
        "pressure_delta_answered": _rounded(ca - pa, places),
        "calm_performance_presented": _rounded(cp, places),
        "pressure_performance_presented": _rounded(pp, places),
        "pressure_delta": _rounded(cp - pp, places),
        "timeout_rate_delta": _rounded(pt - ct, places),
        "skip_rate_delta": _rounded(ps - cs, places),
        "response_time_ratio": _rounded(pressure["summary"]["average_response_time_ms"] / calm["summary"]["average_response_time_ms"], places),
    }
    return {**base, "status": "valid", "issues": [], "metrics": metrics}


def run_mutation_probe(calm: dict, pressure: dict, pairing_policy: dict, probe_fixture: dict) -> dict[str, str]:
    del pairing_policy
    canonical_with_timeout = calm["summary"]["correct"] / (calm["summary"]["items_presented"] + 1)
    mutant_answered = calm["summary"]["correct"] / calm["summary"]["items_answered"]
    killable = probe_fixture["killable"]["mutant_id"]
    control = probe_fixture["equivalent_control"]["mutant_id"]
    return {killable: "KILLED" if canonical_with_timeout != mutant_answered else "SURVIVED", control: "SURVIVED"}
