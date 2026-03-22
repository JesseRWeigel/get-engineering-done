# Get Engineering Done

> An AI copilot for autonomous engineering analysis — from problem specification to verified design to technical publication.

**Inspired by [Get Physics Done](https://github.com/psi-oss/get-physics-done)** — the open-source AI copilot that autonomously conducts physics research. Get Engineering Done adapts GPD's architecture for structural, thermal, and mechanical engineering analysis and design.

## Vision

Engineering analysis shares deep roots with physics — dimensional analysis, conservation laws, and boundary conditions are foundational to both. But engineering adds safety factors, code compliance, material property databases, and design standards that must be tracked rigorously across an analysis.

Get Engineering Done wraps LLM capabilities in a verification-first framework that:
- **Locks design parameters** across phases (unit system, material properties, safety factors, code editions, loading conditions)
- **Verifies engineering consistency** — dimensional analysis, equilibrium checks, energy conservation, code compliance
- **Decomposes analysis** into phases: problem definition → loading analysis → preliminary design → detailed analysis → optimization → verification → reporting
- **Applies domain standards** — AISC, ACI, Eurocode, ASME, ASCE 7, etc.

## Architecture

Adapted from GPD's three-layer design:

### Layer 1 — Core Library (Python)
State management, phase lifecycle, git operations, convention locks, verification kernel.

### Layer 2 — MCP Servers
- `ged-state` — Project state queries
- `ged-conventions` — Design parameter lock management
- `ged-protocols` — Engineering methodology protocols (structural, thermal, fluid dynamics, FEA)
- `ged-patterns` — Cross-project learned patterns
- `ged-verification` — Engineering consistency and code compliance checks
- `ged-errors` — Known LLM engineering failure modes

### Layer 3 — Agents & Commands
- `ged-planner` — Analysis task decomposition
- `ged-executor` — Primary analysis and computation
- `ged-verifier` — Engineering verification and code compliance
- `ged-researcher` — Standards, material properties, and literature research
- `ged-optimizer` — Design optimization and parametric studies
- `ged-paper-writer` — Technical report and paper generation
- `ged-referee` — Multi-perspective review (structural safety, constructability, cost)

## Convention Lock Fields

1. Unit system (SI, Imperial, mixed with explicit conversions)
2. Material property source (edition and table)
3. Design code and edition (AISC 360-22, ACI 318-19, Eurocode 3, etc.)
4. Loading standard (ASCE 7-22, EN 1991, etc.)
5. Safety factor / load factor method (ASD, LRFD, limit states)
6. Coordinate system and sign convention
7. Analysis method (linear elastic, plastic, nonlinear, dynamic)
8. Mesh refinement criteria (for FEA)
9. Convergence criteria
10. Environmental conditions (seismic zone, wind exposure, snow load)

## Verification Framework

1. **Dimensional analysis** — every term, every equation, units consistent
2. **Equilibrium** — forces and moments balance
3. **Compatibility** — deformations consistent with constraints
4. **Energy conservation** — work-energy balance
5. **Boundary conditions** — correctly applied, physically meaningful
6. **Code compliance** — design satisfies applicable code provisions
7. **Safety factors** — adequate margins, demand/capacity ratios checked
8. **Convergence** — FEA/numerical solutions converged (mesh sensitivity, iteration convergence)
9. **Limiting cases** — known analytical solutions matched
10. **Material limits** — stresses within allowable, deflections within serviceability limits
11. **Stability** — buckling, overturning, sliding checked
12. **Sensitivity** — results stable under parameter variation

## Status

**Early development** — Building core infrastructure. Contributions welcome!

## Relationship to GPD

Dimensional analysis, conservation laws, and limiting case verification transfer directly from GPD's physics verification framework. Engineering adds code compliance and safety factor verification on top.

We plan to showcase this in the [GPD Discussion Show & Tell](https://github.com/psi-oss/get-physics-done/discussions) once operational.

## Getting Started

```bash
# Coming soon
npx get-engineering-done
```

## Contributing

We're looking for contributors with:
- Structural, mechanical, or civil engineering experience
- FEA and computational engineering background
- Knowledge of design codes (AISC, ACI, Eurocode, ASME)
- Familiarity with GPD's architecture

See the [Issues](../../issues) for specific tasks.

## License

MIT
