# Structural Analysis Protocols

> Step-by-step methodology guides for structural engineering analysis.

## Protocol: Steel Beam Design

### When to Use
Designing steel beams for bending, shear, and serviceability.

### Steps
1. **Define loading** — dead, live, and any lateral loads on the beam
2. **Determine load combinations** — per ASCE 7-22 or equivalent
3. **Calculate demand** — maximum moment M_u, shear V_u, deflection
4. **Select trial section** — from AISC Manual Table 3-2 (by Z_x)
5. **Check flexural strength** — AISC 360 Chapter F (compact, noncompact, slender)
6. **Check shear strength** — AISC 360 Chapter G
7. **Check lateral-torsional buckling** — unbraced length L_b vs. L_p, L_r
8. **Check deflection** — L/360 live, L/240 total (or project criteria)
9. **Check web crippling and yielding** — if concentrated loads present
10. **Document** — calculation with all code references

### Common LLM Pitfalls
- Using S_x (elastic) instead of Z_x (plastic) for LRFD (E005)
- Missing lateral-torsional buckling check (E004)
- Wrong deflection limit (L/360 for live load, not total load)
- Forgetting self-weight in the dead load (E012)

---

## Protocol: Steel Column Design

### When to Use
Designing steel columns for axial compression, combined axial and bending.

### Steps
1. **Define loads** — axial P_u and moments M_ux, M_uy at each end
2. **Determine effective length** — K factor for each axis
3. **Select trial section** — from AISC Manual Table 4-1a (by phi*P_n)
4. **Check axial capacity** — AISC 360 Chapter E (flexural, torsional, flexural-torsional buckling)
5. **Check combined loading** — AISC 360 Chapter H, Eq. H1-1a or H1-1b
6. **Check local buckling** — width-to-thickness ratios per Table B4.1a
7. **Check slenderness** — KL/r limits
8. **Verify P-delta effects** — use Direct Analysis Method if applicable
9. **Document** — calculation with interaction equation shown

### Common LLM Pitfalls
- Using K=1.0 for all cases regardless of end conditions (E008)
- Not checking both strong-axis and weak-axis buckling
- Forgetting to check the correct interaction equation (H1-1a vs. H1-1b) (E014)
- Missing torsional or flexural-torsional buckling for certain sections

---

## Protocol: Reinforced Concrete Beam Design

### When to Use
Designing RC beams for flexure, shear, and serviceability per ACI 318.

### Steps
1. **Define loading and demand** — M_u, V_u from analysis
2. **Establish material properties** — f'c, f_y, clear cover, bar sizes
3. **Check minimum dimensions** — ACI 318 Table 9.3.1.1 (minimum h)
4. **Design for flexure** — compute required A_s from M_u = phi*A_s*f_y*(d - a/2)
5. **Check minimum and maximum reinforcement** — ACI 318 Section 9.6
6. **Design for shear** — V_c + V_s >= V_u/phi per ACI 318 Section 22.5
7. **Check stirrup spacing** — maximum spacing limits per ACI 318 Section 9.7
8. **Check deflection** — immediate and long-term per ACI 318 Section 24.2
9. **Check crack control** — per ACI 318 Section 24.3
10. **Detail reinforcement** — development lengths, bar cutoffs, lap splices

### Common LLM Pitfalls
- Forgetting the phi factor (0.90 for flexure, 0.75 for shear) (E002)
- Using the wrong value of d (effective depth vs. total depth)
- Not checking both minimum AND maximum reinforcement ratios
- Ignoring long-term deflection multipliers

---

## Protocol: Load Takeoff

### When to Use
Establishing dead, live, wind, seismic, snow, and other loads for a structure.

### Steps
1. **Dead load** — self-weight of structure + superimposed dead (MEP, ceiling, finishes)
2. **Live load** — per occupancy from ASCE 7-22 Table 4.3-1; apply reduction per Section 4.7
3. **Wind load** — ASCE 7-22 Chapter 26-31; determine V, exposure, K_z, G, C_p
4. **Seismic load** — ASCE 7-22 Chapter 11-12; determine S_DS, S_D1, R, C_s, base shear
5. **Snow load** — ASCE 7-22 Chapter 7; ground snow load, exposure, thermal, importance
6. **Rain load** — ponding potential per ASCE 7-22 Chapter 8
7. **Load combinations** — ASCE 7-22 Section 2.3 (LRFD) or 2.4 (ASD)
8. **Tributary areas** — assign loads to members based on geometry
9. **Verify** — total gravity load = sum of all floor loads (sanity check)

### Common LLM Pitfalls
- Missing load combinations, especially uplift cases (E002)
- Incorrect live load reduction application
- Wrong wind exposure category or terrain
- Forgetting to apply importance factor to seismic loads
- Tributary area errors (E010)

---

## Protocol: FEA Model Validation

### When to Use
Validating a finite element analysis model before using results for design.

### Steps
1. **Geometry check** — dimensions match drawings, member positions correct
2. **Boundary conditions** — supports match physical conditions (pin, roller, fixed)
3. **Loading verification** — total applied load matches hand-calculated total
4. **Equilibrium check** — sum of reactions = sum of applied loads
5. **Mesh convergence** — run 3+ mesh densities, plot peak stress vs. elements
6. **Known solution comparison** — compare simple member to hand calculation
7. **Deformed shape check** — does the deflected shape make physical sense?
8. **Stress distribution** — are stress patterns physically reasonable?
9. **Warning review** — check all solver warnings and errors
10. **Document** — record all validation steps and results

### Common LLM Pitfalls
- Accepting results without mesh convergence study
- Not checking equilibrium (reactions vs. loads)
- Missing warning messages from the solver
- Using results from a mesh with poor element quality
