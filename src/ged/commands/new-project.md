---
name: new-project
description: Initialize a new engineering analysis project
---

<process>

## Initialize New Engineering Analysis Project

### Step 1: Create project structure
Create the `.ged/` directory and all required subdirectories:
- `.ged/` — project state and config
- `.ged/observability/sessions/` — session logs
- `.ged/traces/` — execution traces
- `knowledge/` — technical knowledge base
- `reports/` — output reports and calculation packages
- `.scratch/` — temporary working files (gitignored)

### Step 2: Gather project information
Ask the user:
1. **Project name**: What is this engineering project?
2. **Structure type**: Building, bridge, tower, foundation, connection, etc.
3. **Domain**: Structural steel, reinforced concrete, timber, composite, geotechnical, etc.
4. **Design code**: Which code governs? (AISC, ACI, Eurocode, AASHTO, etc.)
5. **Model profile**: structural-analysis (default), preliminary-design, fea-intensive, code-checking, or report-writing?
6. **Analysis mode**: preliminary, detailed (default), optimization, or adaptive?

### Step 3: Create initial ROADMAP.md
Based on the project, create a phase breakdown:

```markdown
# [Project Name] — Roadmap

## Phase 1: Problem Definition
**Goal**: Define structural system, loads, and performance criteria

## Phase 2: Loading Analysis
**Goal**: Determine all loads and load combinations per [loading standard]

## Phase 3: Preliminary Design
**Goal**: Initial member sizing and system proportioning

## Phase 4: Detailed Analysis
**Goal**: Full structural analysis with code checks for all members

## Phase 5: Optimization
**Goal**: Optimize design for weight/cost while maintaining code compliance

## Phase 6: Verification
**Goal**: Independent checking of all calculations

## Phase 7: Reporting
**Goal**: Produce calculation package and engineering report
```

Adjust phases based on the specific project. Some projects need more phases (e.g., connection design, foundation design), some need fewer.

### Step 4: Initialize state
Create STATE.md and state.json with:
- Project name and creation date
- Phase listing from ROADMAP
- Phase 1 set as active
- Analysis mode and autonomy mode

### Step 5: Initialize config
Create `.ged/config.json` with user's choices.

### Step 6: Initialize git
If not already a git repo, initialize one. Add `.scratch/` to `.gitignore`.
Commit the initial project structure.

### Step 7: Convention prompting
Ask if the user wants to pre-set any conventions:
- Unit system (SI vs Imperial)
- Design code and edition
- Loading standard
- Safety factor method (LRFD vs ASD)
- Coordinate system orientation

Lock any conventions the user specifies.

### Step 8: Summary
Display:
- Project structure created
- Phases from roadmap
- Active conventions
- Next step: run `plan-phase` to begin Phase 1

</process>
