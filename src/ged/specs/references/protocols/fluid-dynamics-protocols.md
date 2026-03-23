# Fluid Dynamics Protocols

> Step-by-step methodology guides for fluid mechanics analysis and computation.

## Protocol: Pipe Flow Analysis

### When to Use
Analyzing pressure drop, flow rate, and velocity distribution in closed conduit systems.

### Steps
1. **Classify the flow** — compute Re = ρVD/μ; laminar (Re < 2300), transitional (2300–4000), turbulent (Re > 4000) for circular pipes
2. **Determine the friction factor**:
   - **Laminar**: f = 64/Re (Darcy-Weisbach)
   - **Turbulent smooth**: Blasius f = 0.316 Re^{−1/4} (Re < 10⁵) or Colebrook-White equation (implicit, use Moody chart or Swamee-Jain explicit approximation)
   - **Turbulent rough**: Colebrook-White 1/√f = −2 log₁₀(ε/(3.7D) + 2.51/(Re√f))
3. **Compute head loss** — major losses: h_f = f(L/D)(V²/2g) (Darcy-Weisbach); minor losses: h_m = K(V²/2g) for each fitting, valve, bend
4. **Apply the energy equation** — P₁/(ρg) + V₁²/(2g) + z₁ = P₂/(ρg) + V₂²/(2g) + z₂ + h_f + h_m (+ pump head − turbine head if applicable)
5. **For pipe networks**: apply Hardy-Cross method (iterative correction) or solve simultaneously using Newton-Raphson; ensure continuity (Σ flows at each node = 0) and energy conservation (Σ head losses around each loop = 0)
6. **Check velocity limits** — typical design: 1–3 m/s for water, 15–30 m/s for air; too high causes erosion, too low causes sedimentation
7. **Account for non-circular cross-sections** — use hydraulic diameter D_h = 4A/P (A = cross-sectional area, P = wetted perimeter)
8. **Validate** — compare pressure drop to manufacturer data for fittings; check against design standards

### Common LLM Pitfalls
- Using the Fanning friction factor instead of the Darcy friction factor (differ by a factor of 4)
- Ignoring minor losses in short pipe systems with many fittings (minor losses can dominate)
- Applying the Bernoulli equation to viscous flow without including head loss terms
- Forgetting to iterate the Colebrook-White equation (it is implicit in f)

---

## Protocol: Open Channel Flow

### When to Use
Analyzing flow in channels with a free surface — rivers, canals, drainage systems, spillways.

### Steps
1. **Classify the flow** — compute the Froude number Fr = V/√(gD_h), where D_h = A/T (A = flow area, T = top width); subcritical (Fr < 1), critical (Fr = 1), supercritical (Fr > 1)
2. **Compute normal depth** — for uniform flow, use Manning's equation: Q = (1/n)AR^{2/3}S^{1/2} (SI), where n = Manning's roughness, R = A/P (hydraulic radius), S = bed slope. Solve iteratively for depth
3. **Compute critical depth** — for a given Q, critical depth occurs when specific energy is minimized: Q²T/(gA³) = 1
4. **Classify the channel slope** — mild (y_n > y_c), steep (y_n < y_c), critical (y_n = y_c); determines the gradually varied flow profiles (M1, M2, M3, S1, S2, S3)
5. **For gradually varied flow**: solve the GVF equation dy/dx = (S₀ − S_f)/(1 − Fr²) using standard step or direct step methods; S_f from Manning's equation at each section
6. **Locate hydraulic jumps** — a jump occurs when flow transitions from supercritical to subcritical; the sequent depth ratio is y₂/y₁ = ½(−1 + √(1 + 8Fr₁²))
7. **Design the channel** — most efficient cross-section minimizes P for a given A (semicircle is ideal; trapezoidal with side slopes at 60° is practical)
8. **Verify freeboard** — add 15–30% above design depth to prevent overtopping

### Common LLM Pitfalls
- Confusing hydraulic radius R = A/P with hydraulic depth D_h = A/T (different definitions used in different contexts)
- Using Manning's equation for non-uniform flow without accounting for spatially varying depth
- Forgetting that a hydraulic jump is irreversible and involves energy loss (not just a momentum balance)
- Not checking whether the slope is mild or steep before selecting the correct water surface profile type

