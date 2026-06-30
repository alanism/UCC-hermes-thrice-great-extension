# Determinism Map

| Surface | Class | Rule / comparison |
|---|---|---|
| JSON Schema validation | Deterministic | Same schema and document yield the same ordered issue codes. |
| Semantic receipt validation | Deterministic | Cross-field rules return stable issue codes and paths. |
| CALM/PRESSURE pairing | Deterministic | Versioned comparability policy and stable tie-breaking. |
| Pressure delta | Deterministic | Runs only on a valid pair; explicit denominator and rounding policy. |
| Diagnosis facts | Deterministic | Rule-derived facts only in the production core. |
| Parent brief data | Deterministic | Structured evidence/interpretation/recommendation sections. |
| Parent brief Markdown | Deterministic | Template render; no model prose in the production core. |
| Proposal/task card | Deterministic | Stable ID inputs and schema validation. |
| Approval transition | Deterministic | Append-only event evaluation by proposal revision. |
| Ledger write | Deterministic content, atomic side effect | Stable canonical JSON; volatile write timestamp isolated in envelope. |
| Skill discovery | Deterministic for pinned Hermes | Sorted paths; unique names; all references resolved. |
| Profile install | Deterministic for pinned Hermes | Same distribution commit produces the same distribution-owned files. |
| Build receipts | Partly volatile | Timestamp/agent vary; commands, hashes, and outcomes are factual. |
| Optional model reasoning | Nondeterministic and outside the offline production core | Must never govern deterministic facts or approval. |
| Mock adapters | Deterministic | Contract input maps to captured output; no network. |

## Repeatability rule

Tests compare canonical semantic payloads. Volatile envelope fields are either injected clocks/IDs or excluded explicitly; they may not be silently ignored.
