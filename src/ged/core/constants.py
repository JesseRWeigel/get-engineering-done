"""Single source of truth for all directory/file names and environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


# -- Environment Variables --------------------------------------------------

ENV_GED_HOME = "GED_HOME"
ENV_GED_PROJECT = "GED_PROJECT"
ENV_GED_INSTALL_DIR = "GED_INSTALL_DIR"
ENV_GED_DEBUG = "GED_DEBUG"
ENV_GED_AUTONOMY = "GED_AUTONOMY"

# -- File Names -------------------------------------------------------------

STATE_MD = "STATE.md"
STATE_JSON = "state.json"
STATE_WRITE_INTENT = ".state-write-intent"
ROADMAP_MD = "ROADMAP.md"
CONFIG_JSON = "config.json"
CONVENTIONS_JSON = "conventions.json"

PLAN_PREFIX = "PLAN"
SUMMARY_PREFIX = "SUMMARY"
RESEARCH_MD = "RESEARCH.md"
RESEARCH_DIGEST_MD = "RESEARCH-DIGEST.md"
CONTINUE_HERE_MD = ".continue-here.md"

# -- Directory Names --------------------------------------------------------

GED_DIR = ".ged"
OBSERVABILITY_DIR = "observability"
SESSIONS_DIR = "sessions"
TRACES_DIR = "traces"
KNOWLEDGE_DIR = "knowledge"
REPORTS_DIR = "reports"
SCRATCH_DIR = ".scratch"

# -- Git --------------------------------------------------------------------

CHECKPOINT_TAG_PREFIX = "ged-checkpoint"
COMMIT_PREFIX = "[ged]"

# -- Autonomy Modes ---------------------------------------------------------

AUTONOMY_SUPERVISED = "supervised"
AUTONOMY_BALANCED = "balanced"
AUTONOMY_YOLO = "yolo"
VALID_AUTONOMY_MODES = {AUTONOMY_SUPERVISED, AUTONOMY_BALANCED, AUTONOMY_YOLO}

# -- Analysis Modes ---------------------------------------------------------

ANALYSIS_PRELIMINARY = "preliminary"
ANALYSIS_DETAILED = "detailed"
ANALYSIS_OPTIMIZATION = "optimization"
ANALYSIS_ADAPTIVE = "adaptive"
VALID_ANALYSIS_MODES = {ANALYSIS_PRELIMINARY, ANALYSIS_DETAILED, ANALYSIS_OPTIMIZATION, ANALYSIS_ADAPTIVE}

# -- Model Tiers ------------------------------------------------------------

TIER_1 = "tier-1"  # Highest capability
TIER_2 = "tier-2"  # Balanced
TIER_3 = "tier-3"  # Fastest

# -- Verification Severity --------------------------------------------------

SEVERITY_CRITICAL = "CRITICAL"  # Blocks all downstream work
SEVERITY_MAJOR = "MAJOR"        # Must resolve before final design
SEVERITY_MINOR = "MINOR"        # Must resolve before reporting
SEVERITY_NOTE = "NOTE"          # Informational

# -- Convention Lock Fields (Engineering) -----------------------------------

CONVENTION_FIELDS = [
    "unit_system",                # SI, Imperial, mixed; base units for force/length/time
    "material_source",            # Material property database/standard (AISC, Eurocode, manufacturer data)
    "design_code",                # Governing design code and edition (AISC 360-22, Eurocode 3, ACI 318-19)
    "loading_standard",           # Load standard and edition (ASCE 7-22, EN 1991, IBC 2021)
    "safety_factors",             # LRFD vs ASD, partial safety factors, load combinations
    "coordinate_system",          # Global coordinate system, sign conventions, axis orientation
    "analysis_method",            # Linear elastic, plastic, second-order, direct analysis
    "mesh_criteria",              # Element types, mesh density, aspect ratio limits, refinement zones
    "convergence_criteria",       # Force/displacement/energy tolerances, iteration limits
    "environmental_conditions",   # Temperature range, exposure category, seismic site class, wind exposure
]

# -- Verification Checks ---------------------------------------------------

VERIFICATION_CHECKS = [
    "dimensional_analysis",       # Units consistent throughout all calculations
    "equilibrium",                # Sum of forces and moments equals zero at every node/section
    "compatibility",              # Deformations are consistent with constraints and connections
    "energy_conservation",        # External work equals internal strain energy
    "boundary_conditions",        # Support conditions correctly modeled and applied
    "code_compliance",            # Design meets all applicable code provisions
    "safety_factors",             # Required safety margins maintained for all limit states
    "convergence",                # Numerical solutions converged (mesh, iteration, time-step)
    "limiting_cases",             # Results match known analytical solutions at limits
    "material_limits",            # Stresses/strains within material capacity envelopes
    "stability",                  # Buckling, overturning, sliding, and P-delta effects checked
    "sensitivity",                # Results not overly sensitive to modeling assumptions
]


@dataclass(frozen=True)
class ProjectLayout:
    """Resolved paths for a GED project."""

    root: Path

    @property
    def ged_dir(self) -> Path:
        return self.root / GED_DIR

    @property
    def state_md(self) -> Path:
        return self.ged_dir / STATE_MD

    @property
    def state_json(self) -> Path:
        return self.ged_dir / STATE_JSON

    @property
    def state_write_intent(self) -> Path:
        return self.ged_dir / STATE_WRITE_INTENT

    @property
    def roadmap_md(self) -> Path:
        return self.ged_dir / ROADMAP_MD

    @property
    def config_json(self) -> Path:
        return self.ged_dir / CONFIG_JSON

    @property
    def conventions_json(self) -> Path:
        return self.ged_dir / CONVENTIONS_JSON

    @property
    def observability_dir(self) -> Path:
        return self.ged_dir / OBSERVABILITY_DIR

    @property
    def sessions_dir(self) -> Path:
        return self.observability_dir / SESSIONS_DIR

    @property
    def traces_dir(self) -> Path:
        return self.ged_dir / TRACES_DIR

    @property
    def knowledge_dir(self) -> Path:
        return self.root / KNOWLEDGE_DIR

    @property
    def reports_dir(self) -> Path:
        return self.root / REPORTS_DIR

    @property
    def scratch_dir(self) -> Path:
        return self.root / SCRATCH_DIR

    @property
    def continue_here(self) -> Path:
        return self.ged_dir / CONTINUE_HERE_MD

    def phase_dir(self, phase: str) -> Path:
        return self.root / f"phase-{phase}"

    def plan_path(self, phase: str, plan_number: str) -> Path:
        return self.phase_dir(phase) / f"{PLAN_PREFIX}-{plan_number}.md"

    def summary_path(self, phase: str, plan_number: str) -> Path:
        return self.phase_dir(phase) / f"{SUMMARY_PREFIX}-{plan_number}.md"

    def ensure_dirs(self) -> None:
        """Create all required directories."""
        for d in [
            self.ged_dir,
            self.observability_dir,
            self.sessions_dir,
            self.traces_dir,
            self.knowledge_dir,
            self.scratch_dir,
        ]:
            d.mkdir(parents=True, exist_ok=True)


def find_project_root(start: Path | None = None) -> Path:
    """Walk up from start (or cwd) looking for .ged/ directory."""
    current = start or Path.cwd()
    while current != current.parent:
        if (current / GED_DIR).is_dir():
            return current
        current = current.parent
    raise FileNotFoundError(
        f"No {GED_DIR}/ directory found. Run 'ged init' to create a project."
    )


def get_layout(start: Path | None = None) -> ProjectLayout:
    """Get the project layout, finding the root automatically."""
    env_project = os.environ.get(ENV_GED_PROJECT)
    if env_project:
        return ProjectLayout(root=Path(env_project))
    return ProjectLayout(root=find_project_root(start))
