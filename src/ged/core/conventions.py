"""Convention lock management for engineering design consistency.

Ensures design parameters don't drift across phases of an engineering project.
Adapted from GPD's conventions.py for engineering.
"""

from __future__ import annotations

from typing import Any

from .constants import CONVENTION_FIELDS
from .state import StateEngine, ConventionLock


# -- Convention Field Descriptions -------------------------------------------

CONVENTION_DESCRIPTIONS: dict[str, str] = {
    "unit_system": (
        "System of units for all calculations. SI (kN, m, MPa), Imperial "
        "(kip, ft, ksi), or mixed. Must specify base units for force, length, "
        "time, and temperature. All intermediate calculations must use these units."
    ),
    "material_source": (
        "Source of material properties: AISC Steel Construction Manual (edition), "
        "Eurocode material standards, ACI 318 concrete properties, manufacturer "
        "test certificates, or project-specific test data. Must cite specific "
        "tables/sections for property values."
    ),
    "design_code": (
        "Governing design code and edition. Examples: AISC 360-22 (steel), "
        "ACI 318-19 (concrete), Eurocode 3 EN 1993-1-1:2005+A1:2014 (steel), "
        "AASHTO LRFD Bridge Design Specifications 9th Ed. Must lock the exact "
        "edition — code provisions change between editions."
    ),
    "loading_standard": (
        "Load determination standard and edition: ASCE 7-22 (US), EN 1991 (Europe), "
        "IBC 2021, or project-specific loading criteria. Defines how dead, live, "
        "wind, seismic, snow, and other loads are determined and combined."
    ),
    "safety_factors": (
        "Design philosophy and load/resistance factors. LRFD (Load and Resistance "
        "Factor Design) vs ASD (Allowable Stress Design). Specific load combination "
        "factors (e.g., 1.2D + 1.6L, 1.0D + 1.0E + 0.2S). Resistance factors "
        "(phi factors) for each limit state."
    ),
    "coordinate_system": (
        "Global coordinate system orientation: X = East, Y = North, Z = Up "
        "(or project-specific). Sign convention for forces (tension positive or "
        "compression positive). Moment sign convention (right-hand rule). "
        "Local member axes orientation."
    ),
    "analysis_method": (
        "Structural analysis approach: first-order elastic, second-order elastic "
        "(P-delta), direct analysis method (DAM), plastic analysis, or advanced "
        "nonlinear. For FEA: static, dynamic, modal, buckling, or time-history. "
        "Must specify if geometric and/or material nonlinearity is included."
    ),
    "mesh_criteria": (
        "FEA mesh specifications: element types (shell, solid, beam), target "
        "element size, maximum aspect ratio, minimum angle, refinement zones "
        "(connections, openings, stress concentrations). Mesh convergence "
        "criteria (% change in peak stress between refinements)."
    ),
    "convergence_criteria": (
        "Numerical convergence tolerances: force residual (e.g., 0.1%), "
        "displacement increment (e.g., 0.01%), energy norm (e.g., 0.001%). "
        "Maximum iterations per load step. Line search parameters. "
        "Arc-length method parameters if applicable."
    ),
    "environmental_conditions": (
        "Site-specific environmental parameters: seismic site class (A-F), "
        "seismic design category, wind exposure category (B/C/D), snow ground "
        "load, temperature range, corrosion exposure class, fire rating "
        "requirements. Must cite source (site investigation, code maps, etc.)."
    ),
}

# -- Convention Validation ---------------------------------------------------

# Common valid values for quick validation
CONVENTION_EXAMPLES: dict[str, list[str]] = {
    "unit_system": [
        "SI: kN, m, MPa, degrees C",
        "SI: N, mm, MPa, degrees C",
        "Imperial: kip, ft, ksi, degrees F",
        "Imperial: lb, in, psi, degrees F",
    ],
    "design_code": [
        "AISC 360-22 (Specification for Structural Steel Buildings)",
        "ACI 318-19 (Building Code Requirements for Structural Concrete)",
        "Eurocode 3: EN 1993-1-1:2005+A1:2014",
        "AASHTO LRFD Bridge Design Specifications, 9th Edition, 2020",
    ],
    "safety_factors": [
        "LRFD per AISC 360-22 Chapter B",
        "ASD per AISC 360-22 Chapter B",
        "Eurocode partial safety factors per EN 1990",
        "LRFD per AASHTO with HL-93 loading",
    ],
    "coordinate_system": [
        "Right-hand rule: X=East, Y=North, Z=Up; tension positive",
        "Right-hand rule: X=longitudinal, Y=transverse, Z=vertical; compression positive",
    ],
    "analysis_method": [
        "Second-order elastic (P-delta) per AISC Direct Analysis Method",
        "First-order elastic with amplification factors",
        "Linear elastic FEA with geometric stiffness",
        "Nonlinear static pushover (ASCE 41-17)",
    ],
}


def get_field_description(field: str) -> str:
    """Get the description for a convention field."""
    return CONVENTION_DESCRIPTIONS.get(field, f"Convention field: {field}")


def get_field_examples(field: str) -> list[str]:
    """Get example values for a convention field."""
    return CONVENTION_EXAMPLES.get(field, [])


def list_all_fields() -> list[dict[str, Any]]:
    """List all convention fields with descriptions and examples."""
    return [
        {
            "field": f,
            "description": get_field_description(f),
            "examples": get_field_examples(f),
        }
        for f in CONVENTION_FIELDS
    ]


def check_conventions(engine: StateEngine) -> dict[str, Any]:
    """Check which conventions are locked and which are missing.

    Returns a report dict with locked, unlocked, and coverage stats.
    """
    state = engine.load()
    locked = {}
    unlocked = []

    for field in CONVENTION_FIELDS:
        if field in state.conventions:
            locked[field] = {
                "value": state.conventions[field].value,
                "locked_by": state.conventions[field].locked_by,
                "rationale": state.conventions[field].rationale,
            }
        else:
            unlocked.append(field)

    return {
        "locked": locked,
        "unlocked": unlocked,
        "coverage": f"{len(locked)}/{len(CONVENTION_FIELDS)}",
        "coverage_pct": round(100 * len(locked) / len(CONVENTION_FIELDS), 1)
        if CONVENTION_FIELDS
        else 100.0,
    }


def diff_conventions(
    engine: StateEngine,
    proposed: dict[str, str],
) -> dict[str, Any]:
    """Compare proposed convention values against current locks.

    Returns conflicts, new fields, and matching fields.
    """
    state = engine.load()
    conflicts = {}
    new_fields = {}
    matching = {}

    for field, proposed_value in proposed.items():
        if field in state.conventions:
            current = state.conventions[field].value
            if current != proposed_value:
                conflicts[field] = {
                    "current": current,
                    "proposed": proposed_value,
                }
            else:
                matching[field] = current
        else:
            new_fields[field] = proposed_value

    return {
        "conflicts": conflicts,
        "new_fields": new_fields,
        "matching": matching,
        "has_conflicts": bool(conflicts),
    }
