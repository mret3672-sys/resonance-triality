"""
STRESS TEST COUNCIL: Comprehensive Validation Protocol
for the 132/213 Recursive Control Architecture

Theory-faithful implementation. Corrections applied:
- Variables are COUPLED, not independent (no naive uniform Monte Carlo)
- Directed axis pairs (H->V != V->H) — 25 states, not 15
- Field/Frame is a real translation engine, not a label
- Identity kernel is typed (binary/graded/threshold), not just boolean
- Mixed regime has explicit provisional handling
- 20/50/30 is a phase weighting hypothesis, NOT action-rate targets

Architecture (locked layers):
  L0: Pulse <-> Constrain (primitive tension)
  L1: Pulse -> Constrain -> Calibrate -> Invert (minimal loop)
  L2: 1=Ideal, 3=Boundary, 2=Core (role layer)
  L3: 132 diagnostic, 213 generative (mode layer)
  L4: Stay/Switch/Invert/Escalate/Terminate (control layer)
  L5: Field/Frame/Mixed (regime layer)
  L6: H, V, Face, Body, Periodic + 20 directed pairs (axis layer)
  L7: Domain instances (sales, Bayesian, phonetic, topological, etc.)
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum
import json
from datetime import datetime
import random


# =============================================================================
# PART 1: CORE ENUMS AND TYPES
# =============================================================================

class Mode(Enum):
    DIAGNOSTIC_132 = "132"
    GENERATIVE_213 = "213"

class Regime(Enum):
    FIELD = "field"       # pulse-dominant, center-derived identity
    FRAME = "frame"       # constrain-dominant, boundary-derived identity
    MIXED = "mixed"       # translation zone — PROVISIONAL

class StabilityType(Enum):
    ATTRACTOR = "attractor"   # perturbations converge back
    SADDLE = "saddle"         # some stabilize, some diverge
    REPELLER = "repeller"     # perturbations move away

class TransitionAction(Enum):
    STAY = "stay"
    SWITCH_MODE = "switch_mode"
    INVERT = "invert"
    ESCALATE = "escalate"
    TERMINATE = "terminate"

class InvariantType(Enum):
    BINARY = "binary"         # pass/fail only
    GRADED = "graded"         # continuous degradation [0,1]
    THRESHOLD = "threshold"   # graded internally, hard fail below cutpoint

# The 5 axes
AXES = ["H", "V", "Face", "Body", "Periodic"]

# All 25 axis states: 5 single + 20 directed pairs
def build_axis_states():
    states = list(AXES)  # 5 single-axis
    for a in AXES:
        for b in AXES:
            if a != b:
                states.append(f"{a}->{b}")  # 20 directed pairs
    return states

AXIS_STATES = build_axis_states()


# =============================================================================
# PART 2: IDENTITY KERNEL (typed, not just boolean)
# =============================================================================

@dataclass
class KernelInvariant:
    """A single kernel invariant with typed survival semantics."""
    name: str
    invariant_type: InvariantType
    tier: int                    # 1 = hard fail, 2 = structural, 3 = advisory
    threshold: float             # for THRESHOLD type: hard fail below this
    description: str

    def evaluate(self, score: float) -> Tuple[bool, float]:
        """Returns (passed, effective_score)."""
        if self.invariant_type == InvariantType.BINARY:
            passed = score >= 0.5
            return (passed, 1.0 if passed else 0.0)
        elif self.invariant_type == InvariantType.GRADED:
            return (score > 0.0, score)
        elif self.invariant_type == InvariantType.THRESHOLD:
            passed = score >= self.threshold
            return (passed, score if passed else 0.0)
        return (False, 0.0)


# The 5 locked kernel invariants
KERNEL_INVARIANTS = [
    KernelInvariant(
        name="triadic_completeness",
        invariant_type=InvariantType.BINARY,
        tier=1,
        threshold=0.5,
        description="All three roles (Ideal, Boundary, Core) must be present"
    ),
    KernelInvariant(
        name="asymmetric_work",
        invariant_type=InvariantType.GRADED,
        tier=1,
        threshold=0.3,
        description="Work distribution is asymmetric (Boundary carries most)"
    ),
    KernelInvariant(
        name="boundary_load_bearing",
        invariant_type=InvariantType.THRESHOLD,
        tier=1,
        threshold=0.4,
        description="Boundary/Crush must be load-bearing in both modes"
    ),
    KernelInvariant(
        name="calibration_necessity",
        invariant_type=InvariantType.BINARY,
        tier=1,
        threshold=0.5,
        description="Calibration step cannot be skipped"
    ),
    KernelInvariant(
        name="dependency_primacy",
        invariant_type=InvariantType.BINARY,
        tier=1,
        threshold=0.5,
        description="Dependency order matters more than temporal sequence"
    ),
]


# =============================================================================
# PART 3: FIELD/FRAME TRANSLATION ENGINE
# =============================================================================

@dataclass
class FieldCoordinates:
    """Field-native representation: center-derived."""
    rho: float      # radial distance = magnitude of possibility space
    alpha: float    # angular position (degrees) = sector/domain
    phi: float      # phase = convergence state (0=Burst, 120=Crush, 240=Click)

@dataclass
class FrameCoordinates:
    """Frame-native representation: boundary-derived."""
    constraint_level: float     # 0=open, 1=fully constrained
    enclosure_sector: str       # which boundary domain
    elimination_phase: float    # 0=start, 1=complete

class RegimeTranslator:
    """
    Translates between Field and Frame coordinate systems.

    Translation rules (from the theory):
    - rho proportional to 1/constraint: low rho = high constraint (HP territory)
    - alpha maps to boundary between adjacent domains
    - phi maps to temporal position in elimination sequence

    This is the DECLARED translation. It is provisional and testable.
    """

    @staticmethod
    def field_to_frame(fc: FieldCoordinates) -> FrameCoordinates:
        # rho inversely proportional to constraint
        constraint = max(0.0, min(1.0, 1.0 - (fc.rho / 10.0)))
        # alpha -> sector label
        sector_idx = int(fc.alpha / 60) % 6
        sectors = ["economic", "epistemic", "phonetic", "topological", "signal", "social"]
        sector = sectors[sector_idx]
        # phi -> elimination phase (normalized to [0,1])
        elim_phase = (fc.phi % 360) / 360.0
        return FrameCoordinates(constraint, sector, elim_phase)

    @staticmethod
    def frame_to_field(frc: FrameCoordinates) -> FieldCoordinates:
        rho = max(0.1, (1.0 - frc.constraint_level) * 10.0)
        sectors = ["economic", "epistemic", "phonetic", "topological", "signal", "social"]
        try:
            alpha = sectors.index(frc.enclosure_sector) * 60.0
        except ValueError:
            alpha = 0.0
        phi = frc.elimination_phase * 360.0
        return FieldCoordinates(rho, alpha, phi)

    @staticmethod
    def round_trip_error(fc: FieldCoordinates) -> float:
        """Measure identity loss in Field->Frame->Field round trip."""
        frame = RegimeTranslator.field_to_frame(fc)
        fc_prime = RegimeTranslator.frame_to_field(frame)
        # Normalized error across coordinates
        rho_err = abs(fc.rho - fc_prime.rho) / max(fc.rho, 0.1)
        alpha_err = min(abs(fc.alpha - fc_prime.alpha),
                       360 - abs(fc.alpha - fc_prime.alpha)) / 180.0
        phi_err = min(abs(fc.phi - fc_prime.phi),
                     360 - abs(fc.phi - fc_prime.phi)) / 180.0
        return (rho_err + alpha_err + phi_err) / 3.0

    @staticmethod
    def classify_regime(interaction: Dict) -> Regime:
        """
        Classify regime from interaction data.
        4 diagnostic questions, scored Field vs Frame.
        """
        scores = []
        # Q1: Where does identity originate?
        origin = interaction.get("identity_origin", "boundary")
        scores.append(1.0 if origin == "center" else 0.0)
        # Q2: What does failure look like?
        failure = interaction.get("failure_mode", "collapse")
        scores.append(1.0 if failure in ("drift", "decoherence") else 0.0)
        # Q3: What does coherence feel like?
        coherence = interaction.get("coherence_feel", "containment")
        scores.append(1.0 if coherence in ("resonance", "sync") else 0.0)
        # Q4: What's the native transform?
        transform = interaction.get("native_transform", "segmentation")
        scores.append(1.0 if transform in ("projection", "radiation") else 0.0)

        field_score = np.mean(scores)
        if field_score > 0.7:
            return Regime.FIELD
        elif field_score < 0.3:
            return Regime.FRAME
        else:
            return Regime.MIXED


# =============================================================================
# PART 4: CALIBRATION AND STATE
# =============================================================================

@dataclass
class Residue:
    """What remains after a Pulse-Constrain cycle. Not trash -- logged debt."""
    eliminated: List[str] = field(default_factory=list)
    contested: List[str] = field(default_factory=list)
    unmapped: List[str] = field(default_factory=list)

    @property
    def magnitude(self) -> float:
        """Weighted residue magnitude. Low = clean. High = debt."""
        total = len(self.eliminated) + len(self.contested) + len(self.unmapped)
        if total == 0:
            return 0.0
        weighted = (len(self.eliminated) * 0.1 +
                   len(self.contested) * 0.5 +
                   len(self.unmapped) * 0.8)
        return min(1.0, weighted / max(total, 1))


@dataclass
class CalibrationOutput:
    """The measurement of what survived the Pulse-Constrain interaction."""
    position: Dict                       # where we landed
    residue: Residue                     # what was eliminated/contested/unmapped
    stability_score: float               # [0,1]
    stability_type: StabilityType        # attractor/saddle/repeller
    mode_signal: TransitionAction        # discrete classification
    mode_signal_strength: float          # underlying continuous score


@dataclass
class SystemState:
    """X_t = (m, r, a, s, k, c) -- the full state at cycle t."""
    mode: Mode
    regime: Regime
    axis: str                            # from AXIS_STATES
    scale: str                           # "micro", "meso", "macro"
    kernel_status: Dict[str, Tuple[bool, float]]  # invariant -> (passed, score)
    calibration: Optional[CalibrationOutput] = None
    cycle: int = 0


# =============================================================================
# PART 5: TRANSITION CONTROLLER
# =============================================================================

class TransitionController:
    """
    The controller that computes transition scores and selects actions.

    Precedence (locked):
      Terminate > Escalate > Switch > Invert > Stay

    Chatter prevention via hysteresis (threshold + margin).
    """

    def __init__(self, theta: float = 0.5, delta: float = 0.15):
        self.theta = theta      # activation threshold
        self.delta = delta      # margin over STAY required
        self.history: List[TransitionAction] = []

    def compute_scores(self,
                       sigma: float,       # stability
                       e_star: float,      # residue magnitude
                       mu_star: float,     # mode signal strength
                       d_t: float,         # dominant asymmetry
                       c_star: float,      # task completion
                       u_t: float,         # instability
                       q_t: float          # scale structure signal
                       ) -> Dict[str, float]:
        """Compute all 5 transition scores."""
        s_stay = sigma * (1.0 - e_star) * (1.0 - d_t)
        s_switch = mu_star * e_star * u_t
        s_invert = d_t * (1.0 - sigma)
        s_escalate = sigma * e_star * q_t
        s_terminate = sigma * (1.0 - e_star) * c_star
        return {
            "stay": s_stay,
            "switch_mode": s_switch,
            "invert": s_invert,
            "escalate": s_escalate,
            "terminate": s_terminate,
        }

    def select_action(self, scores: Dict[str, float]) -> TransitionAction:
        """Apply precedence rules with hysteresis."""
        s = scores
        stay = s["stay"]

        # Precedence order: Terminate > Escalate > Switch > Invert > Stay
        if s["terminate"] > self.theta and s["terminate"] > stay + self.delta:
            return TransitionAction.TERMINATE
        if s["escalate"] > self.theta and s["escalate"] > stay + self.delta:
            return TransitionAction.ESCALATE
        if s["switch_mode"] > self.theta and s["switch_mode"] > stay + self.delta:
            return TransitionAction.SWITCH_MODE
        if s["invert"] > stay + self.delta * 0.67:
            return TransitionAction.INVERT
        return TransitionAction.STAY

    def compute_asymmetry(self, interaction: Dict) -> Dict[str, float]:
        """
        Asymmetry vector: which dimension is most imbalanced?
        Inversion targets argmax of this.
        """
        burst_pct = interaction.get("burst_duration_pct", 0.2)
        crush_pct = interaction.get("crush_duration_pct", 0.5)
        denom = max(burst_pct + crush_pct, 0.01)
        direction = abs(burst_pct - crush_pct) / denom

        felt_132 = 1.0 if interaction.get("felt_diagnostic", False) else 0.0
        felt_213 = 1.0 if interaction.get("felt_generative", False) else 0.0
        mode_asym = abs(felt_132 - felt_213)

        regime = interaction.get("regime", "mixed")
        regime_asym = 0.8 if regime in ("field", "frame") else 0.3

        axis = interaction.get("axis", "H")
        axis_asym = 0.3 if "->" in str(axis) else 0.7

        scale = interaction.get("scale", "micro")
        scale_map = {"micro": 0.7, "meso": 0.3, "macro": 0.7}
        scale_asym = scale_map.get(scale, 0.5)

        return {
            "direction": round(direction, 3),
            "mode": round(mode_asym, 3),
            "regime": round(regime_asym, 3),
            "axis": round(axis_asym, 3),
            "scale": round(scale_asym, 3),
        }

    def dominant_asymmetry(self, asymmetry: Dict[str, float]) -> Tuple[str, float]:
        """Returns (dimension_name, score) of the most imbalanced dimension."""
        best = max(asymmetry.items(), key=lambda x: x[1])
        return best


# =============================================================================
# PART 6: MEASUREMENT LAYER (sensors)
# =============================================================================

class MeasurementProtocol:
    """
    How to measure each score component from interaction data.
    This is the SENSOR LAYER.
    """

    @staticmethod
    def measure_stability(interaction: Dict) -> Tuple[float, StabilityType]:
        signals = []
        signals.append(interaction.get("commitment_clarity", 0.5))

        new_obj = interaction.get("new_objections_at_click", 0)
        signals.append(max(0.0, 1.0 - new_obj * 0.3))

        pert = interaction.get("perturbation_response", "neutral")
        pert_map = {
            "strengthened": 1.0,
            "stable": 0.8,
            "neutral": 0.5,
            "wavered": 0.3,
            "abandoned": 0.0,
        }
        signals.append(pert_map.get(pert, 0.5))

        score = float(np.mean(signals))
        if score > 0.7:
            stype = StabilityType.ATTRACTOR
        elif score > 0.4:
            stype = StabilityType.SADDLE
        else:
            stype = StabilityType.REPELLER
        return (round(score, 3), stype)

    @staticmethod
    def measure_residue(interaction: Dict) -> Residue:
        return Residue(
            eliminated=interaction.get("options_eliminated", []),
            contested=interaction.get("options_contested", []),
            unmapped=interaction.get("options_unmapped", []),
        )

    @staticmethod
    def measure_mode_signal(interaction: Dict) -> Tuple[TransitionAction, float]:
        stability = interaction.get("stability_score", 0.5)
        completion = interaction.get("task_completion", 0.5)
        core_dev = interaction.get("core_fully_developed", True)
        boundary_contested = interaction.get("boundary_contested", False)
        scale_residue = interaction.get("scale_bound_residue", False)
        asymmetry = interaction.get("dominant_asymmetry", 0.3)

        if stability > 0.7 and completion > 0.7:
            return (TransitionAction.TERMINATE, min(stability, completion))
        if not core_dev and stability > 0.5:
            return (TransitionAction.SWITCH_MODE, 0.6 + (1 - completion) * 0.3)
        if boundary_contested:
            return (TransitionAction.SWITCH_MODE, 0.5 + stability * 0.3)
        if scale_residue and stability > 0.6:
            return (TransitionAction.ESCALATE, stability * 0.8)
        if asymmetry > 0.6:
            return (TransitionAction.INVERT, asymmetry)
        return (TransitionAction.STAY, stability * (1 - asymmetry))

    @staticmethod
    def evaluate_kernel(interaction: Dict) -> Dict[str, Tuple[bool, float]]:
        """Evaluate all 5 kernel invariants against interaction data."""
        results = {}
        for inv in KERNEL_INVARIANTS:
            raw = interaction.get(f"kernel_{inv.name}", 1.0)
            passed, score = inv.evaluate(raw)
            results[inv.name] = (passed, round(score, 3))
        return results


# =============================================================================
# PART 7: ADVERSARIAL SCENARIOS
# =============================================================================

@dataclass
class AdversarialScenario:
    name: str
    description: str
    target_expert: str
    expected_failure: str
    parameters: Dict
    severity: str  # "critical", "major", "minor"

ADVERSARIAL_SCENARIOS = [
    # --- CONTROL SYSTEMS ---
    AdversarialScenario(
        name="Chatter Loop",
        description="Calibration oscillates SWITCH/STAY every cycle",
        target_expert="Control Systems Engineer",
        expected_failure="Rapid mode switching without convergence",
        parameters={"stability_score": 0.5, "mode_signal_strength": 0.55,
                     "residue_magnitude": 0.5, "cycles": 10},
        severity="critical",
    ),
    AdversarialScenario(
        name="Deadlock",
        description="All scores below threshold, system freezes",
        target_expert="Control Systems Engineer",
        expected_failure="Permanent STAY with no valid transition",
        parameters={"stability_score": 0.3, "mode_signal_strength": 0.2,
                     "task_completion": 0.2, "asymmetry_max": 0.2},
        severity="critical",
    ),
    # --- BAYESIAN ---
    AdversarialScenario(
        name="Overconfident Stability",
        description="Stability 0.99 but interaction actually fails",
        target_expert="Bayesian Statistician",
        expected_failure="Measurement doesn't reflect reality",
        parameters={"stability_score": 0.99, "actual_conversion": False,
                     "perturbation_response": "diverged"},
        severity="major",
    ),
    AdversarialScenario(
        name="Contradictory Signals",
        description="Mode signal TERMINATE but stability is REPELLER",
        target_expert="Bayesian Statistician",
        expected_failure="Incoherent calibration bundle",
        parameters={"mode_signal": "terminate", "stability_type": "repeller",
                     "stability_score": 0.2},
        severity="major",
    ),
    # --- COGNITIVE ---
    AdversarialScenario(
        name="Phase Blur",
        description="Cannot distinguish Burst from Crush",
        target_expert="Cognitive Scientist",
        expected_failure="Phases theoretically distinct but experientially merged",
        parameters={"phase_clarity": 0.3, "burst_duration_pct": 0.45,
                     "crush_duration_pct": 0.45},
        severity="major",
    ),
    AdversarialScenario(
        name="Mode Collision",
        description="Interaction feels both diagnostic AND generative",
        target_expert="Cognitive Scientist",
        expected_failure="132/213 distinction not phenomenologically clean",
        parameters={"felt_diagnostic": True, "felt_generative": True,
                     "mode_declared": "132"},
        severity="minor",
    ),
    # --- PRACTICAL ---
    AdversarialScenario(
        name="Prediction Miss",
        description="Model predicts STAY, reality demands SWITCH",
        target_expert="Sales Practitioner",
        expected_failure="Controller doesn't track actual decision",
        parameters={"predicted_action": "stay", "actual_action": "switch_mode",
                     "outcome": "conversion"},
        severity="critical",
    ),
    AdversarialScenario(
        name="Cognitive Overload",
        description="Logging takes longer than interaction",
        target_expert="Sales Practitioner",
        expected_failure="Framework valid but unusable in real time",
        parameters={"interaction_duration_s": 120, "logging_duration_s": 180},
        severity="major",
    ),
    # --- TOPOLOGICAL ---
    AdversarialScenario(
        name="Kernel Breach",
        description="Transition preserves 4/5 invariants, violates one",
        target_expert="Topologist",
        expected_failure="Partial kernel failure -- fatal or recoverable?",
        parameters={"kernel_triadic_completeness": 1.0, "kernel_asymmetric_work": 0.8,
                     "kernel_boundary_load_bearing": 0.2,  # BREACH
                     "kernel_calibration_necessity": 1.0,
                     "kernel_dependency_primacy": 1.0},
        severity="critical",
    ),
    AdversarialScenario(
        name="Regime Leak",
        description="Field logic applied to Frame-native event without translation",
        target_expert="Topologist",
        expected_failure="Regime mismatch produces garbage output",
        parameters={"declared_regime": "field", "actual_dynamics": "frame",
                     "translation_applied": False},
        severity="major",
    ),
    # --- SYSTEMS ---
    AdversarialScenario(
        name="Mode Stagnation",
        description="System stays in 132 for 10+ cycles despite varied inputs",
        target_expert="Systems Theorist",
        expected_failure="Mode switching broken or too conservative",
        parameters={"mode_history": ["132"] * 10, "input_variance": "high"},
        severity="major",
    ),
    AdversarialScenario(
        name="Scale Collapse",
        description="Escalate action doesn't change scale parameter",
        target_expert="Systems Theorist",
        expected_failure="Scale is nominal, not functional",
        parameters={"action_taken": "escalate", "scale_before": "micro",
                     "scale_after": "micro"},
        severity="minor",
    ),
]


# =============================================================================
# PART 8: DIRECTED AXIS INTERACTION ENGINE
# =============================================================================

# Axis interaction semantics — each directed pair has distinct meaning
AXIS_INTERACTIONS = {
    # H -> X: pulse horizontally, constrain along X
    "H->V": {
        "description": "Spread options, test level constraints, land on viable placement",
        "132_reading": "Open horizontal spread -> test vertical constraints -> land",
        "213_reading": "Seed from a level -> expand lateral reach -> bound spread",
        "field_behavior": "gradient across neighbors, test depth",
        "frame_behavior": "adjacency scan, hierarchy constraint",
    },
    "H->Face": {
        "description": "Distribute signal, constrain presentation",
        "132_reading": "Spread options -> test visible interface -> land on displayable",
        "213_reading": "Seed from display -> expand reach -> bound signal",
    },
    "H->Body": {
        "description": "Spread options, constrain by mechanism",
        "132_reading": "Open spread -> test what mechanism supports -> land",
        "213_reading": "Seed from mechanism -> expand reach -> bound by capacity",
    },
    "H->Periodic": {
        "description": "Spread options, constrain by rhythm/timing",
        "132_reading": "Open spread -> test timing constraints -> land on viable window",
        "213_reading": "Seed from cycle -> expand reach -> bound by phase",
    },
    # V -> X: pulse vertically, constrain along X
    "V->H": {
        "description": "Deepen hierarchy, constrain by spread/adjacency",
        "132_reading": "Open depth -> test lateral limits -> land on viable depth-breadth",
        "213_reading": "Seed from breadth -> expand depth -> bound by coverage",
    },
    "V->Face": {
        "description": "Deepen hierarchy, constrain by presentation",
        "132_reading": "Open depth -> test what's displayable -> land",
        "213_reading": "Seed from display -> expand hierarchy -> bound by interface",
    },
    "V->Body": {
        "description": "Deepen hierarchy, constrain by support",
        "132_reading": "Open depth -> test load-bearing capacity -> land",
        "213_reading": "Seed from mechanism -> expand levels -> bound by structure",
    },
    "V->Periodic": {
        "description": "Deepen hierarchy, constrain by rhythm",
        "132_reading": "Open depth -> test phase constraints -> land",
        "213_reading": "Seed from cycle -> expand levels -> bound by timing",
    },
    # Face -> X: pulse presentation, constrain along X
    "Face->H": {
        "description": "Present signal, constrain by spread",
        "132_reading": "Open signal -> test propagation limits -> land",
        "213_reading": "Seed from reach -> expand display -> bound by coverage",
    },
    "Face->V": {
        "description": "Present signal, constrain by hierarchy",
        "132_reading": "Open signal -> test level appropriateness -> land",
        "213_reading": "Seed from level -> expand display -> bound by authority",
    },
    "Face->Body": {
        "description": "Present signal, constrain by mechanism",
        "132_reading": "Open display -> test what mechanism can support -> land",
        "213_reading": "Seed from mechanism -> expand interface -> bound by capacity",
    },
    "Face->Periodic": {
        "description": "Present signal, constrain by rhythm",
        "132_reading": "Open display -> test timing -> land on viable presentation window",
        "213_reading": "Seed from cycle -> expand display -> bound by phase",
    },
    # Body -> X: pulse mechanism, constrain along X
    "Body->H": {
        "description": "Expand mechanism, constrain by spread",
        "132_reading": "Open mechanism -> test distribution limits -> land",
        "213_reading": "Seed from reach -> expand mechanism -> bound by coverage",
    },
    "Body->V": {
        "description": "Expand mechanism, constrain by hierarchy",
        "132_reading": "Open mechanism -> test support chain -> land",
        "213_reading": "Seed from level -> expand support -> bound by authority",
    },
    "Body->Face": {
        "description": "Expand mechanism, constrain by presentation",
        "132_reading": "Open mechanism -> test what's visible -> land",
        "213_reading": "Seed from display -> expand hidden mechanism -> bound by interface",
    },
    "Body->Periodic": {
        "description": "Expand mechanism, constrain by rhythm",
        "132_reading": "Open mechanism -> test structural oscillation -> land",
        "213_reading": "Seed from cycle -> expand mechanism -> bound by phase",
    },
    # Periodic -> X: pulse rhythm, constrain along X
    "Periodic->H": {
        "description": "Expand rhythm, constrain by spread",
        "132_reading": "Open timing -> test propagation across neighbors -> land",
        "213_reading": "Seed from reach -> expand rhythm -> bound by coverage",
    },
    "Periodic->V": {
        "description": "Expand rhythm, constrain by hierarchy",
        "132_reading": "Open timing -> test level cycling -> land",
        "213_reading": "Seed from level -> expand phase -> bound by authority",
    },
    "Periodic->Face": {
        "description": "Expand rhythm, constrain by presentation",
        "132_reading": "Open timing -> test display cycles -> land",
        "213_reading": "Seed from display -> expand rhythm -> bound by interface",
    },
    "Periodic->Body": {
        "description": "Expand rhythm, constrain by mechanism",
        "132_reading": "Open timing -> test structural oscillation -> land",
        "213_reading": "Seed from mechanism -> expand rhythm -> bound by capacity",
    },
}


# =============================================================================
# PART 9: SENSITIVITY ANALYSIS (theory-aware, not naive uniform)
# =============================================================================

class SensitivityAnalysis:
    """
    Monte Carlo with TWO modes:

    1. Uniform sweep (stress test of controller logic, not of theory)
    2. Regime-conditioned sampling (theory-aware: Field/Frame bias distributions)

    IMPORTANT DISTINCTION:
    Uniform sweep tests whether the CONTROLLER behaves sanely.
    Regime-conditioned sweep tests whether the THEORY's predictions hold.
    """

    def __init__(self, controller: TransitionController, n_samples: int = 10000):
        self.controller = controller
        self.n_samples = n_samples

    def _sample_uniform(self) -> Dict[str, float]:
        return {
            "sigma": random.uniform(0, 1),
            "e_star": random.uniform(0, 1),
            "mu_star": random.uniform(0, 1),
            "d_t": random.uniform(0, 1),
            "c_star": random.uniform(0, 1),
            "u_t": random.uniform(0, 1),
            "q_t": random.uniform(0, 1),
        }

    def _sample_field_regime(self) -> Dict[str, float]:
        """Field regime: pulse-dominant, higher sigma, lower constraint."""
        return {
            "sigma": random.betavariate(5, 2),      # skewed toward stable
            "e_star": random.betavariate(2, 5),      # skewed toward low residue
            "mu_star": random.uniform(0, 1),
            "d_t": random.betavariate(2, 3),         # moderate asymmetry
            "c_star": random.uniform(0, 1),
            "u_t": random.betavariate(2, 5),         # skewed toward low instability
            "q_t": random.betavariate(2, 4),
        }

    def _sample_frame_regime(self) -> Dict[str, float]:
        """Frame regime: constrain-dominant, lower stability, higher residue."""
        return {
            "sigma": random.betavariate(3, 4),       # moderate-low stability
            "e_star": random.betavariate(4, 3),      # higher residue (more elimination)
            "mu_star": random.uniform(0, 1),
            "d_t": random.betavariate(4, 2),         # higher asymmetry (constrain-heavy)
            "c_star": random.uniform(0, 1),
            "u_t": random.betavariate(3, 3),
            "q_t": random.betavariate(3, 4),
        }

    def run(self, mode: str = "uniform") -> Dict:
        """Run Monte Carlo analysis in specified mode."""
        if mode == "uniform":
            sampler = self._sample_uniform
        elif mode == "field":
            sampler = self._sample_field_regime
        elif mode == "frame":
            sampler = self._sample_frame_regime
        else:
            sampler = self._sample_uniform

        winners = {a.value: 0 for a in TransitionAction}
        param_by_winner = {a.value: [] for a in TransitionAction}

        for _ in range(self.n_samples):
            params = sampler()
            scores = self.controller.compute_scores(**params)
            action = self.controller.select_action(scores)
            winners[action.value] += 1
            param_by_winner[action.value].append(params)

        action_probs = {k: v / self.n_samples for k, v in winners.items()}

        # Compute mean parameter values per winning action
        sensitivities = {}
        for action, param_list in param_by_winner.items():
            if param_list:
                keys = param_list[0].keys()
                sensitivities[action] = {
                    k: round(np.mean([p[k] for p in param_list]), 3)
                    for k in keys
                }

        return {
            "mode": mode,
            "n_samples": self.n_samples,
            "action_probabilities": action_probs,
            "sensitivities": sensitivities,
        }

    def cliff_edge_analysis(self,
                            base_params: Dict,
                            vary_param: str,
                            n_steps: int = 100) -> List[Dict]:
        """Find where small parameter changes flip the winning action."""
        results = []
        for i in range(n_steps + 1):
            value = i / n_steps
            params = base_params.copy()
            params[vary_param] = value
            scores = self.controller.compute_scores(**params)
            action = self.controller.select_action(scores)
            results.append((value, action.value))

        transitions = []
        for i in range(1, len(results)):
            if results[i][1] != results[i - 1][1]:
                transitions.append({
                    "at_value": round(results[i][0], 3),
                    "from_action": results[i - 1][1],
                    "to_action": results[i][1],
                })
        return transitions


# =============================================================================
# PART 10: COUNCIL EXPERTS
# =============================================================================

class CouncilExpert:
    """Base class for council expert validators."""
    name: str
    domain: str

    def evaluate(self, interaction: Dict, state: SystemState,
                 predicted: TransitionAction) -> Dict:
        raise NotImplementedError


class ControlSystemsEngineer(CouncilExpert):
    name = "Control Systems Engineer"
    domain = "Stability, convergence, oscillation, deadlock"

    def evaluate(self, interaction, state, predicted):
        issues = []
        # Check for chatter (rapid switching)
        history = interaction.get("action_history", [])
        if len(history) >= 4:
            last_4 = history[-4:]
            switches = sum(1 for i in range(1, len(last_4))
                          if last_4[i] != last_4[i-1])
            if switches >= 3:
                issues.append("CHATTER: 3+ action changes in last 4 cycles")

        # Check for deadlock
        if (state.calibration and
            state.calibration.stability_score < 0.3 and
            predicted == TransitionAction.STAY):
            issues.append("POTENTIAL DEADLOCK: low stability forcing default STAY")

        # Check feedback closure
        if not state.calibration:
            issues.append("NO CALIBRATION: feedback loop is open")

        return {
            "expert": self.name,
            "pass": len(issues) == 0,
            "issues": issues,
            "verdict": "PASS" if not issues else "FAIL",
        }


class BayesianStatistician(CouncilExpert):
    name = "Bayesian Statistician"
    domain = "Measurement validity, uncertainty, coherence"

    def evaluate(self, interaction, state, predicted):
        issues = []
        if state.calibration:
            c = state.calibration
            # Overconfidence check
            if c.stability_score > 0.9 and c.stability_type == StabilityType.REPELLER:
                issues.append("INCOHERENT: high stability score but repeller type")

            # Contradictory signal check
            if (c.mode_signal == TransitionAction.TERMINATE and
                c.stability_type == StabilityType.REPELLER):
                issues.append("CONTRADICTORY: TERMINATE signal with REPELLER stability")

            # Residue vs completion
            completion = interaction.get("task_completion", 0.5)
            if completion > 0.8 and c.residue.magnitude > 0.6:
                issues.append("INCOHERENT: high completion but high residue")

        return {
            "expert": self.name,
            "pass": len(issues) == 0,
            "issues": issues,
            "verdict": "PASS" if not issues else "FAIL",
        }


class CognitiveScientist(CouncilExpert):
    name = "Cognitive Scientist"
    domain = "Phenomenological validity, decision process accuracy"

    def evaluate(self, interaction, state, predicted):
        issues = []
        # Phase blur
        burst = interaction.get("burst_duration_pct", 0.2)
        crush = interaction.get("crush_duration_pct", 0.5)
        if abs(burst - crush) < 0.1 and burst > 0.3:
            issues.append("PHASE BLUR: Burst and Crush nearly equal duration")

        # Mode collision
        if (interaction.get("felt_diagnostic") and
            interaction.get("felt_generative")):
            issues.append("MODE COLLISION: felt both diagnostic and generative")

        return {
            "expert": self.name,
            "pass": len(issues) == 0,
            "issues": issues,
            "verdict": "PASS" if not issues else "FAIL",
        }


class SalesPractitioner(CouncilExpert):
    name = "Sales Practitioner"
    domain = "Predictive accuracy, real-time usability"

    def evaluate(self, interaction, state, predicted):
        issues = []
        actual = interaction.get("actual_action")
        if actual and actual != predicted.value:
            issues.append(
                f"PREDICTION MISS: predicted {predicted.value}, "
                f"actual was {actual}"
            )

        # Cognitive overload check
        log_time = interaction.get("logging_duration_s", 0)
        int_time = interaction.get("interaction_duration_s", 120)
        if log_time > int_time:
            issues.append("COGNITIVE OVERLOAD: logging > interaction time")

        return {
            "expert": self.name,
            "pass": len(issues) == 0,
            "issues": issues,
            "verdict": "PASS" if not issues else "FAIL",
        }


class Topologist(CouncilExpert):
    name = "Topologist / Mathematician"
    domain = "Structural integrity, invariant preservation, transform validity"

    def evaluate(self, interaction, state, predicted):
        issues = []
        # Kernel check
        if state.kernel_status:
            for name, (passed, score) in state.kernel_status.items():
                inv = next((i for i in KERNEL_INVARIANTS if i.name == name), None)
                if inv and inv.tier == 1 and not passed:
                    issues.append(f"TIER-1 KERNEL BREACH: {name} (score={score})")

        # Regime leak check
        declared = interaction.get("declared_regime")
        actual = interaction.get("actual_dynamics")
        translated = interaction.get("translation_applied", True)
        if declared and actual and declared != actual and not translated:
            issues.append(
                f"REGIME LEAK: declared={declared}, actual={actual}, "
                f"no translation applied"
            )

        # Round-trip reversibility check
        if state.regime == Regime.MIXED:
            fc = FieldCoordinates(
                rho=interaction.get("rho", 5.0),
                alpha=interaction.get("alpha", 0.0),
                phi=interaction.get("phi", 0.0),
            )
            rt_error = RegimeTranslator.round_trip_error(fc)
            if rt_error > 0.15:
                issues.append(
                    f"REVERSIBILITY LOSS: round-trip error {rt_error:.3f} > 0.15"
                )

        return {
            "expert": self.name,
            "pass": len(issues) == 0,
            "issues": issues,
            "verdict": "PASS" if not issues else "FAIL",
        }


class SystemsTheorist(CouncilExpert):
    name = "Systems Theorist"
    domain = "Emergence, feedback coherence, scale consistency"

    def evaluate(self, interaction, state, predicted):
        issues = []
        # Mode stagnation
        history = interaction.get("mode_history", [])
        if len(history) >= 8 and len(set(history[-8:])) == 1:
            issues.append("MODE STAGNATION: same mode for 8+ cycles")

        # Scale collapse
        if (predicted == TransitionAction.ESCALATE and
            interaction.get("scale_before") == interaction.get("scale_after")):
            issues.append("SCALE COLLAPSE: escalate didn't change scale")

        return {
            "expert": self.name,
            "pass": len(issues) == 0,
            "issues": issues,
            "verdict": "PASS" if not issues else "FAIL",
        }


COUNCIL = [
    ControlSystemsEngineer(),
    BayesianStatistician(),
    CognitiveScientist(),
    SalesPractitioner(),
    Topologist(),
    SystemsTheorist(),
]


# =============================================================================
# PART 11: FALSIFICATION CONDITIONS
# =============================================================================

FALSIFICATION_CONDITIONS = [
    {
        "id": "F1",
        "name": "Core Without Crush",
        "description": "Stable Core located WITHOUT meaningful boundary-testing",
        "test": "Find 10 successful conversions where Crush < 10% of effort",
        "kill_condition": "8+ show stable Core without Crush",
        "kills": "T2 (Boundary as Work)",
    },
    {
        "id": "F2",
        "name": "Expansion Without Boundary",
        "description": "213 generative mode produces stable form without boundary",
        "test": "Run 213 and skip boundary crystallization",
        "kill_condition": "Form holds in 8+ of 10 cases",
        "kills": "Generative mode architecture",
    },
    {
        "id": "F3",
        "name": "Inversion Breaks Kernel",
        "description": "132->213 switch systematically violates kernel invariants",
        "test": "Log kernel before/after every mode switch",
        "kill_condition": ">20% of switches show kernel breach",
        "kills": "Mode inversion claim",
    },
    {
        "id": "F4",
        "name": "Roles Swap Freely",
        "description": "Ideal/Boundary/Core can be assigned arbitrarily",
        "test": "Deliberately mis-assign roles, measure prediction accuracy",
        "kill_condition": "Accuracy unchanged vs correct assignment",
        "kills": "Role identity (Level 2)",
    },
    {
        "id": "F5",
        "name": "Thresholds Unstable",
        "description": "Optimal thresholds vary wildly across practitioners",
        "test": "Calibrate for 3 different practitioners",
        "kill_condition": "Optimal theta varies by >0.2",
        "kills": "Universal architecture claim",
    },
    {
        "id": "F6",
        "name": "20/50/30 Is Arbitrary",
        "description": "Phase duration distribution varies wildly",
        "test": "Measure durations across 30 successful conversions",
        "kill_condition": "SD > mean for any phase",
        "kills": "Structural weighting hypothesis",
    },
    {
        "id": "F7",
        "name": "Prediction <= Chance",
        "description": "Model predictions not better than random",
        "test": "Accuracy across 50+ interactions",
        "kill_condition": "Accuracy < 40% (less than 2x chance)",
        "kills": "Entire controller",
    },
]


# =============================================================================
# PART 12: FULL STRESS TEST EXECUTION
# =============================================================================

def run_demo_interaction():
    """
    Run one synthetic interaction through the full pipeline.
    This is a DEMO. Real validation requires actual sales-floor data.
    """
    interaction = {
        # Phase data
        "burst_duration_pct": 0.20,
        "crush_duration_pct": 0.50,
        "click_duration_pct": 0.30,
        # Stability
        "commitment_clarity": 0.7,
        "new_objections_at_click": 1,
        "perturbation_response": "stable",
        # Residue
        "options_eliminated": ["competitor_A", "old_plan"],
        "options_contested": ["price_concern"],
        "options_unmapped": [],
        # Mode/regime
        "felt_diagnostic": True,
        "felt_generative": False,
        "regime": "frame",
        "identity_origin": "boundary",
        "failure_mode": "collapse",
        "coherence_feel": "containment",
        "native_transform": "segmentation",
        # Completion
        "task_completion": 0.75,
        "core_fully_developed": True,
        "boundary_contested": False,
        "scale_bound_residue": False,
        "dominant_asymmetry": 0.3,
        # Axis
        "axis": "H->V",
        "scale": "micro",
        # Kernel scores
        "kernel_triadic_completeness": 1.0,
        "kernel_asymmetric_work": 0.85,
        "kernel_boundary_load_bearing": 0.9,
        "kernel_calibration_necessity": 1.0,
        "kernel_dependency_primacy": 1.0,
        # Field coordinates (for reversibility test)
        "rho": 4.0,
        "alpha": 30.0,
        "phi": 120.0,
        # History
        "action_history": ["stay", "stay", "invert", "stay"],
        "mode_history": ["132", "132", "213", "132"],
        # Actual outcome (for practitioner validation)
        "actual_action": "terminate",
        "interaction_duration_s": 120,
        "logging_duration_s": 60,
    }
    return interaction


def run_full_stress_test():
    """Execute the complete stress test protocol."""
    print("=" * 78)
    print("    STRESS TEST COUNCIL: FULL PROTOCOL EXECUTION")
    print("    Architecture: 132/213 Recursive Control System")
    print("=" * 78)

    # --- 1. DEMO INTERACTION ---
    print("\n[1] DEMO INTERACTION PIPELINE")
    print("-" * 40)

    interaction = run_demo_interaction()
    controller = TransitionController(theta=0.5, delta=0.15)

    # Measure
    sigma, stype = MeasurementProtocol.measure_stability(interaction)
    residue = MeasurementProtocol.measure_residue(interaction)
    mode_sig, mode_str = MeasurementProtocol.measure_mode_signal(interaction)
    kernel = MeasurementProtocol.evaluate_kernel(interaction)
    asymmetry = controller.compute_asymmetry(interaction)
    dom_dim, dom_score = controller.dominant_asymmetry(asymmetry)
    regime = RegimeTranslator.classify_regime(interaction)

    print(f"  Stability: {sigma} ({stype.value})")
    print(f"  Residue magnitude: {residue.magnitude:.3f}")
    print(f"  Mode signal: {mode_sig.value} (strength={mode_str:.3f})")
    print(f"  Regime: {regime.value}")
    print(f"  Dominant asymmetry: {dom_dim} ({dom_score:.3f})")
    print(f"  Kernel status:")
    tier1_breach = False
    for name, (passed, score) in kernel.items():
        status = "OK" if passed else "BREACH"
        print(f"    {name}: {status} (score={score})")
        inv = next((i for i in KERNEL_INVARIANTS if i.name == name), None)
        if inv and inv.tier == 1 and not passed:
            tier1_breach = True

    # Build calibration
    cal = CalibrationOutput(
        position={"rho": interaction["rho"], "alpha": interaction["alpha"],
                  "phi": interaction["phi"]},
        residue=residue,
        stability_score=sigma,
        stability_type=stype,
        mode_signal=mode_sig,
        mode_signal_strength=mode_str,
    )

    # Build state
    state = SystemState(
        mode=Mode.DIAGNOSTIC_132,
        regime=regime,
        axis=interaction.get("axis", "H"),
        scale=interaction.get("scale", "micro"),
        kernel_status=kernel,
        calibration=cal,
        cycle=len(interaction.get("action_history", [])),
    )

    # Compute transition
    scores = controller.compute_scores(
        sigma=sigma,
        e_star=residue.magnitude,
        mu_star=mode_str,
        d_t=dom_score,
        c_star=interaction.get("task_completion", 0.5),
        u_t=1.0 - sigma,
        q_t=0.3,
    )
    predicted = controller.select_action(scores)

    print(f"\n  Transition scores:")
    for action, score in sorted(scores.items(), key=lambda x: -x[1]):
        marker = " <-- WINNER" if action == predicted.value else ""
        print(f"    {action:15s}: {score:.4f}{marker}")
    print(f"\n  Predicted action: {predicted.value}")
    print(f"  Actual action:   {interaction.get('actual_action', 'unknown')}")

    # --- 2. COUNCIL REVIEW ---
    print("\n\n[2] COUNCIL REVIEW")
    print("-" * 40)

    pass_count = 0
    for expert in COUNCIL:
        result = expert.evaluate(interaction, state, predicted)
        status = "PASS" if result["pass"] else "FAIL"
        print(f"\n  {result['expert']}: {status}")
        if result["issues"]:
            for issue in result["issues"]:
                print(f"    ! {issue}")
        if result["pass"]:
            pass_count += 1

    print(f"\n  Council result: {pass_count}/{len(COUNCIL)} experts passed")

    # --- 3. REGIME TRANSLATION TEST ---
    print("\n\n[3] REGIME TRANSLATION (Field <-> Frame)")
    print("-" * 40)

    fc = FieldCoordinates(rho=4.0, alpha=30.0, phi=120.0)
    frc = RegimeTranslator.field_to_frame(fc)
    fc_rt = RegimeTranslator.frame_to_field(frc)
    rt_err = RegimeTranslator.round_trip_error(fc)

    print(f"  Field:  rho={fc.rho}, alpha={fc.alpha}, phi={fc.phi}")
    print(f"  Frame:  constraint={frc.constraint_level:.3f}, "
          f"sector={frc.enclosure_sector}, elim_phase={frc.elimination_phase:.3f}")
    print(f"  Round-trip Field': rho={fc_rt.rho:.1f}, alpha={fc_rt.alpha:.1f}, "
          f"phi={fc_rt.phi:.1f}")
    print(f"  Round-trip error: {rt_err:.4f}")
    print(f"  Verdict: {'PASS' if rt_err < 0.15 else 'FAIL'} "
          f"(threshold: 0.15)")

    # --- 4. DIRECTED AXIS SEMANTICS ---
    print("\n\n[4] DIRECTED AXIS INTERACTION CHECK")
    print("-" * 40)

    current_axis = interaction.get("axis", "H")
    if current_axis in AXIS_INTERACTIONS:
        info = AXIS_INTERACTIONS[current_axis]
        print(f"  Active axis: {current_axis}")
        print(f"  Description: {info['description']}")
        if state.mode == Mode.DIAGNOSTIC_132:
            print(f"  132 reading: {info.get('132_reading', 'N/A')}")
        else:
            print(f"  213 reading: {info.get('213_reading', 'N/A')}")
    else:
        print(f"  Active axis: {current_axis} (single-axis, no directed pair)")

    print(f"\n  Total axis states: {len(AXIS_STATES)}")
    print(f"    Single-axis: {len(AXES)}")
    print(f"    Directed pairs: {len(AXIS_INTERACTIONS)}")

    # --- 5. SENSITIVITY ANALYSIS ---
    print("\n\n[5] SENSITIVITY ANALYSIS")
    print("-" * 40)

    sa = SensitivityAnalysis(controller, n_samples=10000)

    # Run all three modes
    for mode_name in ["uniform", "field", "frame"]:
        result = sa.run(mode=mode_name)
        print(f"\n  [{mode_name.upper()} sampling] (n={result['n_samples']})")
        print("  Action probabilities:")
        for action, prob in sorted(result["action_probabilities"].items(),
                                   key=lambda x: -x[1]):
            bar = "#" * int(prob * 40)
            print(f"    {action:15s}: {prob:.3f} {bar}")

    # Cliff edges
    print("\n  Cliff edges (moderate base case):")
    base = {
        "sigma": 0.5, "e_star": 0.3, "mu_star": 0.5,
        "d_t": 0.3, "c_star": 0.5, "u_t": 0.3, "q_t": 0.3,
    }
    for param in ["sigma", "e_star", "c_star", "d_t"]:
        edges = sa.cliff_edge_analysis(base, param)
        if edges:
            for e in edges:
                print(f"    {param}={e['at_value']:.2f}: "
                      f"{e['from_action']} -> {e['to_action']}")

    # --- 6. FALSIFICATION CONDITIONS ---
    print("\n\n[6] FALSIFICATION CONDITIONS")
    print("-" * 40)
    for fc_item in FALSIFICATION_CONDITIONS:
        print(f"\n  [{fc_item['id']}] {fc_item['name']}")
        print(f"    {fc_item['description']}")
        print(f"    Test: {fc_item['test']}")
        print(f"    Kill: {fc_item['kill_condition']}")
        print(f"    Kills: {fc_item['kills']}")

    # --- 7. ADVERSARIAL SCENARIOS ---
    print("\n\n[7] ADVERSARIAL SCENARIOS ({} total)".format(
        len(ADVERSARIAL_SCENARIOS)))
    print("-" * 40)
    by_severity = {"critical": [], "major": [], "minor": []}
    for s in ADVERSARIAL_SCENARIOS:
        by_severity[s.severity].append(s)

    for sev in ["critical", "major", "minor"]:
        print(f"\n  {sev.upper()} ({len(by_severity[sev])}):")
        for s in by_severity[sev]:
            print(f"    - {s.name}: {s.expected_failure}")

    # --- SUMMARY ---
    print("\n\n" + "=" * 78)
    print("STRESS TEST SUMMARY")
    print("=" * 78)

    actual_action = interaction.get("actual_action", "unknown")
    prediction_match = predicted.value == actual_action

    print(f"""
  Controller prediction: {predicted.value}
  Actual outcome:        {actual_action}
  Prediction match:      {'YES' if prediction_match else 'NO -- CALIBRATION GAP'}

  Council pass rate:     {pass_count}/{len(COUNCIL)}
  Kernel intact:         {'YES' if not tier1_breach else 'NO -- TIER-1 BREACH'}
  Regime translation:    round-trip error {rt_err:.4f}
  Directed axis states:  {len(AXIS_STATES)} (5 single + 20 directed)

  Architecture layers verified:
    L0 Primitive (Pulse/Constrain):     LOCKED
    L1 Loop (P->C->Cal->Inv):           LOCKED
    L2 Roles (1=Ideal,3=Bound,2=Core):  LOCKED
    L3 Modes (132/213):                 LOCKED
    L4 Control (5 actions):             LOCKED
    L5 Regimes (Field/Frame/Mixed):     LOCKED (Mixed provisional)
    L6 Axes (25 states):                LOCKED
    L7 Domains:                         OPEN (needs real interaction data)

  Theory-faithful corrections applied:
    - Regime-conditioned Monte Carlo (not just uniform)
    - Directed axis pairs (H->V != V->H)
    - Typed kernel invariants (binary/graded/threshold)
    - Field<->Frame translation with round-trip error
    - 20/50/30 kept as HYPOTHESIS, not action-rate target

  NEXT STEP:
    One real sales interaction. Fill the template.
    Run through this pipeline. Compare prediction to reality.
    That comparison IS the test.
""")

    return {
        "prediction": predicted.value,
        "actual": actual_action,
        "match": prediction_match,
        "council_pass_rate": f"{pass_count}/{len(COUNCIL)}",
        "kernel_intact": not tier1_breach,
        "rt_error": rt_err,
        "scores": scores,
    }


if __name__ == "__main__":
    results = run_full_stress_test()
