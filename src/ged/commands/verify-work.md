---
name: verify-work
description: Run the 12-check engineering verification framework
---

<process>

## Verify Work

### Overview
Run post-hoc verification on completed phase work using the 12-check framework.

### Step 1: Collect Artifacts
Gather all output from the current phase:
- Calculation files (markdown/LaTeX)
- FEA model files and results
- SUMMARY files from executors

### Step 2: Build Evidence Registry
Extract verification evidence from artifacts:
- Unit consistency across all calculations
- Equilibrium checks (reactions vs. applied loads)
- Code clause references and compliance status
- Convergence study results (if FEA)
- Material stress/strain vs. limits

### Step 3: Run Verification
Spawn ged-verifier with:
- All phase artifacts
- Evidence registry
- Convention locks
- LLM error catalog

### Step 4: Process Verdict
Parse the VERIFICATION-REPORT.md:
- If PASS: record in state, proceed
- If PARTIAL: create targeted gap-closure for MAJOR failures
- If FAIL: create gap-closure for CRITICAL failures, block downstream

### Step 5: Route Failures
For each failure, route to the appropriate agent:
- Unit errors — ged-executor (targeted recalculation)
- Equilibrium failures — ged-executor (free-body re-analysis)
- Code violations — ged-executor (specific clause check)
- Stability failures — ged-optimizer (redesign)
- Convergence failures — ged-executor (refined mesh/solver settings)

### Step 6: Update State
Record verification results in STATE.md:
- Verdict hash (content-addressed)
- Pass/fail counts
- Any unresolved issues

</process>
