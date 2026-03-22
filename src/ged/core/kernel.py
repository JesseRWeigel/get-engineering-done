"""Content-addressed verification kernel.

Runs predicates over evidence registries and produces SHA-256 verdicts.
Adapted from GPD's kernel.py for engineering analysis verification.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable

from .constants import VERIFICATION_CHECKS, SEVERITY_CRITICAL, SEVERITY_MAJOR, SEVERITY_MINOR, SEVERITY_NOTE


class Severity(str, Enum):
    CRITICAL = SEVERITY_CRITICAL
    MAJOR = SEVERITY_MAJOR
    MINOR = SEVERITY_MINOR
    NOTE = SEVERITY_NOTE


@dataclass
class CheckResult:
    """Result of a single verification check."""

    check_id: str
    name: str
    status: str  # PASS | FAIL | SKIP | WARN
    severity: Severity
    message: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    suggestions: list[str] = field(default_factory=list)


@dataclass
class Verdict:
    """Complete verification verdict with content-addressed hashes."""

    registry_hash: str
    predicates_hash: str
    verdict_hash: str
    overall: str  # PASS | FAIL | PARTIAL
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    results: dict[str, CheckResult] = field(default_factory=dict)
    summary: str = ""

    @property
    def critical_failures(self) -> list[CheckResult]:
        return [
            r
            for r in self.results.values()
            if r.status == "FAIL" and r.severity == Severity.CRITICAL
        ]

    @property
    def major_failures(self) -> list[CheckResult]:
        return [
            r
            for r in self.results.values()
            if r.status == "FAIL" and r.severity == Severity.MAJOR
        ]

    @property
    def all_failures(self) -> list[CheckResult]:
        return [r for r in self.results.values() if r.status == "FAIL"]

    @property
    def pass_count(self) -> int:
        return sum(1 for r in self.results.values() if r.status == "PASS")

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results.values() if r.status == "FAIL")

    def to_dict(self) -> dict[str, Any]:
        return {
            "registry_hash": self.registry_hash,
            "predicates_hash": self.predicates_hash,
            "verdict_hash": self.verdict_hash,
            "overall": self.overall,
            "timestamp": self.timestamp,
            "summary": self.summary,
            "results": {
                k: {
                    "check_id": v.check_id,
                    "name": v.name,
                    "status": v.status,
                    "severity": v.severity.value,
                    "message": v.message,
                    "evidence": v.evidence,
                    "suggestions": v.suggestions,
                }
                for k, v in self.results.items()
            },
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# -- Predicate Type ---------------------------------------------------------

# A predicate takes an evidence registry and returns a CheckResult
Predicate = Callable[[dict[str, Any]], CheckResult]


# -- Built-in Engineering Predicates ----------------------------------------

def check_dimensional_analysis(evidence: dict[str, Any]) -> CheckResult:
    """Check that units are consistent throughout all calculations."""
    unit_errors = evidence.get("unit_errors", [])
    calculations_checked = evidence.get("calculations_checked", 0)

    if calculations_checked == 0:
        return CheckResult(
            check_id="dimensional_analysis",
            name="Dimensional Analysis",
            status="SKIP",
            severity=Severity.CRITICAL,
            message="No calculations provided for dimensional analysis.",
        )

    if unit_errors:
        return CheckResult(
            check_id="dimensional_analysis",
            name="Dimensional Analysis",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Found {len(unit_errors)} unit inconsistency/ies.",
            evidence={"errors": unit_errors},
            suggestions=[f"Fix unit error: {e}" for e in unit_errors[:5]],
        )

    return CheckResult(
        check_id="dimensional_analysis",
        name="Dimensional Analysis",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"Units consistent across {calculations_checked} calculation(s).",
    )


def check_equilibrium(evidence: dict[str, Any]) -> CheckResult:
    """Check that forces and moments balance at every node/section."""
    equilibrium_checks = evidence.get("equilibrium_checks", [])
    equilibrium_violations = evidence.get("equilibrium_violations", [])

    if not equilibrium_checks:
        return CheckResult(
            check_id="equilibrium",
            name="Equilibrium",
            status="SKIP",
            severity=Severity.CRITICAL,
            message="No equilibrium checks provided.",
        )

    if equilibrium_violations:
        return CheckResult(
            check_id="equilibrium",
            name="Equilibrium",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Equilibrium violated at {len(equilibrium_violations)} location(s).",
            evidence={"violations": equilibrium_violations},
            suggestions=["Re-check reaction calculations and load paths."],
        )

    return CheckResult(
        check_id="equilibrium",
        name="Equilibrium",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"Equilibrium verified at {len(equilibrium_checks)} location(s).",
    )


def check_compatibility(evidence: dict[str, Any]) -> CheckResult:
    """Check that deformations are consistent with constraints and connections."""
    compatibility_checks = evidence.get("compatibility_checks", [])
    compatibility_violations = evidence.get("compatibility_violations", [])

    if not compatibility_checks:
        return CheckResult(
            check_id="compatibility",
            name="Compatibility",
            status="SKIP",
            severity=Severity.CRITICAL,
            message="No compatibility checks provided.",
        )

    if compatibility_violations:
        return CheckResult(
            check_id="compatibility",
            name="Compatibility",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Compatibility violated at {len(compatibility_violations)} location(s).",
            evidence={"violations": compatibility_violations},
            suggestions=["Review connection details and constraint modeling."],
        )

    return CheckResult(
        check_id="compatibility",
        name="Compatibility",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"Compatibility verified at {len(compatibility_checks)} location(s).",
    )


def check_energy_conservation(evidence: dict[str, Any]) -> CheckResult:
    """Check that external work equals internal strain energy."""
    external_work = evidence.get("external_work", None)
    internal_energy = evidence.get("internal_energy", None)
    energy_tolerance = evidence.get("energy_tolerance", 0.01)

    if external_work is None or internal_energy is None:
        return CheckResult(
            check_id="energy_conservation",
            name="Energy Conservation",
            status="SKIP",
            severity=Severity.MAJOR,
            message="Energy balance data not provided.",
        )

    if external_work == 0 and internal_energy == 0:
        return CheckResult(
            check_id="energy_conservation",
            name="Energy Conservation",
            status="PASS",
            severity=Severity.MAJOR,
            message="Zero-load case: both external work and internal energy are zero.",
        )

    ratio = abs(external_work - internal_energy) / max(abs(external_work), abs(internal_energy))
    if ratio > energy_tolerance:
        return CheckResult(
            check_id="energy_conservation",
            name="Energy Conservation",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"Energy imbalance: {ratio:.2%} exceeds tolerance {energy_tolerance:.2%}.",
            evidence={"external_work": external_work, "internal_energy": internal_energy, "ratio": ratio},
            suggestions=["Check for missing loads, incorrect stiffness, or modeling errors."],
        )

    return CheckResult(
        check_id="energy_conservation",
        name="Energy Conservation",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"Energy balance within tolerance: {ratio:.4%} difference.",
    )


def check_boundary_conditions(evidence: dict[str, Any]) -> CheckResult:
    """Check that support conditions are correctly modeled and applied."""
    bc_checks = evidence.get("boundary_condition_checks", [])
    bc_violations = evidence.get("boundary_condition_violations", [])

    if not bc_checks:
        return CheckResult(
            check_id="boundary_conditions",
            name="Boundary Conditions",
            status="SKIP",
            severity=Severity.CRITICAL,
            message="No boundary condition checks provided.",
        )

    if bc_violations:
        return CheckResult(
            check_id="boundary_conditions",
            name="Boundary Conditions",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Found {len(bc_violations)} boundary condition error(s).",
            evidence={"violations": bc_violations},
            suggestions=["Review support conditions against structural drawings."],
        )

    return CheckResult(
        check_id="boundary_conditions",
        name="Boundary Conditions",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(bc_checks)} boundary condition(s) verified.",
    )


def check_code_compliance(evidence: dict[str, Any]) -> CheckResult:
    """Check that design meets all applicable code provisions."""
    code_checks = evidence.get("code_checks", [])
    code_violations = evidence.get("code_violations", [])
    code_edition = evidence.get("code_edition", "")

    if not code_checks:
        return CheckResult(
            check_id="code_compliance",
            name="Code Compliance",
            status="WARN",
            severity=Severity.CRITICAL,
            message="No code compliance checks performed.",
            suggestions=["Identify applicable design code and check all provisions."],
        )

    if code_violations:
        return CheckResult(
            check_id="code_compliance",
            name="Code Compliance",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Design fails {len(code_violations)} code provision(s) per {code_edition}.",
            evidence={"violations": code_violations},
            suggestions=[f"Address violation: {v}" for v in code_violations[:5]],
        )

    return CheckResult(
        check_id="code_compliance",
        name="Code Compliance",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(code_checks)} code check(s) pass per {code_edition}.",
    )


def check_safety_factors(evidence: dict[str, Any]) -> CheckResult:
    """Check that required safety margins are maintained for all limit states."""
    sf_checks = evidence.get("safety_factor_checks", [])
    sf_violations = evidence.get("safety_factor_violations", [])
    design_method = evidence.get("design_method", "LRFD")

    if not sf_checks:
        return CheckResult(
            check_id="safety_factors",
            name="Safety Factors",
            status="WARN",
            severity=Severity.CRITICAL,
            message="No safety factor checks performed.",
            suggestions=[f"Verify all members meet {design_method} requirements."],
        )

    if sf_violations:
        return CheckResult(
            check_id="safety_factors",
            name="Safety Factors",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"{len(sf_violations)} member(s)/section(s) fail safety factor requirements.",
            evidence={"violations": sf_violations},
            suggestions=["Increase member sizes or reduce loads for failing elements."],
        )

    return CheckResult(
        check_id="safety_factors",
        name="Safety Factors",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(sf_checks)} safety factor check(s) pass ({design_method}).",
    )


def check_convergence(evidence: dict[str, Any]) -> CheckResult:
    """Check that numerical solutions have converged."""
    convergence_studies = evidence.get("convergence_studies", [])
    convergence_failures = evidence.get("convergence_failures", [])

    if not convergence_studies:
        return CheckResult(
            check_id="convergence",
            name="Convergence",
            status="SKIP",
            severity=Severity.MAJOR,
            message="No convergence studies provided (may be hand-calculation only).",
        )

    if convergence_failures:
        return CheckResult(
            check_id="convergence",
            name="Convergence",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"{len(convergence_failures)} convergence failure(s) in numerical analysis.",
            evidence={"failures": convergence_failures},
            suggestions=[
                "Refine mesh in regions of high stress gradient.",
                "Check element aspect ratios and distortion.",
                "Increase iteration limit or adjust convergence tolerance.",
            ],
        )

    return CheckResult(
        check_id="convergence",
        name="Convergence",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"All {len(convergence_studies)} convergence study/ies pass.",
    )


def check_limiting_cases(evidence: dict[str, Any]) -> CheckResult:
    """Check results match known analytical solutions at limiting cases."""
    limiting_cases = evidence.get("limiting_cases", [])
    limiting_case_failures = evidence.get("limiting_case_failures", [])

    if not limiting_cases:
        return CheckResult(
            check_id="limiting_cases",
            name="Limiting Cases",
            status="WARN",
            severity=Severity.MAJOR,
            message="No limiting case comparisons performed.",
            suggestions=[
                "Compare with simply-supported beam, cantilever, or other known solutions.",
                "Check that model reduces to textbook results for simple configurations.",
            ],
        )

    if limiting_case_failures:
        return CheckResult(
            check_id="limiting_cases",
            name="Limiting Cases",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"Results disagree with {len(limiting_case_failures)} known analytical solution(s).",
            evidence={"failures": limiting_case_failures},
        )

    return CheckResult(
        check_id="limiting_cases",
        name="Limiting Cases",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"Results match {len(limiting_cases)} known analytical solution(s).",
    )


def check_material_limits(evidence: dict[str, Any]) -> CheckResult:
    """Check that stresses and strains are within material capacity envelopes."""
    material_checks = evidence.get("material_checks", [])
    material_violations = evidence.get("material_violations", [])

    if not material_checks:
        return CheckResult(
            check_id="material_limits",
            name="Material Limits",
            status="WARN",
            severity=Severity.CRITICAL,
            message="No material limit checks performed.",
            suggestions=["Verify stresses against yield, ultimate, and fatigue limits."],
        )

    if material_violations:
        return CheckResult(
            check_id="material_limits",
            name="Material Limits",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"{len(material_violations)} material limit exceedance(s) found.",
            evidence={"violations": material_violations},
            suggestions=["Review material selection or increase member capacity."],
        )

    return CheckResult(
        check_id="material_limits",
        name="Material Limits",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(material_checks)} material check(s) within limits.",
    )


def check_stability(evidence: dict[str, Any]) -> CheckResult:
    """Check buckling, overturning, sliding, and P-delta effects."""
    stability_checks = evidence.get("stability_checks", [])
    stability_violations = evidence.get("stability_violations", [])

    if not stability_checks:
        return CheckResult(
            check_id="stability",
            name="Stability",
            status="WARN",
            severity=Severity.CRITICAL,
            message="No stability checks performed.",
            suggestions=[
                "Check column buckling (Euler and code-based).",
                "Verify lateral-torsional buckling for beams.",
                "Check global stability (overturning, sliding).",
                "Evaluate P-delta effects if applicable.",
            ],
        )

    if stability_violations:
        return CheckResult(
            check_id="stability",
            name="Stability",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"{len(stability_violations)} stability failure(s) found.",
            evidence={"violations": stability_violations},
            suggestions=["Add bracing, increase member sizes, or revise geometry."],
        )

    return CheckResult(
        check_id="stability",
        name="Stability",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(stability_checks)} stability check(s) pass.",
    )


def check_sensitivity(evidence: dict[str, Any]) -> CheckResult:
    """Check that results are not overly sensitive to modeling assumptions."""
    sensitivity_studies = evidence.get("sensitivity_studies", [])
    sensitivity_concerns = evidence.get("sensitivity_concerns", [])

    if not sensitivity_studies:
        return CheckResult(
            check_id="sensitivity",
            name="Sensitivity",
            status="WARN",
            severity=Severity.MINOR,
            message="No sensitivity studies performed.",
            suggestions=[
                "Vary key parameters (material properties, loads, boundary conditions) by +/-10%.",
                "Check if results change significantly with different mesh densities.",
            ],
        )

    if sensitivity_concerns:
        return CheckResult(
            check_id="sensitivity",
            name="Sensitivity",
            status="FAIL",
            severity=Severity.MINOR,
            message=f"Results are sensitive to {len(sensitivity_concerns)} assumption(s).",
            evidence={"concerns": sensitivity_concerns},
            suggestions=["Investigate sensitive parameters and add safety margin or refine model."],
        )

    return CheckResult(
        check_id="sensitivity",
        name="Sensitivity",
        status="PASS",
        severity=Severity.MINOR,
        message=f"All {len(sensitivity_studies)} sensitivity study/ies show robust results.",
    )


# -- Default predicate registry ---------------------------------------------

DEFAULT_PREDICATES: dict[str, Predicate] = {
    "dimensional_analysis": check_dimensional_analysis,
    "equilibrium": check_equilibrium,
    "compatibility": check_compatibility,
    "energy_conservation": check_energy_conservation,
    "boundary_conditions": check_boundary_conditions,
    "code_compliance": check_code_compliance,
    "safety_factors": check_safety_factors,
    "convergence": check_convergence,
    "limiting_cases": check_limiting_cases,
    "material_limits": check_material_limits,
    "stability": check_stability,
    "sensitivity": check_sensitivity,
}


# -- Verification Kernel ----------------------------------------------------

class VerificationKernel:
    """Content-addressed verification kernel.

    Runs predicates over evidence registries and produces
    SHA-256 verdicts for reproducibility and tamper-evidence.
    """

    def __init__(self, predicates: dict[str, Predicate] | None = None):
        self.predicates = predicates or dict(DEFAULT_PREDICATES)

    def _hash(self, data: str) -> str:
        return f"sha256:{hashlib.sha256(data.encode()).hexdigest()}"

    def verify(self, evidence: dict[str, Any]) -> Verdict:
        """Run all predicates against evidence and produce a verdict."""
        # Hash inputs
        evidence_json = json.dumps(evidence, sort_keys=True, default=str)
        registry_hash = self._hash(evidence_json)

        predicate_names = json.dumps(sorted(self.predicates.keys()))
        predicates_hash = self._hash(predicate_names)

        # Run predicates
        results: dict[str, CheckResult] = {}
        for check_id, predicate in self.predicates.items():
            try:
                result = predicate(evidence)
                results[check_id] = result
            except Exception as e:
                results[check_id] = CheckResult(
                    check_id=check_id,
                    name=check_id.replace("_", " ").title(),
                    status="FAIL",
                    severity=Severity.MAJOR,
                    message=f"Predicate raised exception: {e}",
                )

        # Determine overall status
        has_critical_fail = any(
            r.status == "FAIL" and r.severity == Severity.CRITICAL
            for r in results.values()
        )
        has_major_fail = any(
            r.status == "FAIL" and r.severity == Severity.MAJOR
            for r in results.values()
        )

        if has_critical_fail:
            overall = "FAIL"
        elif has_major_fail:
            overall = "PARTIAL"
        else:
            overall = "PASS"

        # Hash the results for tamper-evidence
        results_json = json.dumps(
            {k: v.message for k, v in results.items()},
            sort_keys=True,
        )
        verdict_hash = self._hash(
            f"{registry_hash}:{predicates_hash}:{results_json}"
        )

        # Build summary
        pass_count = sum(1 for r in results.values() if r.status == "PASS")
        fail_count = sum(1 for r in results.values() if r.status == "FAIL")
        skip_count = sum(1 for r in results.values() if r.status == "SKIP")
        warn_count = sum(1 for r in results.values() if r.status == "WARN")

        summary = (
            f"{overall}: {pass_count} passed, {fail_count} failed, "
            f"{warn_count} warnings, {skip_count} skipped "
            f"out of {len(results)} checks."
        )

        return Verdict(
            registry_hash=registry_hash,
            predicates_hash=predicates_hash,
            verdict_hash=verdict_hash,
            overall=overall,
            results=results,
            summary=summary,
        )
