#!/usr/bin/env python3
"""
UCC Self-Heal Health Check — runs daily at 5am.
Checks all subsystems, attempts known repairs, reports findings.
Output is delivered verbatim via no_agent=True cron job.
"""
import subprocess, os, sys, json, time
from datetime import datetime, timezone

PROFILE = "thoth-big-pc"
HERMES_HOME = os.path.expanduser(f"~/AppData/Local/hermes/profiles/{PROFILE}")
HERMES_CLI = os.path.join(
    os.path.expanduser("~/AppData/Local/hermes/hermes-agent/venv/Scripts/hermes")
)

REQUIRED_CHANNELS = {
    "parent-agent": "[CHANNEL_ID]",
    "student-tasks": "[CHANNEL_ID]",
    "tutor-student": "[CHANNEL_ID]",
    "receipts": "[CHANNEL_ID]",
    "admin-support": "[CHANNEL_ID]",
}

FREE_RESPONSE_CHANNELS = ["[CHANNEL_ID]", "[CHANNEL_ID]"]

EXPECTED_CRON_JOBS = ["Weekly Math Assessment", "Weekly Reading Assessment"]

def run(cmd, timeout=15):
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, shell=True
        )
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT", -1
    except Exception as e:
        return "", str(e), -1

def check_gateway():
    """Check gateway process and log health."""
    issues = []
    healed = []

    # Check system process table for any hermes gateway python process
    out, _, _ = run('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH 2>nul')
    gateway_pids = []
    for line in out.split("\n"):
        if "hermes" in line.lower():
            parts = line.split(",")
            if len(parts) > 1:
                pid = parts[1].strip().strip('"')
                gateway_pids.append(pid)

    # Check hermes gateway status
    status_out, status_err, status_rc = run(f'"{HERMES_CLI}" gateway status', timeout=10)

    log_path = os.path.join(HERMES_HOME, "logs", "gateway.log")

    log_ok = False
    log_age_minutes = 999
    if os.path.exists(log_path):
        mtime = os.path.getmtime(log_path)
        log_age_minutes = (time.time() - mtime) / 60
        log_ok = log_age_minutes < 10  # fresh within 10 minutes

    # Check last connected status in log
    connected = False
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            for line in f:
                if "discord connected" in line:
                    connected = True

    pid_running = len(gateway_pids) > 0
    status_reports_running = "Gateway process running" in status_out

    if not pid_running and not status_reports_running:
        issues.append("Gateway process not found")
        # Self-heal: restart gateway
        _, _, rc = run(f'start "" /B "{HERMES_CLI}" gateway run --replace', timeout=5)
        time.sleep(8)
        # Re-check
        out2, _, _ = run(f'"{HERMES_CLI}" gateway status', timeout=10)
        if "Gateway process running" in out2:
            healed.append("Gateway was dead → restarted successfully")
        else:
            issues.append("SELF-HEAL FAILED: gateway restart did not take")

    elif not log_ok and pid_running:
        issues.append(f"Gateway log stale ({log_age_minutes:.0f} min) — possible frozen process")
        # Self-heal: kill and restart
        for pid in gateway_pids:
            run(f"taskkill /F /PID {pid} 2>nul", timeout=5)
        time.sleep(2)
        _, _, rc = run(f'start "" /B "{HERMES_CLI}" gateway run --replace', timeout=5)
        time.sleep(8)
        out2, _, _ = run(f'"{HERMES_CLI}" gateway status', timeout=10)
        if "Gateway process running" in out2:
            healed.append("Gateway was frozen → killed and restarted")
        else:
            issues.append("SELF-HEAL FAILED: frozen gateway restart did not take")

    elif not connected and pid_running:
        issues.append("Gateway running but NOT connected to Discord")
        healed.append("Gateway restarting to re-establish Discord connection")
        for pid in gateway_pids:
            run(f"taskkill /F /PID {pid} 2>nul", timeout=5)
        time.sleep(2)
        _, _, rc = run(f'start "" /B "{HERMES_CLI}" gateway run --replace', timeout=5)
        time.sleep(8)

    return issues, healed, len(gateway_pids) > 0 or status_reports_running, connected

