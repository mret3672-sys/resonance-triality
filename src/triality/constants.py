"""
Constants for the Resonance Triality coordinate system.

All fundamental values are defined here. Design choices are annotated
with their justification and confidence level.
"""

import math
from enum import Enum
from typing import NamedTuple


# ── Golden Ratio ──────────────────────────────────────────────────────
PHI = (1 + math.sqrt(5)) / 2          # 1.618033988749895
PHI_INV = 1 / PHI                      # 0.6180339887498949
PHI_SQ = PHI ** 2                      # 2.6180339887498953
PHI_INV_SQ = PHI_INV ** 2              # 0.38196601125010515
SQRT_5 = math.sqrt(5)                  # 2.23606797749979 = pulse energy

# ── Radial bounds ─────────────────────────────────────────────────────
RHO_MIN = 0.0
RHO_MAX = PHI       # Maximum radial projection
RHO_UNITY = 1.0     # φ⁻¹ reflection point (Boundary target)

# ── Angular sectors ───────────────────────────────────────────────────
NUM_SECTORS = 6
SECTOR_WIDTH_DEG = 360.0 / NUM_SECTORS  # 60°
SECTOR_WIDTH_RAD = 2 * math.pi / NUM_SECTORS


class Sector(NamedTuple):
    """A hexagonal sector definition."""
    index: int
    code: str
    name: str
    angle_deg: float
    angle_rad: float


SECTORS = [
    Sector(0, "TMP", "Temporal Navigation",  0.0,   0.0),
    Sector(1, "ACT", "Actualize Output",     60.0,  math.pi / 3),
    Sector(2, "GRV", "Gravity Synthesis",    120.0, 2 * math.pi / 3),
    Sector(3, "GRL", "Gralv Synthesis",      180.0, math.pi),
    Sector(4, "CDX", "Codex Vault",          240.0, 4 * math.pi / 3),
    Sector(5, "ORG", "Origin (W-O bilateral)", 300.0, 5 * math.pi / 3),
]

SECTOR_BY_CODE = {s.code: s for s in SECTORS}
SECTOR_BY_INDEX = {s.index: s for s in SECTORS}


# ── Base frequency for α mapping ─────────────────────────────────────
# Confidence: 0.65 — convergence of speech F0, musical grounding, psychoacoustic floor.
# Requires empirical validation against speech corpus.
F_BASE = 125.0  # Hz


def frequency_to_sector_index(f: float) -> int:
    """
    Map a frequency to a sector index using octave-periodic log-frequency binning.

    α = floor(6 × frac(log₂(f / f_base))) × 60°

    This is the EXPLICIT mapping that closes the α gap identified in the
    epistemic audit. It is octave-periodic: frequencies one octave apart
    map to the same sector. Within each octave, 6 equal log-frequency bins
    map to the 6 hexagonal sectors.

    Args:
        f: Frequency in Hz. Must be > 0.

    Returns:
        Sector index in {0, 1, 2, 3, 4, 5}.
    """
    if f <= 0:
        raise ValueError(f"Frequency must be positive, got {f}")

    log2_ratio = math.log2(f / F_BASE)
    fractional = log2_ratio % 1.0  # octave-periodic: frac(log₂(f/f_base))
    sector_idx = int(fractional * NUM_SECTORS) % NUM_SECTORS
    return sector_idx


def frequency_to_alpha(f: float) -> float:
    """Map frequency to angular coordinate in degrees."""
    return frequency_to_sector_index(f) * SECTOR_WIDTH_DEG


# ── GSSM Layers ──────────────────────────────────────────────────────

class GSSMLayer(NamedTuple):
    """A concentric radial layer in the GSSM model."""
    index: int
    code: str
    name: str
    rho_min: float
    rho_max: float
    hp_range: str


# Boundaries at φ × (n/5) for n ∈ {0, 1, 2, 3, 4, 5}
_boundaries = [PHI * n / 5 for n in range(6)]

GSSM_LAYERS = [
    GSSMLayer(0, "EPI", "Epicenter",   _boundaries[0], _boundaries[1], "LP-3 to LP-1"),
    GSSMLayer(1, "MAR", "Mark",        _boundaries[1], _boundaries[2], "HP-5 to HP-4"),
    GSSMLayer(2, "STA", "Stabilize",   _boundaries[2], _boundaries[3], "HP-6 (Sweet Spot)"),
    GSSMLayer(3, "SUP", "Support",     _boundaries[3], _boundaries[4], "HP-9 to HP-7"),
    GSSMLayer(4, "GUI", "Guide",       _boundaries[4], _boundaries[5], "HP-12 to HP-10"),
]

