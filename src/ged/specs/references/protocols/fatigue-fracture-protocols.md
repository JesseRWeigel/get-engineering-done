# Fatigue and Fracture Protocols

> Step-by-step methodology guides for fatigue life prediction and fracture mechanics analysis.

## Protocol: S-N Curve Fatigue Analysis

### When to Use
Estimating fatigue life under constant-amplitude cyclic loading using stress-life methods.

### Steps
1. **Characterize the loading** — determine the stress amplitude S_a, mean stress S_m, stress ratio R = S_min/S_max, and loading type (axial, bending, torsion)
2. **Obtain the S-N curve** — from material test data, standards (e.g., ASTM, Eurocode 3), or handbooks; identify the fatigue limit S_e (endurance limit for steels, typically ~0.5 S_u for S_u < 1400 MPa; aluminum alloys have no true endurance limit)
3. **Apply correction factors to the endurance limit** — S_e' = S_e × k_a (surface) × k_b (size) × k_c (loading) × k_d (temperature) × k_e (reliability) × k_f (miscellaneous)
4. **Account for mean stress** — use Goodman (conservative, linear: S_a/S_e + S_m/S_u = 1), Gerber (parabolic, less conservative), or Soderberg (safest, uses S_y) diagrams
5. **Determine the fatigue life** — from the corrected S-N curve, read N_f at the applied S_a; if S_a < S_e, the component has infinite life (for ferrous metals)
6. **Apply a factor of safety** — on stress (n = S_e/S_a at infinite life) or on life (ratio of predicted to required cycles)
7. **Consider notch effects** — use the fatigue stress concentration factor K_f = 1 + q(K_t − 1), where K_t is the elastic stress concentration factor and q is the notch sensitivity
8. **Report** — fatigue life, factor of safety, critical location, and dominant stress component

### Common LLM Pitfalls
- Assuming aluminum alloys have an endurance limit (they do not — fatigue strength must be quoted at a specific cycle count, typically 10⁷ or 5×10⁸)
- Applying S-N data from polished specimens without correction factors for real-world conditions
- Ignoring mean stress effects (compressive mean stress extends life; tensile mean stress reduces it)
- Confusing K_t (elastic stress concentration) with K_f (fatigue stress concentration) — K_f ≤ K_t due to notch sensitivity

---

## Protocol: Miner's Rule for Variable Amplitude Loading

### When to Use
Estimating fatigue life under variable-amplitude or spectrum loading where stress amplitude varies over time.

### Steps
1. **Decompose the load history** — use rainflow counting to extract individual cycles with amplitudes S_ai and mean stresses S_mi from the irregular load signal
2. **For each stress level**: determine the number of applied cycles n_i and the fatigue life N_i from the S-N curve (with mean stress correction)
3. **Compute the cumulative damage** — D = Σ (n_i / N_i); according to Miner's rule, failure occurs when D = 1
4. **Apply a critical damage sum** — in practice, D_crit = 0.7–2.0 depending on the application and load sequence; D_crit = 1 is the nominal assumption, but conservative design uses D_crit < 1 (e.g., 0.7 for welded joints)
5. **Check for sequence effects** — Miner's rule ignores load sequence (high-low vs low-high); high-low loading typically produces shorter life than predicted (overloads create beneficial residual stresses, but load-level interaction is complex)
6. **For below-endurance-limit cycles**: decide whether to include them. Some codes (Eurocode 3, Haibach extension) assign finite life to cycles below S_e at a reduced slope; others truncate. This choice significantly affects the life prediction
7. **Apply a factor of safety** — use D_allowable = D_crit / safety factor; typical safety factors 2–5 on life depending on consequence of failure
8. **Report** — total damage fraction, predicted life, rainflow histogram, and sensitivity to the damage accumulation rule

### Common LLM Pitfalls
- Ignoring cycles below the endurance limit in a variable-amplitude spectrum (they contribute to damage, especially after higher-amplitude cycles have initiated cracks)
- Treating Miner's rule as exact (it is a simplification; real damage accumulation depends on load sequence, material, and failure mode)
- Not using rainflow counting for cycle extraction (simple range counting or level crossing underestimates or overestimates damage)
- Applying Miner's rule to crack propagation problems (it is a stress-life method; use Paris' law for crack growth)

