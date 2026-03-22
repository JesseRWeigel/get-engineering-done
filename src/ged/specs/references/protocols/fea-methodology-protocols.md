# FEA Methodology Protocols

> Step-by-step methodology guides for finite element analysis in engineering.

## Protocol: Linear Static Analysis

### When to Use
Standard structural analysis for service and ultimate loads; no significant geometric or material nonlinearity.

### Steps
1. **Define geometry** — create model from structural drawings
2. **Assign materials** — E, nu, Fy, density from locked material_source convention
3. **Assign sections** — member cross-sections from design or trial sizing
4. **Define boundary conditions** — supports per structural intent (pin, roller, fixed)
5. **Apply loads** — per each load case from loading analysis
6. **Run analysis** — linear static solver
7. **Post-process** — extract forces, moments, reactions, deflections
8. **Validate** — equilibrium check, deformed shape review, hand-calc comparison
9. **Iterate** — if results show inadequacy, resize and re-run

### Mesh Guidelines
- Beams/columns: minimum 4 elements per member for reasonable accuracy
- Plates/shells: target element size = min(thickness, span/20)
- Solids: mesh refinement at stress concentrations (2-3 elements through thickness)
- Maximum aspect ratio: 5:1 for beams, 3:1 for shells, 4:1 for solids

### Convergence Criteria
- Force residual: < 0.1% of maximum applied force
- Displacement: converged when peak displacement changes < 1% between mesh refinements

---

## Protocol: Buckling Analysis

### When to Use
Determining elastic critical buckling loads and mode shapes for stability assessment.

### Steps
1. **Create validated model** — from linear static analysis (validated)
2. **Apply reference load** — typically the factored gravity load combination
3. **Run eigenvalue buckling** — extract first 10+ modes
4. **Review mode shapes** — identify physical buckling modes vs. numerical artifacts
5. **Compute buckling load factors** — lambda_cr for each mode
6. **Check adequacy** — lambda_cr should exceed required safety factor
7. **Cross-check** — compare critical column loads with Euler/code predictions
8. **If lambda_cr < threshold** — add bracing, increase member sizes, or change system

### Interpretation
- lambda_cr < 1.0: Structure buckles BEFORE reaching design load — REDESIGN
- 1.0 < lambda_cr < 2.5: P-delta effects significant — use second-order analysis
- lambda_cr > 10: Buckling not governing — linear analysis likely adequate
- Local modes (plate buckling): may need stiffeners or thicker plates

### Common LLM Pitfalls
- Confusing linear buckling eigenvalue with actual collapse load
- Not including enough modes (local modes may be critical)
- Missing lateral-torsional buckling modes by only requesting axial modes
- Forgetting imperfection sensitivity for shell structures

---

## Protocol: Nonlinear Static Analysis (Pushover)

### When to Use
Seismic performance assessment, progressive collapse evaluation, or when material/geometric nonlinearity is significant.

### Steps
1. **Create validated linear model** — start from linear static analysis
2. **Define material nonlinearity** — stress-strain curves, plastic hinges
3. **Define geometric nonlinearity** — P-delta, large deformation if needed
4. **Define load pattern** — gravity (constant) + lateral (incremental)
5. **Set solution parameters** — load increments, convergence criteria, max iterations
6. **Run pushover** — displacement-controlled or force-controlled
7. **Extract capacity curve** — base shear vs. roof displacement
8. **Evaluate performance** — check against ASCE 41-17 acceptance criteria
9. **Document hinge sequence** — which hinges form, in what order

### Convergence Settings
- Force tolerance: 0.1% of total applied force
- Displacement tolerance: 0.01% of characteristic dimension
- Energy tolerance: 0.001% of external work
- Maximum iterations per step: 25-50
- If non-convergence: reduce step size, try arc-length method

### Common LLM Pitfalls
- Using load-controlled analysis when displacement control is needed (snap-through)
- Setting convergence tolerance too loose (results look converged but are wrong)
- Not verifying energy balance (external work vs. internal energy)
- Incorrectly defining plastic hinge properties

---

## Protocol: Dynamic / Modal Analysis

### When to Use
Natural frequency determination, seismic response spectrum analysis, wind dynamic response.

### Steps
1. **Create validated model** — with correct mass distribution
2. **Define mass source** — dead load + fraction of live load (per code)
3. **Run modal analysis** — extract first N modes (enough for 90% mass participation)
4. **Review mode shapes** — verify physical reasonableness
5. **Check mass participation** — must reach 90% in each direction
6. **Apply response spectrum** — per ASCE 7-22 Section 12.9 or equivalent
7. **Combine modes** — CQC (preferred) or SRSS combination rule
8. **Extract design forces** — combine with gravity per load combinations
9. **Check drift** — story drift per ASCE 7-22 Table 12.12-1

### Mass Modeling
- Include all dead load mass
- Include 25% of storage live load (ASCE 7-22 Section 12.7.2)
- Include partition weight if applicable
- Model at floor diaphragm levels (lumped mass approach)

### Common LLM Pitfalls
- Not extracting enough modes to reach 90% mass participation
- Using SRSS when CQC is required (closely-spaced modes)
- Forgetting to include accidental torsion
- Applying response spectrum to wrong axis

---

## Protocol: Mesh Convergence Study

### When to Use
Any FEA analysis where results will be used for design decisions.

### Steps
1. **Define quantity of interest** — peak stress, maximum deflection, reaction force
2. **Create coarse mesh** — mesh factor 1.0x (baseline)
3. **Run analysis** — extract quantity of interest
4. **Refine mesh** — mesh factor 0.5x (doubled density)
5. **Run analysis** — extract quantity of interest
6. **Refine again** — mesh factor 0.25x (quadrupled density)
7. **Plot convergence** — quantity vs. mesh density (or DOF count)
8. **Check convergence** — is the change < 5% between last two refinements?
9. **Select design mesh** — coarsest mesh that gives converged results
10. **Document** — convergence plot and selected mesh justification

### Convergence Criteria
- Stress: < 5% change between successive refinements
- Displacement: < 2% change between successive refinements
- Reaction forces: < 1% change between successive refinements
- If not converging: check for singularities, re-mesh problem areas

### Common LLM Pitfalls
- Only running 2 mesh densities (need minimum 3 for a convergence trend)
- Refining everywhere instead of targeting high-gradient regions
- Ignoring stress singularities at sharp corners (use averaged stress or move evaluation point)
- Declaring convergence when only global quantities converge (local stresses may not)