GSSM_BY_CODE = {layer.code: layer for layer in GSSM_LAYERS}


def rho_to_gssm(rho: float) -> GSSMLayer:
    """Map a radial value to its GSSM layer."""
    rho = max(RHO_MIN, min(rho, RHO_MAX))
    for layer in GSSM_LAYERS:
        if layer.rho_min <= rho < layer.rho_max:
            return layer
    # rho == PHI exactly → top of GUIDE
    return GSSM_LAYERS[-1]


# ── Phase states (132 Protocol) ──────────────────────────────────────

class Phase(Enum):
    """
    The three distinguished states of the 132 pulse topology.

    Named by their 132 sequence position:
    - IDEAL (1): Maximum outward projection, emit pulse
    - BOUNDARY (3): Reflection surface, detect resistance
    - CORE (2): Convergence point, resolve to action
    """
    IDEAL = 1       # ϕ₁ — emit, project, search mode
    BOUNDARY = 3    # ϕ₃ — reflect, detect, approach
    CORE = 2        # ϕ₂ — resolve, converge, terminal

    @property
    def code(self) -> str:
        return {1: "IDL", 3: "BND", 2: "COR"}[self.value]

    @property
    def rho_target(self) -> float:
        """Golden ratio target ρ for this phase."""
        return {1: PHI, 3: RHO_UNITY, 2: PHI_INV}[self.value]

    @property
    def sequence_order(self) -> int:
        """Position in the 132 execution sequence (0-indexed)."""
        return {1: 0, 3: 1, 2: 2}[self.value]


# 132 sequence as ordered list
PULSE_SEQUENCE = [Phase.IDEAL, Phase.BOUNDARY, Phase.CORE]

# Phase distance matrix (for state_distance calculation)
PHASE_DISTANCE = {
    (Phase.IDEAL, Phase.IDEAL): 0.0,
    (Phase.IDEAL, Phase.BOUNDARY): PHI_INV,
    (Phase.IDEAL, Phase.CORE): 1.0,
    (Phase.BOUNDARY, Phase.IDEAL): PHI_INV,
    (Phase.BOUNDARY, Phase.BOUNDARY): 0.0,
    (Phase.BOUNDARY, Phase.CORE): PHI_INV,
    (Phase.CORE, Phase.IDEAL): 1.0,
    (Phase.CORE, Phase.BOUNDARY): PHI_INV,
    (Phase.CORE, Phase.CORE): 0.0,
}

# ── Pulse energy ──────────────────────────────────────────────────────
# E_pulse = φ² - φ⁻² = √5
PULSE_ENERGY = PHI_SQ - PHI_INV_SQ  # ≈ 2.236 = √5


# ── HP-12 Lattice mapping ────────────────────────────────────────────
HP_LEVELS = 12
HP_TO_RHO_SCALE = RHO_MAX / HP_LEVELS  # Each HP level = φ/12 in ρ


def hp_to_rho(hp_level: int) -> float:
    """Convert HP level (1-12) to radial coordinate."""
    if not 1 <= hp_level <= 12:
        raise ValueError(f"HP level must be 1-12, got {hp_level}")
    return hp_level * HP_TO_RHO_SCALE


def rho_to_hp(rho: float) -> int:
    """Convert radial coordinate to nearest HP level (1-12)."""
    rho = max(RHO_MIN, min(rho, RHO_MAX))
    level = round(rho / HP_TO_RHO_SCALE)
    return max(1, min(12, level))


# ── Breath mapping ───────────────────────────────────────────────────
# 4-7-8 Spiral Breathing maps to 132 Protocol
BREATH_INHALE = 4    # seconds — maps to BURST/IDEAL
BREATH_HOLD = 7      # seconds — maps to CRUSH/BOUNDARY
BREATH_EXHALE = 8    # seconds — maps to CLICK/CORE
BREATH_TOTAL = BREATH_INHALE + BREATH_HOLD + BREATH_EXHALE  # 19 seconds