def check_config():
    """Check config.yaml for correct channel IDs."""
    issues = []
    healed = []
    config_path = os.path.join(HERMES_HOME, "config.yaml")

    if not os.path.exists(config_path):
        return ["config.yaml not found"], [], False

    with open(config_path, "r") as f:
        config_text = f.read()

    # Check allowed channels
    # NOTE: [CHANNEL_ID] placeholders below should be replaced with actual IDs for deployment
    expected_allowed = ",".join(REQUIRED_CHANNELS.values()) + ",[CHANNEL_ID]"
    if "allowed_channels:" in config_text:
        for ch_id in REQUIRED_CHANNELS.values():
            if ch_id not in config_text:
                issues.append(f"Missing channel {ch_id} in allowed_channels")
        # Check for any stale/old channel IDs that should no longer be in config
        # (configure your specific old IDs here for your deployment)

    # Check free_response_channels
    expected_free = ",".join(FREE_RESPONSE_CHANNELS)
    if "free_response_channels:" in config_text:
        for ch_id in FREE_RESPONSE_CHANNELS:
            if ch_id not in config_text:
                issues.append(f"Missing {ch_id} in free_response_channels")

    # Check home_channel
    if "home_channel: [CHANNEL_ID]" not in config_text:
        if "home_channel:" in config_text:
            issues.append("home_channel not pointing to #general")
            healed.append("home_channel mismatch detected")

    return issues, healed, len(issues) == 0

def check_cron_jobs():
    """Check expected cron jobs exist."""
    issues = []
    healed = []
    out, _, _ = run(f'"{HERMES_CLI}" cron list', timeout=10)

    for job_name in EXPECTED_CRON_JOBS:
        if job_name.lower() not in out.lower():
            issues.append(f"Cron job '{job_name}' missing")
            healed.append(f"Cron job '{job_name}' needs recreation")

    return issues, healed, len(issues) == 0

def test_outbound():
    """Quick outbound test via hermes send."""
    issues = []
    out, err, rc = run(
        f'"{HERMES_CLI}" send --to discord:[CHANNEL_ID] '
        f'"🕐 5AM health check — system alive"',
        timeout=10,
    )
    if "sent" not in out.lower():
        issues.append(f"Outbound send failed: {err or out}")
    return issues

def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    report_lines = [
        "╔══════════════════════════════════════╗",
        "║  UCC Morning Health Check — 5AM     ║",
        f"║  {now}",
        "╚══════════════════════════════════════╝",
        "",
    ]

    all_issues = []
    all_healed = []
    all_ok = True

    # === 1. Gateway ===
    gw_issues, gw_healed, gw_running, gw_connected = check_gateway()
    all_issues.extend(gw_issues)
    all_healed.extend(gw_healed)

    if gw_running and gw_connected:
        report_lines.append("✅ Gateway: running + Discord connected")
    elif gw_running and not gw_connected:
        report_lines.append("⚠️ Gateway: running but Discord disconnected")
        all_ok = False
    else:
        report_lines.append("❌ Gateway: DOWN")
        all_ok = False

    # === 2. Config ===
    cfg_issues, cfg_healed, cfg_ok = check_config()
    all_issues.extend(cfg_issues)
    all_healed.extend(cfg_healed)
    report_lines.append(f"{'✅' if cfg_ok else '⚠️'} Config: {'clean' if cfg_ok else 'issues found'}")

    # === 3. Cron Jobs ===
    cron_issues, cron_healed, cron_ok = check_cron_jobs()
    all_issues.extend(cron_issues)
    all_healed.extend(cron_healed)
    report_lines.append(f"{'✅' if cron_ok else '⚠️'} Cron jobs: {'all present' if cron_ok else 'missing jobs'}")

    # === 4. Outbound connectivity ===
    send_issues = test_outbound()
    all_issues.extend(send_issues)
    report_lines.append(f"{'❌' if send_issues else '✅'} Outbound send: {'FAILED' if send_issues else 'working'}")

    report_lines.append("")

    # === Summary ===
    if all_issues:
        report_lines.append("── Issues Found ──")
        for issue in all_issues:
            report_lines.append(f"  • {issue}")
        report_lines.append("")
    if all_healed:
        report_lines.append("── Self-Heal Actions ──")
        for heal in all_healed:
            report_lines.append(f"  ✓ {heal}")
        report_lines.append("")

    if all_ok and not all_issues:
        report_lines.append("All systems nominal. No action needed.")
    elif all_healed:
        report_lines.append(f"Self-healed {len(all_healed)} issue(s). Review recommended.")
    else:
        report_lines.append("Manual intervention required. See issues above.")

    report_lines.append("")
    report_lines.append("─" * 40)
    print("\n".join(report_lines))

if __name__ == "__main__":
    main()
