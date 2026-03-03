"""
Resonance Triality — Geometric Coordinate System S = (ρ, α, ϕ)

A unified coordinate framework connecting radial pressure depth,
hexagonal angular orientation, and 132 pulse phase topology.
"""

from triality.constants import PHI, PHI_INV, F_BASE, SECTORS, GSSM_LAYERS, Phase
from triality.coordinates import State, polar_to_cartesian, state_distance
from triality.gabor import GaborTransform
from triality.pulse_probe import PulseProbe
from triality.hp_lattice import HPLattice

__version__ = "0.1.0"
__all__ = [
    "PHI", "PHI_INV", "F_BASE",
    "SECTORS", "GSSM_LAYERS", "Phase",
    "State", "polar_to_cartesian", "state_distance",
    "GaborTransform",
    "PulseProbe",
    "HPLattice",
]
