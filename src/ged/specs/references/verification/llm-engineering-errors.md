# Known LLM Engineering Analysis Failure Modes

> This catalog documents systematic failure patterns of LLMs in engineering calculations.
> The verifier and plan-checker cross-reference against these patterns.

## Critical Errors (High Frequency)

### E001: Unit Conversion Errors
**Pattern**: Incorrect conversion between unit systems or within a system.
**Example**: Converting kN to lb using 1 kN = 1000 lb (correct: 224.8 lb). Mixing ksi and MPa in the same calculation. Using mm when the formula expects m.
**Guard**: State units on every line. Verify unit conversion factors from a reference table. Perform dimensional analysis on final results.

### E002: Load Combination Errors
**Pattern**: Missing load combinations, wrong load factors, or incomplete LRFD/ASD combinations.
**Example**: Using 1.2D + 1.6L but forgetting 1.2D + 1.0W + 0.5L. Applying ASD factors when the code check uses LRFD. Missing the 0.9D - 1.0W uplift combination.
**Guard**: List ALL load combinations from the loading standard before starting design checks. Verify against ASCE 7-22 Section 2.3 or equivalent.

### E003: Wrong Code Edition
**Pattern**: Using provisions from an older or different edition of the design code.
**Example**: Using AISC 360-16 beam stability provisions when the project specifies AISC 360-22. Using Eurocode steel provisions for a US project. Citing ACI 318-14 when ACI 318-19 changed the provision.
**Guard**: Lock the code edition in conventions. Verify clause numbers match the locked edition. Be especially careful with provisions that changed between editions.

### E004: Missing Stability Checks
**Pattern**: Checking strength but forgetting stability (buckling, overturning, P-delta).
**Example**: Designing a column for axial strength but not checking buckling. Sizing a beam for bending but missing lateral-torsional buckling. Ignoring P-delta effects in a tall frame.
**Guard**: For every compression member, check ALL buckling modes. For every beam, check LTB. For every frame, evaluate P-delta significance.

### E005: Incorrect Section Properties
**Pattern**: Using wrong moment of inertia, section modulus, or area for a member.
**Example**: Using S_x (elastic) when Z_x (plastic) is required for LRFD. Confusing strong-axis and weak-axis properties. Using gross area when net area is required.
**Guard**: Look up section properties from the AISC Manual or equivalent. State which property is used and why. Double-check strong vs. weak axis.

## Serious Errors (Medium Frequency)

### E006: Sign Convention Errors
**Pattern**: Inconsistent sign conventions leading to wrong force directions.
**Example**: Treating compression as positive in one calculation and negative in another. Getting the wrong moment direction from a free-body diagram. Wind load applied in wrong direction.
**Guard**: State sign convention at the start of every calculation. Mark tension/compression explicitly. Draw free-body diagrams.

### E007: Connection Design Oversights
**Pattern**: Designing members but not connections, or using incorrect connection assumptions.
**Example**: Designing a moment frame but assuming pinned connections in the analysis. Using shear-only connections where moment transfer is needed. Forgetting to check bolt bearing, tear-out, and block shear.
**Guard**: Every connection must be designed for the forces it must transfer. Check ALL failure modes per the code (bolt shear, bearing, plate yielding, block shear, weld, etc.).

### E008: Effective Length Factor Errors
**Pattern**: Using K=1.0 for all columns regardless of end conditions.
**Example**: Using K=1.0 for a cantilever column (should be K=2.0). Using K=1.0 in an unbraced frame (K>1.0). Not distinguishing between braced and unbraced frames.
**Guard**: Determine effective length factor from end conditions and frame bracing. Use alignment charts or direct analysis method. Be conservative if uncertain.

### E009: Serviceability Limit Omissions
**Pattern**: Checking strength but forgetting deflection, drift, or vibration limits.
**Example**: A beam that passes bending checks but deflects L/120 instead of the required L/360. A frame that meets strength but exceeds H/400 story drift. Floor vibrations not checked against human comfort criteria.
**Guard**: After every strength check, immediately check the applicable serviceability limit. List ALL serviceability criteria at the start of the project.

### E010: Tributary Area Errors
**Pattern**: Incorrect load distribution to members based on wrong tributary areas.
**Example**: Using half the bay width when the load distributes to one-third points. Double-counting loads where tributary areas overlap. Forgetting to include cladding loads on perimeter beams.
**Guard**: Draw tributary area diagrams. Verify that the sum of all tributary area loads equals the total applied load (equilibrium check).

## Moderate Errors (Common but Usually Caught)

### E011: Interpolation and Table Lookup Errors
**Pattern**: Incorrect interpolation from design tables or charts.
**Example**: Linear interpolation in a table that requires logarithmic interpolation. Reading the wrong row/column in a design table. Using a table that applies to a different steel grade.
**Guard**: State the table reference, input values, and interpolation method. Verify with adjacent table entries that the result makes sense.

### E012: Neglecting Self-Weight
**Pattern**: Forgetting to include the structure's own weight in the dead load.
**Example**: Calculating beam design loads without including the beam's self-weight. Forgetting concrete slab self-weight in a composite design. Not including the weight of fireproofing, MEP, and ceiling.
**Guard**: Always include self-weight as the first item in dead load takeoff. Use an estimated member weight initially, then verify after sizing.

### E013: Thermal and Settlement Effects
**Pattern**: Ignoring thermal expansion/contraction or differential settlement.
**Example**: A long building without expansion joints developing large thermal forces. Differential settlement between adjacent columns causing frame distortion. Temperature gradient in a bridge deck ignored.
**Guard**: Check if the structure length exceeds typical expansion joint limits (~60m for steel, ~45m for concrete). Evaluate settlement differences from geotechnical data.

### E014: Incorrect Demand-to-Capacity Ratio
**Pattern**: Computing the ratio incorrectly or comparing the wrong quantities.
**Example**: Comparing factored demand to unfactored capacity. Using the wrong interaction equation (H1-1a vs. H1-1b). Not including all relevant force components in the interaction check.
**Guard**: Clearly label factored vs. unfactored quantities. Cite the specific interaction equation. Show all terms in the interaction check.

### E015: Weld and Bolt Specification Errors
**Pattern**: Specifying incorrect weld sizes, bolt grades, or fastener details.
**Example**: Specifying E70XX welds for a connection requiring E80XX. Using A325 bolt capacity for A490 bolts. Undersizing fillet welds by forgetting the 0.707 throat factor.
**Guard**: Verify weld electrode matches base metal requirements. Use correct bolt capacity tables for the specified grade. Apply correct geometric factors (throat, grip length, etc.).

## How to Use This Catalog

1. **Plan-checker**: Before execution, identify tasks where specific errors are likely. Add explicit guards.
2. **Executor**: Consult relevant entries when performing work of that type. Follow guards.
3. **Verifier**: After execution, cross-reference results against applicable error patterns.
4. **Pattern library**: When a new error pattern is discovered, add it here.