---

## Protocol: Bernoulli Equation Application

### When to Use
Analyzing inviscid, incompressible, steady flow along a streamline for preliminary engineering estimates.

### Steps
1. **Verify the assumptions** — steady flow, incompressible fluid, inviscid (or losses accounted separately), along a single streamline
2. **Write the equation** — P₁ + ½ρV₁² + ρgz₁ = P₂ + ½ρV₂² + ρgz₂ (energy form per unit volume)
3. **Identify known and unknown quantities** — typically know three of {P, V, z} at each point; apply continuity A₁V₁ = A₂V₂ to relate velocities
4. **Apply to common devices**:
   - **Venturi/orifice meter**: ΔP = ½ρ(V₂² − V₁²); solve for Q with discharge coefficient C_d
   - **Pitot tube**: V = √(2ΔP/ρ), where ΔP = stagnation pressure − static pressure
   - **Tank draining**: V_exit = √(2gh) (Torricelli's theorem); apply C_c (contraction coefficient) and C_v (velocity coefficient)
5. **Account for real-fluid effects** — add head loss term for viscous effects; apply discharge coefficients (C_d typically 0.60–0.65 for sharp-edged orifice, 0.97–0.99 for Venturi)
6. **Check compressibility** — Bernoulli for incompressible flow is valid when Ma < 0.3; for higher Mach numbers, use compressible flow relations
7. **State limitations** — results are approximate; do not apply across streamlines without additional assumptions (irrotational flow)

### Common LLM Pitfalls
- Applying Bernoulli across streamlines without justifying irrotational flow
- Forgetting to include the elevation term in vertical flow problems
- Using Bernoulli for viscous-dominated flows (e.g., fully developed pipe flow) without adding head loss
- Ignoring compressibility effects at high velocities (Ma > 0.3)

---

## Protocol: CFD Methodology

### When to Use
Setting up, running, and validating computational fluid dynamics simulations.

### Steps
1. **Define the problem** — geometry, boundary conditions, fluid properties, flow regime (laminar/turbulent), steady/transient, compressible/incompressible
2. **Create the mesh** — structured (hexahedral, more accurate per cell) or unstructured (tetrahedral, easier to generate); refine near walls (y⁺ requirements: wall-resolved LES y⁺ < 1, wall-modeled LES/k-ε with wall functions y⁺ = 30–300)
3. **Select the turbulence model** — RANS: k-ε (standard, realizable, RNG), k-ω SST (best general-purpose), Spalart-Allmaras (aerospace); LES (resolved large eddies, modeled small); DNS (all scales resolved, extremely expensive)
4. **Set boundary conditions** — inlet (velocity/mass flow + turbulence intensity ~5%, turbulent length scale), outlet (pressure), walls (no-slip, specified temperature or heat flux), symmetry/periodic where applicable
5. **Choose the solver settings** — pressure-velocity coupling (SIMPLE, PISO), discretization schemes (second-order upwind minimum for convection), convergence criteria (residuals < 10⁻⁴ to 10⁻⁶ depending on the quantity of interest)
6. **Perform a mesh independence study** — run on at least 3 mesh levels (coarse, medium, fine); compute the Grid Convergence Index (GCI) using Richardson extrapolation; the solution should change < 2% between the two finest meshes
7. **Validate against experimental data or analytical solutions** — compare velocity profiles, pressure drops, drag coefficients, heat transfer rates
8. **Post-process and report** — contour plots, streamlines, integrated quantities; report mesh size, turbulence model, convergence metrics, and GCI

### Common LLM Pitfalls
- Skipping the mesh independence study (results may be mesh-dependent and unreliable)
- Using k-ε with wall functions at y⁺ < 5 or y⁺ > 300 (outside the valid range for standard wall functions)
- Applying RANS to inherently unsteady flows (vortex shedding, separation) where LES or URANS is needed
- Reporting CFD results without validation against experimental data or analytical benchmarks
