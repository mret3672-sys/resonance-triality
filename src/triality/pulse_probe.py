"""
132 Pulse Probe — Echolocation topology for calibration.

The 132 pulse is NOT a temporal sequence — it's a calibration probe
that follows the golden spiral inward:

    IDEAL (1) → Maximum projection outward (emit pulse)
    BOUNDARY (3) → Reflection surface / resistance (detect)
    CORE (2) → Actionable truth revealed (resolve)

Echolocation analog:
    d = c × Δt / 2

Where d = distance to Core, c = propagation velocity (context-dependent),
Δt = round-trip time from Ideal projection to Boundary return.
"""

import math
from dataclasses import dataclass, field
from typing import Optional

from triality.constants import (
    PHI, PHI_INV, PHI_INV_SQ, SQRT_5,
    Phase, PULSE_SEQUENCE, PULSE_ENERGY,
    SECTORS, Sector, SECTOR_BY_CODE,
)
from triality.coordinates import State, state_distance


@dataclass
class ProbeResult:
    """Result of a single 132 pulse probe through one sector."""
    sector: Sector
    states: list[State]                # [IDEAL, BOUNDARY, CORE]
    rho_targets: list[float]           # [φ, 1.0, φ⁻¹]
    rho_actual: list[float]            # actual measured ρ at each phase
    energy: float                      # ρ(IDEAL)² - ρ(CORE)²
    convergence_ratio: float           # ρ(CORE) / ρ(IDEAL)
    boundary_reflection: float         # ρ(BOUNDARY) / ρ(IDEAL)

    @property
    def is_golden(self) -> bool:
        """Check if the probe follows golden ratio decay within tolerance."""
        tol = 0.02  # tight tolerance — 2% relative
        return (
            abs(self.boundary_reflection - PHI_INV) < tol
            and abs(self.convergence_ratio - PHI_INV_SQ) < tol
        )

    @property
    def distance_to_core(self) -> float:
        """Radial distance from IDEAL to CORE."""
        return self.rho_actual[0] - self.rho_actual[2]

    def __repr__(self) -> str:
        return (
            f"Probe[{self.sector.code}]: "
            f"ρ={self.rho_actual[0]:.3f}→{self.rho_actual[1]:.3f}→{self.rho_actual[2]:.3f} "
            f"E={self.energy:.3f} conv={self.convergence_ratio:.3f}"
        )