---

## Protocol: Linear Elastic Fracture Mechanics (LEFM)

### When to Use
Analyzing crack growth and fracture in materials where the plastic zone at the crack tip is small relative to the crack length and component dimensions.

### Steps
1. **Identify the crack geometry** — through crack, edge crack, surface (semi-elliptical) crack, embedded crack; and the loading mode (Mode I: opening, Mode II: sliding, Mode III: tearing)
2. **Compute the stress intensity factor** — K_I = Yσ√(πa), where Y is the geometry correction factor (handbook solutions: Tada, Paris, and Irwin; or numerical from FEA), σ is the applied stress, a is the crack length
3. **Compare to fracture toughness** — if K_I ≥ K_Ic (plane strain fracture toughness), unstable fracture occurs. K_Ic is a material property obtained from ASTM E399 testing
4. **Check plane strain conditions** — specimen thickness B ≥ 2.5(K_Ic/σ_y)²; if not satisfied, the measured toughness K_c > K_Ic (less conservative)
5. **For sub-critical crack growth (fatigue)**: apply Paris' law da/dN = C(ΔK)^m, where ΔK = K_max − K_min, C and m are material constants
6. **Integrate Paris' law** — from initial crack a_i (from inspection or assumed) to critical crack a_c (where K_max = K_Ic): N = ∫ da / [C(ΔK)^m]. This gives the remaining fatigue life
7. **Set inspection intervals** — based on the crack growth rate, set inspection intervals so that a crack can be detected and repaired before reaching a_c (damage tolerance philosophy)
8. **Check for crack closure** — at low R ratios, crack closure reduces the effective ΔK; use effective stress intensity range ΔK_eff = K_max − K_op (opening stress intensity)

### Common LLM Pitfalls
- Using LEFM when the plastic zone is large relative to the crack (need elastic-plastic fracture mechanics — J-integral, CTOD)
- Applying plane strain K_Ic to thin sections where plane stress conditions apply (K_c is higher, but failure may still occur)
- Integrating Paris' law with a constant Y factor when Y varies with crack length (Y must be updated at each integration step)
- Ignoring the stress intensity factor threshold ΔK_th — below this, cracks do not propagate

---

## Protocol: Damage Tolerance Assessment

### When to Use
Ensuring structural integrity in the presence of known or assumed flaws — standard practice in aerospace, nuclear, and critical infrastructure.

### Steps
1. **Define the initial flaw** — assume the largest flaw that could escape detection by the applicable NDE (non-destructive examination) method; typical assumptions: 1.27 mm (0.05 in) for eddy current, 6.35 mm (0.25 in) for visual inspection
2. **Characterize the loading spectrum** — service loads, spectrum truncation level, and environmental conditions (temperature, corrosive media)
3. **Compute the critical crack size** — a_c where K_max = K_Ic (or K_c for non-plane-strain conditions), considering all loading conditions including limit loads
4. **Predict crack growth life** — integrate da/dN = f(ΔK, R, environment) from a_initial to a_critical; use cycle-by-cycle integration for spectrum loading
5. **Establish the inspection program** — inspection interval ≤ crack growth life / safety factor (typically SF = 2 for single load path, SF = 3 for continuing damage)
6. **Consider multiple-site damage** — widespread fatigue damage (MSD) can cause link-up of adjacent cracks, reducing residual strength below that predicted for a single crack
7. **Account for environmental effects** — stress corrosion cracking (SCC) thresholds K_ISCC, corrosion fatigue (accelerated da/dN in aggressive environments), hydrogen embrittlement
8. **Document and maintain** — record all inspections, findings, repairs; update the damage tolerance analysis if the structure is modified or loading changes

### Common LLM Pitfalls
- Setting the initial flaw size too small (must be based on the NDE detection capability, not the expected flaw size)
- Ignoring environmental effects on crack growth rate (corrosion fatigue can increase da/dN by 10–100×)
- Applying damage tolerance without considering multiple-site damage in aging structures
- Confusing safe-life (retirement at predicted life with scatter factor) with damage tolerance (inspection-based continued service)
