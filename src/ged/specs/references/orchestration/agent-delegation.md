# Agent Delegation Protocol

> How the orchestrator spawns subagents, collects results, and handles failures.

## Task Delegation Pattern

```
orchestrator
  |-- spawn(ged-researcher, {phase_goal})  -> RESEARCH.md
  |-- spawn(ged-planner, {research, phase_goal})  -> PLAN.md
  |-- validate plans (coverage, dependencies, feasibility)
  |   +-- if REVISE: loop back to planner (max 3 iterations)
  |-- for each wave:
  |   |-- spawn(ged-executor, {task_1})  -> artifacts + SUMMARY
  |   |-- spawn(ged-executor, {task_2})  -> artifacts + SUMMARY  (parallel)
  |   +-- verify_artifacts_on_disk()
  |-- spawn(ged-verifier, {phase_artifacts})  -> VERIFICATION-REPORT.md
  |   +-- if FAIL: create gap-closure plans, re-execute
  |-- spawn(ged-optimizer, {verified_design})  -> OPTIMIZATION-REPORT.md  (if optimization phase)
  +-- update STATE.md
```

## Artifact Recovery Protocol

**CRITICAL**: Never trust that a subagent's reported success means files were written.

After every subagent returns:
1. Parse the `ged_return` envelope from SUMMARY.md
2. Verify every file in `files_written` exists on disk
3. If missing: attempt to extract content from the agent's response text
4. If still missing: log error and flag for re-execution

## Return Envelope Parsing

Every subagent MUST produce a `ged_return:` YAML block in their SUMMARY.md:

```yaml
ged_return:
  status: completed | checkpoint | blocked | failed
  files_written: [...]
  files_modified: [...]
  issues: [...]
  next_actions: [...]
  claims_verified: [...]
  conventions_proposed: {field: value}
  verification_evidence: {...}
```

The orchestrator uses this structured data -- NOT the agent's prose -- to determine:
- Whether to proceed to the next wave
- What files to verify
- What convention proposals to evaluate
- What verification evidence to feed to the verifier

## Failure Handling

| Agent Status | Orchestrator Action |
|-------------|-------------------|
| `completed` | Verify artifacts, proceed |
| `checkpoint` | Save state, can resume later |
| `blocked` | Analyze blocker, may route to different agent |
| `failed` | Analyze failure, create targeted re-execution plan |

## Context Budget

Each subagent gets a fresh context window. The orchestrator targets ~15% of its own context for coordination. Budget allocation per phase type:

| Phase Type | Orchestrator | Planner | Executor | Verifier |
|-----------|-------------|---------|----------|----------|
| Problem definition | 10% | 5% | 70% | 15% |
| Loading analysis | 10% | 10% | 60% | 20% |
| Detailed analysis | 15% | 10% | 50% | 25% |
| Optimization | 10% | 5% | 55% | 30% |
| Report writing | 10% | 5% | 70% | 15% |
