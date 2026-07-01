# Post-Release Tasks

## Proposed D13.1 — Human-gated upstream Hermes drift review

Status: **PROPOSED / NOT CLAIMABLE**

Earliest review date: 2027-01-01

Trigger: human authorization that adds D13.1 to the active task board and permits the required network comparison.

Goal: measure the jagged frontier against then-current Hermes without silently changing the accepted release.

Required work after authorization:

1. Record the accepted baseline package `hermes-agent==0.16.0` and commit `2a5dc0ef3df433a36abed9ee544ea067d807c438`.
2. Fetch or inspect upstream only inside an isolated comparison boundary.
3. Produce a compatibility/security diff without modifying the accepted checkout.
4. Re-run H1 identity/profile probes, R4 canaries, installed CLI acceptance, aliases, containment, and full F1 on a candidate pin.
5. Require a human decision before changing the pin or merging upstream.

No fetch, update, vendoring, merge, or Hermes source modification occurred during F12.3.
