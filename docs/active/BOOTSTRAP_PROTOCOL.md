# ACDF Bootstrap Protocol

Status: DEFINED, NOT AUTHORIZED.

## Problem

Gate A1's machine claim/state validators do not exist until Phase 2, but repository recon and the governance tasks that create those validators necessarily occur first. This protocol prevents that bootstrap dependency from becoming an excuse for unclaimed product work.

## Human authorization required

Before any task is executed, the human owner must add a dated declaration to this file naming:

- repository root;
- permitted bootstrap task IDs;
- agent ID;
- allowed environment;
- forbidden actions;
- expiration condition.

No declaration is currently present. Therefore no bootstrap task is authorized.

## Maximum bootstrap scope

Only T0.*, H1.*, and A2.* tasks may be named. Allowed work is limited to read-only recon, planning evidence, Git initialization specifically authorized by A2.1, and test-first governance machinery.

Forbidden during bootstrap:

- product/plugin/profile/schema/skill implementation;
- real or semi-real learner data;
- live model, network, messaging, Discord, or Campaign OS actions;
- Hermes source edits or updates;
- weakening authority, tests, privacy, ignore rules, or stop conditions.

## Manual controls until A1

Each bootstrap task still requires:

1. a JSON claim at `.agent/claims/<task-id>.<agent-id>.json` with all normal fields;
2. manual verification that its `active_plan_hash` matches `authority.json`;
3. matching `.agent/state.log` events;
4. allowed/forbidden-file review before and after work;
5. a receipt before DONE;
6. one task in progress at a time.

The absence of the future checker does not waive the data contract.

## Expiration

The bootstrap exception expires automatically when Gate A1 passes. After that point, machine claim/state validation is mandatory and this file cannot authorize any task.

## Human declaration

Not yet provided.
