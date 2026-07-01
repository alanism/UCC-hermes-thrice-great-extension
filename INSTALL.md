# Install Hermes Thrice Great on Windows

These instructions install the generated profile payload into an isolated Hermes home. They do not install the repository root and do not require network access after the pinned Hermes runtime is available.

## Prerequisites

- Native Windows PowerShell.
- Python 3.11 or 3.12.
- Stock `hermes-agent==0.16.0` available as `hermes`.
- This repository checked out locally.

The acceptance baseline used Hermes commit `2a5dc0ef3df433a36abed9ee544ea067d807c438`.

## Build the install payload

From the repository root:

```powershell
$Repo = (Get-Location).Path
$Staging = Join-Path $Repo 'dist\hermes-thrice-great-profile'
python .\scripts\build_profile_staging.py --source $Repo --output $Staging
```

The builder creates a deny-by-default payload plus a sibling `.inventory.json`. Do not copy additional repository content into the payload.

## Install the public `ucc` profile

Choose an empty local Hermes root. Do not use a home containing real user or learner material.

```powershell
$HermesRoot = Join-Path $env:TEMP 'hermes-thrice-great-release'
if (Test-Path -LiteralPath $HermesRoot) {
    throw "Choose an empty Hermes root: $HermesRoot"
}
$env:HERMES_HOME = $HermesRoot
$env:HERMES_SAFE_MODE = '1'
$env:HERMES_ENABLE_PROJECT_PLUGINS = '0'

hermes profile install $Staging --name ucc --yes

$InstalledProfile = Join-Path $HermesRoot 'profiles\ucc'
$InstalledConfig = Join-Path $InstalledProfile 'config.yaml'
$ConfigText = [IO.File]::ReadAllText($InstalledConfig)
if (([regex]::Matches($ConfigText, '(?m)^plugins:$').Count -ne 1) -or
    (-not $ConfigText.Contains('  enabled: []'))) {
    throw 'Installed config does not match the release activation contract.'
}
$ConfigText = $ConfigText.Replace('  enabled: []', '  enabled: [hermes-thrice-great]')
[IO.File]::WriteAllText($InstalledConfig, $ConfigText, [Text.UTF8Encoding]::new($false))
$env:HERMES_HOME = $InstalledProfile
Remove-Item Env:HERMES_SAFE_MODE
```

Never run `hermes profile install $Repo`. Repository-root installation is intentionally rejected.

## Verify the installed commands

```powershell
hermes ucc doctor
hermes ucc validate --synthetic
hermes ucc validate --fixture valid/week.json
hermes ucc dry-run --synthetic
```

The commands emit deterministic JSON. Successful validation performs no ledger commit. A successful dry run executes seven stages and commits exactly once to temporary isolated storage.

The following checks must fail with a nonzero process exit:

```powershell
hermes ucc validate --synthetic --case invalid_totals
hermes ucc validate --fixture adversarial/week-cases.json
```

`invalid_totals` must report `RECEIPT_TOTAL_INCONSISTENT`; the adversarial fixture must report `APPROVAL_REQUIRED`. A failed run commits zero ledger entries.

## Equivalent public alias

To install the same generated payload under the long public name:

```powershell
$env:HERMES_HOME = $HermesRoot
$env:HERMES_SAFE_MODE = '1'
hermes profile install $Staging --name hermes-thrice-great --yes
$InstalledProfile = Join-Path $HermesRoot 'profiles\hermes-thrice-great'
$InstalledConfig = Join-Path $InstalledProfile 'config.yaml'
$ConfigText = [IO.File]::ReadAllText($InstalledConfig)
$ConfigText = $ConfigText.Replace('  enabled: []', '  enabled: [hermes-thrice-great]')
[IO.File]::WriteAllText($InstalledConfig, $ConfigText, [Text.UTF8Encoding]::new($false))
$env:HERMES_HOME = $InstalledProfile
Remove-Item Env:HERMES_SAFE_MODE
hermes ucc doctor
```

The optional name `thoth` is reserved for local compatibility only. It is not the default product identity and is not required for public use.

## Safety boundary

Use synthetic fixtures only. Do not add credentials, `.env`, learner records, local memories, network tools, MCP servers, messaging, Discord, Campaign OS, or external adapters. Stop if a command attempts a socket connection or model call.

For repeatable acceptance and troubleshooting, use [docs/active/OWNER_RUNBOOK.md](docs/active/OWNER_RUNBOOK.md).