class PulseProbe:
    """
    Execute 132 calibration pulses through the hexagonal lattice.

    A pulse probe emits at IDEAL (ρ=φ), detects at BOUNDARY (ρ=1.0),
    and resolves at CORE (ρ=φ⁻¹), following the golden spiral contraction.

    The probe can be run through any sector, and the actual measured ρ values
    at each phase reveal the state of that sector.

    In sales terms:
        IDEAL  = Price/effort anchor (maximum projection)
        BOUNDARY = Customer resistance surface
        CORE   = Actual transaction point
    """

    def __init__(self, propagation_velocity: float = 1.0):
        """
        Args:
            propagation_velocity: Context-dependent speed of the probe.
                In echolocation: speed of sound.
                In conversation: abstract (set to 1.0 for normalized).
        """
        self.c = propagation_velocity

    def probe_sector(
        self,
        sector_code: str,
        rho_ideal: Optional[float] = None,
        rho_boundary: Optional[float] = None,
        rho_core: Optional[float] = None,
    ) -> ProbeResult:
        """
        Execute a 132 pulse through a single sector.

        Default ρ targets follow golden ratio decay:
            IDEAL: φ, BOUNDARY: 1.0, CORE: φ⁻¹

        Override with actual measured values to compute diagnostics.

        Args:
            sector_code: Sector to probe (TMP, ACT, GRV, GRL, CDX, ORG).
            rho_ideal: Actual ρ at IDEAL phase (default φ).
            rho_boundary: Actual ρ at BOUNDARY phase (default 1.0).
            rho_core: Actual ρ at CORE phase (default φ⁻¹).
        """
        sector = SECTOR_BY_CODE[sector_code]

        r_i = rho_ideal if rho_ideal is not None else PHI
        r_b = rho_boundary if rho_boundary is not None else 1.0
        r_c = rho_core if rho_core is not None else PHI_INV

        states = [
            State(rho=r_i, alpha_deg=sector.angle_deg, phase=Phase.IDEAL),
            State(rho=r_b, alpha_deg=sector.angle_deg, phase=Phase.BOUNDARY),
            State(rho=r_c, alpha_deg=sector.angle_deg, phase=Phase.CORE),
        ]

        energy = r_i ** 2 - r_c ** 2
        convergence = r_c / r_i if r_i > 0 else 0.0
        reflection = r_b / r_i if r_i > 0 else 0.0

        return ProbeResult(
            sector=sector,
            states=states,
            rho_targets=[PHI, 1.0, PHI_INV],
            rho_actual=[r_i, r_b, r_c],
            energy=energy,
            convergence_ratio=convergence,
            boundary_reflection=reflection,
        )

    def probe_all_sectors(
        self,
        rho_overrides: Optional[dict[str, tuple[float, float, float]]] = None,
    ) -> list[ProbeResult]:
        """
        Execute 132 pulse through all 6 sectors.

        Args:
            rho_overrides: Dict mapping sector code → (ρ_ideal, ρ_boundary, ρ_core).
                          Sectors not in dict use golden ratio defaults.

        Returns:
            List of 6 ProbeResults, one per sector.
        """
        rho_overrides = rho_overrides or {}
        results = []
        for sector in SECTORS:
            if sector.code in rho_overrides:
                r_i, r_b, r_c = rho_overrides[sector.code]
                result = self.probe_sector(sector.code, r_i, r_b, r_c)
            else:
                result = self.probe_sector(sector.code)
            results.append(result)
        return results

    def echolocation_distance(self, delta_t: float) -> float:
        """
        Compute distance to Core from round-trip time.

        d = c × Δt / 2

        Args:
            delta_t: Round-trip time from emission to return.

        Returns:
            Distance to Core (in units determined by propagation velocity).
        """
        return self.c * delta_t / 2.0

    def golden_spiral_trajectory(self, sector_code: str, n_steps: int = 10) -> list[State]:
        """
        Generate a full golden spiral trajectory through a sector.

        Starting at ρ=φ, each step contracts by φ⁻¹.
        The first 3 points are the 132 pulse targets.

        Args:
            sector_code: Sector to spiral through.
            n_steps: Number of spiral points.

        Returns:
            List of States along the spiral.
        """
        sector = SECTOR_BY_CODE[sector_code]
        trajectory = []
        rho = PHI

        for i in range(n_steps):
            # Assign phase based on position in spiral
            if i % 3 == 0:
                phase = Phase.IDEAL
            elif i % 3 == 1:
                phase = Phase.BOUNDARY
            else:
                phase = Phase.CORE

            trajectory.append(State(
                rho=rho,
                alpha_deg=sector.angle_deg,
                phase=phase,
            ))
            rho *= PHI_INV

        return trajectory

    @staticmethod
    def ideal_energy() -> float:
        """
        Energy of a perfect golden-ratio 132 pulse.

        E = φ² - φ⁻² = √5 ≈ 2.236

        This is exact, not approximate — a consequence of the identity:
        φ² - φ⁻² = (φ + φ⁻¹)(φ - φ⁻¹) = √5 × 1 = √5
        """
        return PULSE_ENERGY

    def diagnose(self, result: ProbeResult) -> dict:
        """
        Diagnose a probe result against golden-ratio ideal.

        Returns dict with:
            deviation: How far from golden ratio targets
            recommendation: Protocol recommendation based on state
            energy_efficiency: ratio of actual to ideal energy
        """
        # Deviations from ideal
        dev_boundary = abs(result.boundary_reflection - PHI_INV)
        dev_convergence = abs(result.convergence_ratio - PHI_INV_SQ)

        # Energy efficiency
        energy_efficiency = result.energy / PULSE_ENERGY if PULSE_ENERGY > 0 else 0.0

        # Protocol recommendation based on where the probe landed
        avg_rho = sum(result.rho_actual) / 3
        if avg_rho > 1.294:
            protocol = "BURST first — high pressure zone, expand chamber"
        elif avg_rho > 0.971:
            protocol = "Careful CRUSH — medium-high, gentle grounding"
        elif avg_rho > 0.647:
            protocol = "CLICK immediately — sweet spot, decision window open"
        elif avg_rho > 0.324:
            protocol = "Micro-CRUSH + CLICK — medium-low"
        else:
            protocol = "CLICK only — low pressure, no compression needed"

        return {
            "is_golden": result.is_golden,
            "boundary_deviation": dev_boundary,
            "convergence_deviation": dev_convergence,
            "energy_efficiency": energy_efficiency,
            "protocol_recommendation": protocol,
        }
