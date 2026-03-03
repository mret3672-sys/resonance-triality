"""
HP-12 Pressure Lattice — 12-point topology for decision-state detection.

Maps breath rate, posture indicators, and radial coordinates to
one of 12 pressure states, from HP-12 (maximum pressure, frozen)
to LP-1 (minimum pressure, settled).

The lattice connects to the coordinate system via:
    HP level → ρ:  ρ = hp_level × (φ / 12)
    ρ → HP level:  hp = round(ρ × 12 / φ)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from triality.constants import (
    PHI, HP_LEVELS, HP_TO_RHO_SCALE,
    Phase,
    hp_to_rho, rho_to_hp, rho_to_gssm,
)


class ThermoState(Enum):
    """Thermodynamic phase states of cognition."""
    FROZEN = "frozen"           # Rigid, HP-10+ → Apply BURST
    MELTING = "melting"         # Fluid, HP-7 to HP-5 → Optimal
    VIBRATING = "vibrating"    # High energy no structure → Apply CRUSH
    TRIPLE_POINT = "triple"    # All states accessible → Execute CLICK


@dataclass
class PressureState:
    """A point on the HP-12 lattice with full diagnostic information."""
    hp_level: int               # 1-12
    rho: float                  # radial coordinate
    zone: str                   # High/Medium-High/Sweet Spot/Medium-Low/Low
    breath_rate_range: tuple[float, float]  # Hz range
    thermo_state: ThermoState
    protocol: str               # Recommended 132 action
    gssm_layer: str             # GSSM layer code

    def __repr__(self) -> str:
        return (
            f"HP-{self.hp_level} (ρ={self.rho:.3f}, {self.zone}, "
            f"{self.thermo_state.value}, → {self.protocol})"
        )


# ── Pressure state definitions ───────────────────────────────────────

_PRESSURE_DEFS = [
    # (hp, zone, breath_min, breath_max, thermo, protocol)
    (12, "High Pressure",  0.45, 0.60, ThermoState.FROZEN,       "BURST first"),
    (11, "High Pressure",  0.42, 0.50, ThermoState.FROZEN,       "BURST first"),
    (10, "High Pressure",  0.40, 0.45, ThermoState.FROZEN,       "BURST first"),
    (9,  "Medium-High",    0.37, 0.40, ThermoState.VIBRATING,    "Careful CRUSH"),
    (8,  "Medium-High",    0.33, 0.37, ThermoState.VIBRATING,    "Careful CRUSH"),
    (7,  "Medium-High",    0.30, 0.33, ThermoState.VIBRATING,    "Careful CRUSH"),
    (6,  "Sweet Spot",     0.25, 0.30, ThermoState.TRIPLE_POINT, "CLICK immediately"),
    (5,  "Medium-Low",     0.22, 0.27, ThermoState.MELTING,      "Light CRUSH + CLICK"),
    (4,  "Medium-Low",     0.20, 0.25, ThermoState.MELTING,      "Micro-CRUSH + CLICK"),
    (3,  "Low Pressure",   0.17, 0.22, ThermoState.MELTING,      "CLICK only"),
    (2,  "Low Pressure",   0.13, 0.17, ThermoState.MELTING,      "CLICK only"),
    (1,  "Low Pressure",   0.08, 0.15, ThermoState.MELTING,      "CLICK only"),
]


class HPLattice:
    """
    The 12-point pressure lattice for decision-state detection.

    Provides bidirectional mapping between:
        - HP level (1-12) ↔ ρ coordinate
        - Breath rate (Hz) → HP level
        - HP level → Protocol recommendation
        - HP level → Thermodynamic state
    """

    def __init__(self):
        self._states: dict[int, PressureState] = {}
        for hp, zone, br_min, br_max, thermo, protocol in _PRESSURE_DEFS:
            rho = hp_to_rho(hp)
            gssm = rho_to_gssm(rho)
            self._states[hp] = PressureState(
                hp_level=hp,
                rho=rho,
                zone=zone,
                breath_rate_range=(br_min, br_max),
                thermo_state=thermo,
                protocol=protocol,
                gssm_layer=gssm.code,
            )

    def get_state(self, hp_level: int) -> PressureState:
        """Get the full pressure state for an HP level."""
        if hp_level not in self._states:
            raise ValueError(f"HP level must be 1-12, got {hp_level}")
        return self._states[hp_level]

    def from_rho(self, rho: float) -> PressureState:
        """Map a radial coordinate to the nearest pressure state."""
        hp = rho_to_hp(rho)
        return self._states[hp]

    def from_breath_rate(self, breath_rate_hz: float) -> PressureState:
        """
        Detect pressure state from breath rate.

        Scans the lattice for the level whose breath rate range
        contains the given value. If between ranges, picks the
        nearest boundary.

        Args:
            breath_rate_hz: Observed breath rate in Hz (breaths per second).
                           Typical range: 0.08-0.60 Hz (5-36 breaths/min).
        """
        best_match = None
        best_dist = float("inf")

        for state in self._states.values():
            br_min, br_max = state.breath_rate_range
            if br_min <= breath_rate_hz <= br_max:
                return state
            # Track nearest if no exact match
            dist = min(abs(breath_rate_hz - br_min), abs(breath_rate_hz - br_max))
            if dist < best_dist:
                best_dist = dist
                best_match = state

        return best_match  # type: ignore

    def recommend_protocol(self, hp_level: int) -> str:
        """Get the 132 protocol recommendation for a pressure level."""
        return self._states[hp_level].protocol

    def is_sweet_spot(self, hp_level: int) -> bool:
        """Check if the pressure level is at the HP-6 sweet spot."""
        return hp_level == 6

    def is_frozen(self, hp_level: int) -> bool:
        """Check if the customer is in frozen state (HP-10+)."""
        return hp_level >= 10

    def utility_score(
        self,
        relief: float,
        momentum: float,
        gravity: float,
        cost: float,
        pressure: float,
        time: float,
    ) -> float:
        """
        Compute the Sovereign Optimization utility score.

        U = (Relief × Momentum × Gravity) / (Cost × Pressure × t) × Φ

        Decision thresholds:
            U > 7:  Execute immediately
            U = 5-7: Strong buy
            U = 3-5: Address objections
            U < 3:  Wrong fit

        Args:
            relief: Pain reduction factor (0-10)
            momentum: Forward energy (0-10)
            gravity: Attentional weight (0-10)
            cost: Financial/effort cost (0-10)
            pressure: Current pressure level (0-10)
            time: Temporal urgency factor (0-10)

        Returns:
            Utility score U.
        """
        denominator = cost * pressure * time
        if denominator <= 0:
            return float("inf")
        return (relief * momentum * gravity) / denominator * PHI

    def utility_verdict(self, u: float) -> str:
        """Interpret a utility score."""
        if u > 7:
            return "Execute immediately"
        elif u >= 5:
            return "Strong buy"
        elif u >= 3:
            return "Address objections"
        else:
            return "Wrong fit"

    def all_states(self) -> list[PressureState]:
        """Return all 12 pressure states, HP-12 down to LP-1."""
        return [self._states[i] for i in range(12, 0, -1)]

    def decision_tree(self, breath_rate_hz: float) -> dict:
        """
        Run the full Protocol Selection Decision Tree.

        Customer enters → Check breath rate →
            HP-10+?   → BURST first
            HP-7-9?   → Light CRUSH
            HP-6?     → CLICK IMMEDIATELY
            HP-4-5?   → Micro-CRUSH + CLICK
            LP-1-3?   → CLICK only

        Returns dict with state, recommendation, and phase mapping.
        """
        state = self.from_breath_rate(breath_rate_hz)

        # Map to 132 phase recommendation
        if state.hp_level >= 10:
            start_phase = Phase.IDEAL
        elif state.hp_level >= 7:
            start_phase = Phase.BOUNDARY
        else:
            start_phase = Phase.CORE

        return {
            "pressure_state": state,
            "breath_rate_hz": breath_rate_hz,
            "breath_rate_bpm": breath_rate_hz * 60,
            "recommended_protocol": state.protocol,
            "start_phase": start_phase,
            "thermo_state": state.thermo_state.value,
            "gssm_layer": state.gssm_layer,
            "rho": state.rho,
        }
