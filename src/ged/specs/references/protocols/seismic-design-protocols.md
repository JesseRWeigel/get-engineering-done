# Seismic Design Protocols

> Step-by-step methodology guides for earthquake-resistant structural design.

## Protocol: Equivalent Lateral Force (ELF) Method

### When to Use
Preliminary seismic design of regular, low-to-mid-rise structures where higher modes are not significant (ASCE 7 §12.8).

### Steps
1. **Determine the seismic design parameters** — site class (A–F from soil investigation), mapped spectral accelerations S_S and S_1 from USGS hazard maps, site coefficients F_a and F_v, design spectral accelerations S_DS = (2/3)F_a S_S and S_D1 = (2/3)F_v S_1
2. **Assign the Seismic Design Category (SDC)** — based on S_DS, S_D1, and Risk Category (I–IV from occupancy); SDC A through F determines required analysis procedures and detailing
3. **Determine the fundamental period** — approximate T_a = C_t h_n^x (C_t and x from ASCE 7 Table 12.8-2), subject to upper limit C_u T_a; or compute from modal analysis (but cannot exceed C_u T_a for base shear)
4. **Compute the seismic response coefficient** — C_s = S_DS/(R/I_e), but not less than 0.044 S_DS I_e and not less than 0.01; check C_s = S_D1/(T(R/I_e)) for the long-period limit
5. **Compute base shear** — V = C_s W, where W = seismic weight (dead load + applicable portions of live, snow, storage)
6. **Distribute vertically** — F_x = C_vx V, where C_vx = w_x h_x^k / Σ w_i h_i^k (k = 1 for T ≤ 0.5s, k = 2 for T ≥ 2.5s, interpolate between)
7. **Apply accidental torsion** — displace the center of mass by ±5% of the building dimension perpendicular to the direction of force
8. **Check drift limits** — story drift Δ = δ_xe C_d / I_e ≤ allowable (typically 0.020 h_sx for Risk Category I/II); design for the more restrictive of strength or drift

### Common LLM Pitfalls
- Using the approximate period without the upper limit C_u T_a (can significantly underestimate base shear)
- Forgetting to check the minimum C_s values (especially important in low-seismicity regions)
- Applying ELF to irregular structures where modal response spectrum analysis is required
- Confusing R (response modification coefficient) with C_d (deflection amplification factor) — R reduces forces, C_d amplifies elastic drifts

---

## Protocol: Response Spectrum Analysis

### When to Use
Seismic design of structures with irregularities, tall buildings, or when higher modes contribute significantly to the response (ASCE 7 §12.9).

### Steps
1. **Construct the design response spectrum** — plot S_a vs T using S_DS (short period plateau), S_D1 (descending branch S_D1/T), and T_L (long-period transition to S_D1 T_L/T²)
2. **Build the structural model** — include member stiffnesses (consider cracked sections for concrete: 0.35 I_g for beams, 0.70 I_g for columns per ACI 318), mass distribution, boundary conditions, diaphragm rigidity
3. **Perform modal analysis** — extract natural periods and mode shapes; include enough modes to capture ≥ 90% of total mass participation in each direction
4. **Compute modal responses** — for each mode j, compute the modal base shear V_j = S_a(T_j) × effective modal mass; compute story forces, displacements, and member forces
5. **Combine modal responses** — use CQC (Complete Quadratic Combination) if modes are closely spaced (Δf/f < 10%); SRSS (Square Root of Sum of Squares) if well-separated
6. **Scale the base shear** — if the combined modal base shear < 100% of ELF base shear (using C_u T_a), scale all forces up to match (ASCE 7 §12.9.4.1, as amended in recent editions)
7. **Apply accidental torsion** — same ±5% eccentricity; if torsional irregularity exists, amplify by A_x = (δ_max/(1.2 δ_avg))² ≤ 3.0
8. **Combine orthogonal directions** — use 100% in one direction + 30% in the orthogonal direction, or SRSS of orthogonal responses

### Common LLM Pitfalls
- Using SRSS for closely spaced modes (CQC is required to account for modal correlation)
- Not including enough modes (must capture ≥ 90% mass participation; tall or irregular buildings may need many modes)
- Forgetting to scale modal results up to the ELF base shear minimum
- Using uncracked section properties for reinforced concrete (overestimates stiffness, underestimates period, overestimates forces — non-conservative for drift, unconservative for force)

---

## Protocol: Performance-Based Seismic Design (PBSD)

### When to Use
Designing structures to meet specific performance objectives at multiple hazard levels — beyond code-minimum prescriptive design.

### Steps
1. **Define performance objectives** — map each hazard level to a target performance level:
   - **Frequent earthquake** (50% in 30 yr, ~43-yr return): Immediate Occupancy (IO)
   - **Design earthquake** (10% in 50 yr, ~475-yr return): Life Safety (LS)
   - **Maximum Considered Earthquake (MCE)** (2% in 50 yr, ~2475-yr return): Collapse Prevention (CP)
2. **Select the analysis procedure** — nonlinear static (pushover) or nonlinear response history analysis (NLRHA); ASCE 41 or ASCE 7 Chapter 16
3. **For pushover analysis**: apply incrementally increasing lateral loads with a distribution matching the fundamental mode; plot base shear vs roof displacement; identify yield point, target displacement (ASCE 41 coefficient method or ATC-40 capacity spectrum method), and limit states
4. **For NLRHA**: select and scale ground motion records (minimum 7 per ASCE 7 §16.2; match the target spectrum over the period range 0.2T₁ to 2T₁); model material and geometric nonlinearity; run all records and assess using the mean response
5. **Check acceptance criteria** — compare member demands (plastic hinge rotations, shear forces, axial loads) to acceptance limits for the target performance level (ASCE 41 Tables for steel, concrete, masonry, wood)
6. **Assess collapse probability** — for MCE, the target is ≤ 10% probability of collapse (ASCE 7 risk-targeted approach); use incremental dynamic analysis (IDA) or fragility curves
7. **Iterate** — if performance objectives are not met, strengthen members, add supplemental damping, or use seismic isolation
8. **Peer review** — PBSD designs exceeding code provisions require independent peer review per most building codes

### Common LLM Pitfalls
- Confusing DBE (Design Basis Earthquake) with MCE (Maximum Considered Earthquake) — MCE is approximately 1.5× DBE
- Using linear analysis results for performance-based assessment (PBSD requires nonlinear modeling to capture yielding, degradation, and redistribution)
- Selecting and scaling ground motions without matching the target spectrum over the appropriate period range
- Not accounting for P-delta effects in nonlinear analysis (can trigger progressive collapse in tall or flexible structures)
