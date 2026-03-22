---
name: plan-phase
description: Plan the current phase — research, plan, and validate before execution
---

<process>

## Plan Phase

### Overview
Before execution, create validated plans for the current phase:
1. Research the domain (ged-researcher)
2. Create plans (ged-planner)
3. Validate plans (ged-verifier in plan-check mode)
4. Iterate until plans pass validation

### Step 1: Domain Research
Spawn ged-researcher with:
- Phase goal from ROADMAP.md
- Current convention locks
- Analysis mode parameters

Collect RESEARCH.md output.

### Step 2: Plan Creation
Spawn ged-planner with:
- Phase goal
- RESEARCH.md findings
- Convention locks
- Task sizing constraints (max 8-10 tasks per plan)

Collect PLAN-XX-YY.md files.

### Step 3: Plan Validation
For each plan, verify:
- Coverage: does the plan address all requirements?
- Dependencies: are task dependencies correct?
- Feasibility: is each task sized appropriately?
- Convention coverage: are needed conventions locked?
- Error awareness: are known LLM failure modes guarded against?

### Step 4: Revision Loop
If validation returns REVISE:
1. Feed revision recommendations back to ged-planner
2. Planner revises the plan
3. Re-validate
4. Maximum 3 iterations

If validation returns REJECT after 3 iterations:
- Present issues to user
- Ask for guidance on approach

### Step 5: Commit and Present
Once plans are validated:
1. Commit all PLAN.md files
2. Display plan summary to user
3. Show wave structure (what runs in parallel)
4. If autonomy is 'supervised': wait for user approval
5. If autonomy is 'balanced' or 'yolo': proceed to execute-phase

</process>
