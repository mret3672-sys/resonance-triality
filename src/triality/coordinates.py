"""
Core coordinate system: S = (ρ, α, ϕ)

Defines the State object and all coordinate transforms between
the polar triality space and derived representations.
"""

import math
from dataclasses import dataclass, field
from typing import Optional

from triality.constants import (
    PHI, PHI_INV, RHO_MIN, RHO_MAX,
    NUM_SECTORS, SECTOR_WIDTH_DEG,
    Phase, PHASE_DISTANCE, PULSE_SEQUENCE,
    SECTORS, Sector,
    rho_to_gssm, GSSMLayer,
    rho_to_hp, frequency_to_sector_index, frequency_to_alpha,
)


@dataclass
class State:
    """
    A point in the Resonance Triality coordinate space.

    S = (ρ, α, ϕ) where:
        ρ ∈ [0, φ]       — radial depth (pressure / attentional intensity)
        α ∈ {0,60,...,300} — angular sector (hexagonal orientation, degrees)
        ϕ ∈ {IDL,BND,COR} — phase state (132 pulse position)
    """
    rho: float
    alpha_deg: float
    phase: Phase

    def __post_init__(self):
        self.rho = max(RHO_MIN, min(float(self.rho), RHO_MAX))
        self.alpha_deg = float(self.alpha_deg) % 360.0

    @classmethod
    def from_frequency(cls, rho: float, freq: float, phase: Phase) -> "State":
        """Create a State by mapping frequency to angular sector."""
        alpha = frequency_to_alpha(freq)
        return cls(rho=rho, alpha_deg=alpha, phase=phase)

    @classmethod
    def from_sector_code(cls, rho: float, sector_code: str, phase: Phase) -> "State":
        """Create a State by sector code (TMP, ACT, GRV, GRL, CDX, ORG)."""
        from triality.constants import SECTOR_BY_CODE
        sector = SECTOR_BY_CODE[sector_code]
        return cls(rho=rho, alpha_deg=sector.angle_deg, phase=phase)

    @classmethod
    def from_hp_level(cls, hp_level: int, sector_code: str, phase: Phase) -> "State":
        """Create a State from HP pressure level (1-12) and sector."""
        from triality.constants import hp_to_rho, SECTOR_BY_CODE
        rho = hp_to_rho(hp_level)
        sector = SECTOR_BY_CODE[sector_code]
        return cls(rho=rho, alpha_deg=sector.angle_deg, phase=phase)

    @property
    def alpha_rad(self) -> float:
        """Angular coordinate in radians."""
        return math.radians(self.alpha_deg)

    @property
    def x(self) -> float:
        """Cartesian X projection: ρ × cos(α)."""
        return self.rho * math.cos(self.alpha_rad)

    @property
    def y(self) -> float:
        """Cartesian Y projection: ρ × sin(α)."""
        return self.rho * math.sin(self.alpha_rad)

    @property
    def cartesian(self) -> tuple[float, float]:
        """(X, Y) Cartesian projection."""
        return (self.x, self.y)

    @property
    def sector(self) -> Sector:
        """The hexagonal sector this state falls in."""
        idx = round(self.alpha_deg / SECTOR_WIDTH_DEG) % NUM_SECTORS
        return SECTORS[idx]

    @property
    def gssm_layer(self) -> GSSMLayer:
        """The GSSM layer for this radial depth."""
        return rho_to_gssm(self.rho)

    @property
    def hp_level(self) -> int:
        """Nearest HP-12 lattice level."""
        return rho_to_hp(self.rho)

    @property
    def pressure_index(self) -> float:
        """Continuous pressure index: ρ/φ × 12, maps [0,φ] → [0,12]."""
        return (self.rho / PHI) * 12

    @property
    def normalized_rho(self) -> float:
        """ρ normalized to [0, 1] range (dividing by φ)."""
        return self.rho / PHI

    def tuple(self) -> tuple[float, float, Phase]:
        """Return (ρ, α°, ϕ) tuple."""
        return (self.rho, self.alpha_deg, self.phase)

    def __repr__(self) -> str:
        return (
            f"S(ρ={self.rho:.3f}, α={self.alpha_deg:.0f}°[{self.sector.code}], "
            f"ϕ={self.phase.code})"
        )


def polar_to_cartesian(rho: float, alpha_deg: float) -> tuple[float, float]:
    """Convert polar (ρ, α°) to Cartesian (X, Y)."""
    alpha_rad = math.radians(alpha_deg)
    return (rho * math.cos(alpha_rad), rho * math.sin(alpha_rad))


def cartesian_to_polar(x: float, y: float) -> tuple[float, float]:
    """Convert Cartesian (X, Y) to polar (ρ, α°)."""
    rho = math.sqrt(x * x + y * y)
    alpha_deg = math.degrees(math.atan2(y, x)) % 360.0
    return (rho, alpha_deg)


def state_distance(s1: State, s2: State, phase_weight: float = 1.0) -> float:
    """
    Compute distance between two states in the triality space.

    d(S₁, S₂) = √( (x₁-x₂)² + (y₁-y₂)² + w_ϕ × δ(ϕ₁,ϕ₂)² )

    Args:
        s1, s2: States to compare.
        phase_weight: Weight for the phase distance component.
    """
    dx = s1.x - s2.x
    dy = s1.y - s2.y
    spatial_sq = dx * dx + dy * dy

    phase_d = PHASE_DISTANCE[(s1.phase, s2.phase)]
    phase_sq = phase_weight * phase_d * phase_d

    return math.sqrt(spatial_sq + phase_sq)


def interpolate_rho(rho_start: float, rho_end: float, t: float) -> float:
    """
    Linear interpolation of radial coordinate.

    Args:
        rho_start, rho_end: Start and end ρ values.
        t: Interpolation parameter in [0, 1].
    """
    t = max(0.0, min(1.0, t))
    return rho_start + t * (rho_end - rho_start)


def golden_spiral_rho(n_steps: int) -> list[float]:
    """
    Generate ρ values along the golden spiral contraction.

    Starting at φ, each step multiplies by φ⁻¹:
    φ, 1.0, φ⁻¹, φ⁻², ...

    The first 3 steps are exactly the 132 pulse targets:
    [1.618, 1.0, 0.618]
    """
    values = []
    rho = PHI
    for _ in range(n_steps):
        values.append(rho)
        rho *= PHI_INV
    return values
