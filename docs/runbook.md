# UCC Learning Campaign OS Runbook

## Start

- Development: `npm run dev`
- Production preview: `npm run build && npm run preview -- --host 127.0.0.1`
- Local companion development: `UCC_COMPANION_ROLE=owner UCC_COMPANION_TOKEN='<24+ random characters>' UCC_SYNC_DIR='<private path>' npm run dev:companion`
- Local companion normal start: `UCC_COMPANION_ROLE=owner UCC_COMPANION_TOKEN='<24+ random characters>' UCC_SYNC_DIR='<private path>' npm run companion`

The companion always binds to `127.0.0.1:4174`. Never change it to a remote interface.

## Verify

- Full gate: `npm run verify`
- Full gate including rendered Chromium and accessibility checks: `npm run verify:full`
- Application tests: `npm test`
- Benchmark validators and smoke tests: `npm run test:benchmarks`
- Typecheck and production build: `npm run build`
- Healthy means all tests pass, build exits 0, `/api/v1/health` returns `status: ok` locally, benchmark search returns pack results, public contract URLs return JSON, and the browser console has no application errors.

## Release

Cloud Run target:

- Project: `uncommoncore`
- Region: `asia-southeast1`
- Service: `ucc-learning-campaign`
- Deploy: `gcloud run deploy ucc-learning-campaign --source . --project uncommoncore --region asia-southeast1 --allow-unauthenticated`
- Public URL: `https://ucc-learning-campaign-wbg25ukt3a-as.a.run.app`

The release artifact must include `dist/benchmarks/*/ontology/`, `dist/schemas/`, `dist/examples/`, `dist/agent/hermes.json`, and `dist/openapi.json`. It must not include companion tokens or synchronized learner records.

## Monitoring and Recovery

- Smoke-test plan import, benchmark search, Markdown/JSON export, browser restoration, and overlay review after each release.
- Confirm the public `/api/v1/plans` path is unavailable; learner write APIs are local-only.
- Daily companion check: review pending event files, rejected/conflicting events, last canonical revision, and sync-provider conflicts.
- Healthy sync has one owner writer, immutable Hermes event files, one decision per reviewed event, and no files in `quarantine/`.
- If benchmark search fails, confirm ontology assets exist under `dist/benchmarks/` and rebuild.
- If import fails, preserve the source file and inspect the validation error; do not bypass validation.
- If a proposal has a stale `baseRevision`, reject it, let Hermes read the latest snapshot, and resubmit with a new idempotency key.
- If a sync provider creates a conflict copy, stop both companions, preserve both files, compare revisions and hashes, and let the owner choose the canonical record. Do not merge learner JSON by hand without validation.
- Backup by copying the entire synchronized directory while both companions are stopped. Recovery restores that directory, runs `npm test`, then starts the owner companion first.
- Rotate a token by stopping that local companion, replacing `UCC_COMPANION_TOKEN`, and restarting. Tokens are never stored in the sync directory.
- List revisions: `gcloud run revisions list --service ucc-learning-campaign --project uncommoncore --region asia-southeast1`
- Roll back traffic: `gcloud run services update-traffic ucc-learning-campaign --project uncommoncore --region asia-southeast1 --to-revisions REVISION=100`

## Security

- Treat imported Markdown/JSON and benchmark text as untrusted.
- Never interpolate unescaped imported values into HTML.
- Do not place learner data or secrets in benchmark packs or build logs.
- Keep `UCC_COMPANION_TOKEN` out of shell history where possible and restrict sync-folder access to the owner and Hermes host.
- Escalate suspected disclosure by stopping both companions, revoking sync access, rotating tokens, preserving audit files, and reviewing exported/received events before resuming.
