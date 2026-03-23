# Thermal Analysis Protocols

> Step-by-step methodology guides for heat transfer and thermal system analysis.

## Protocol: Conduction Analysis

### When to Use
Analyzing steady-state or transient heat conduction through solid materials.

### Steps
1. **Identify the geometry** — plane wall, cylinder, sphere, or complex geometry requiring numerical methods
2. **Determine the regime** — steady-state (∂T/∂t = 0) or transient (temperature changes with time)
3. **For steady-state 1D conduction**: apply Fourier's law q = −kA(dT/dx); for composite walls, use the thermal resistance analogy R = L/(kA) in series/parallel
4. **Compute the overall heat transfer coefficient** — U = 1/ΣR, including convective resistances at surfaces: R_conv = 1/(hA)
5. **For transient problems**: compute the Biot number Bi = hL_c/k (where L_c = V/A_s); if Bi < 0.1, use lumped capacitance method (T(t) = T_∞ + (T_i − T_∞)exp(−t/τ), τ = ρVc_p/(hA_s))
6. **If Bi ≥ 0.1**: use exact solutions (Heisler charts, series solutions) or finite difference/element methods
7. **Include contact resistance** if interfaces between materials exist — R_contact from empirical data or standards
8. **Verify energy balance** — heat in − heat out + heat generated = heat stored; check units (W, not W/m²)

### Common LLM Pitfalls
- Applying lumped capacitance when Bi > 0.1 (spatial temperature gradients are significant)
- Confusing heat flux q'' (W/m²) with heat transfer rate q (W)
- Forgetting thermal contact resistance between bonded or pressed surfaces
- Using thermal conductivity k at the wrong temperature (k is temperature-dependent for many materials)

---

## Protocol: Convection Analysis

### When to Use
Analyzing heat transfer between a surface and a moving fluid — forced or natural convection.

### Steps
1. **Classify the convection type** — forced (external flow, internal flow) or natural (buoyancy-driven); determine if the flow is laminar or turbulent
2. **Compute the Reynolds number** Re = ρVL/μ (or VL/ν) to determine flow regime; critical Re depends on geometry (pipe: ~2300, flat plate: ~5×10⁵)
3. **Select the appropriate correlation** for the Nusselt number Nu = hL/k_f:
   - **Forced, external flat plate**: Nu = 0.664 Re^{1/2} Pr^{1/3} (laminar); Nu = 0.037 Re^{4/5} Pr^{1/3} (turbulent)
   - **Forced, internal pipe**: Nu = 3.66 (laminar, constant T_s); Dittus-Boelter Nu = 0.023 Re^{4/5} Pr^n (turbulent, n=0.4 heating, 0.3 cooling)
   - **Natural convection**: Nu = C(Gr·Pr)^n = C·Ra^n, where Ra = gβΔTL³/να, with C and n from geometry tables
4. **Evaluate fluid properties** at the film temperature T_f = (T_s + T_∞)/2
5. **Compute h** from Nu = hL/k_f, then q = hA(T_s − T_∞)
6. **For mixed convection** (both forced and natural significant): check Gr/Re² — if ~1, both matter; combine using (Nu_forced^n ± Nu_natural^n)^{1/n}
7. **Account for entrance effects** in internal flow — heat transfer coefficients are higher near the inlet; use average Nu over the pipe length
8. **Validate** — compare computed h values to published ranges for the fluid and geometry

### Common LLM Pitfalls
- Using the wrong characteristic length (diameter for pipes, length for plates, specific definitions for each correlation)
- Applying turbulent correlations to laminar flow or vice versa
- Evaluating fluid properties at the surface temperature instead of the film temperature
- Ignoring entrance effects in short pipes (where developing flow dominates)

---

## Protocol: Radiation Heat Transfer

### When to Use
Analyzing heat exchange by electromagnetic radiation between surfaces, especially at high temperatures.

### Steps
1. **Determine surface properties** — emissivity ε, absorptivity α, reflectivity ρ, transmissivity τ; for gray bodies ε = α (Kirchhoff's law)
2. **Compute view factors** — F_{ij} = fraction of radiation leaving surface i intercepted by surface j; verify the summation rule (ΣF_{ij} = 1) and reciprocity rule (A_i F_{ij} = A_j F_{ji})
3. **For simple geometries**: look up view factors from tables/charts (Howell catalog); for complex geometries, use the crossed-string method (2D), contour integration, or Monte Carlo ray tracing
4. **Set up the radiosity equations** — for each surface: J_i = ε_i σT_i⁴ + (1−ε_i) Σ F_{ij} J_j, where J is radiosity (total radiation leaving the surface)
5. **Solve the radiosity system** — linear system of N equations for N surfaces; then compute net heat transfer: q_i = A_i ε_i/(1−ε_i) × (σT_i⁴ − J_i)
6. **For the resistance network method** (two surfaces): q₁₂ = σ(T₁⁴ − T₂⁴) / [(1−ε₁)/(ε₁A₁) + 1/(A₁F₁₂) + (1−ε₂)/(ε₂A₂)]
7. **Include participating media** if gas radiation is significant (CO₂, H₂O in combustion) — use mean beam length and gas emissivity charts
8. **Combine with conduction/convection** — radiation often acts in parallel with convection at the surface: q_total = q_conv + q_rad

### Common LLM Pitfalls
- Forgetting the T⁴ dependence (radiation is significant at high temperatures; often negligible below ~200°C for engineering surfaces)
- Violating view factor algebra (summation or reciprocity rules)
- Assuming ε = 1 (blackbody) without justification — real surfaces have ε < 1 and it is wavelength-dependent
- Ignoring participating media in combustion or furnace applications

---

## Protocol: HVAC Load Calculation

### When to Use
Estimating heating and cooling loads for building thermal design and equipment sizing.

### Steps
1. **Gather design conditions** — outdoor design temperatures (ASHRAE 99.6% heating, 0.4% cooling), indoor setpoints, solar data, building orientation
2. **Compute the building envelope loads** — conduction through walls, roof, floor, windows using U-values and temperature differences; for cooling, use CLTD (Cooling Load Temperature Difference) or RTS (Radiant Time Series) method
3. **Compute solar gains** — through windows: q_solar = A × SHGC × solar irradiance × shading coefficient; through opaque surfaces: use sol-air temperature
4. **Compute internal gains** — people (sensible ~75W, latent ~55W per person), lighting (W/m²), equipment (W/m²), and their radiant/convective splits
5. **Compute infiltration/ventilation loads** — q_sensible = ṁc_p(T_out − T_in), q_latent = ṁh_fg(ω_out − ω_in); ventilation rates from ASHRAE 62.1
6. **Sum the loads** — total cooling = envelope + solar + internal + ventilation; apply diversity factors (not all loads peak simultaneously)
7. **Size the equipment** — apply a safety factor (10–15%); select equipment capacity ≥ peak load; check part-load performance
8. **Perform energy simulation** — 8760-hour simulation (EnergyPlus, eQUEST) for annual energy use, not just peak loads

### Common LLM Pitfalls
- Using peak individual loads without diversity factors (overestimates total peak by 10–30%)
- Ignoring thermal mass effects in cooling load calculations (instantaneous heat gain ≠ cooling load)
- Confusing heating load calculation (steady-state, no solar or internal gains credit) with cooling load calculation (dynamic, must include solar and internal gains)
- Not accounting for latent loads in humid climates (can be 30–40% of total cooling load)
