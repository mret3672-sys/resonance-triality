"""
STRESS TEST COUNCIL: Comprehensive Validation Protocol
=======================================================

This is not just code. This is the PLAN:

1. COUNCIL COMPOSITION - Who tests what, and why
2. ADVERSARIAL SCENARIOS - Edge cases designed to break the model
3. SENSITIVITY ANALYSIS - Which parameters are load-bearing
4. CALIBRATION PROTOCOL - How to tune thresholds empirically
5. FALSIFICATION CONDITIONS - What would kill the theory

The goal: determine if this architecture PREDICTS or merely DESCRIBES.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Callable
from enum import Enum
import json
from datetime import datetime
import random

# =============================================================================
# PART 1: COUNCIL COMPOSITION
# =============================================================================

COUNCIL_ROSTER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    STRESS TEST COUNCIL: EXPERT ROSTER                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  EXPERT 1: CONTROL SYSTEMS ENGINEER                                          ║
║  ─────────────────────────────────────                                        ║
║  Domain: Stability, convergence, oscillation, deadlock                       ║
║  Questions:                                                                  ║
║    • Does the transition logic avoid chatter (rapid switching)?              ║
║    • Are thresholds preventing spurious mode changes?                        ║
║    • Is there a stable attractor, or does state drift indefinitely?          ║
║    • Do feedback loops actually close, or is "calibration" decorative?       ║
║  Failure mode: System oscillates, deadlocks, or drifts without converging    ║
║                                                                              ║
║  EXPERT 2: BAYESIAN STATISTICIAN                                              ║
║  ─────────────────────────────────────                                        ║
║  Domain: Measurement validity, uncertainty quantification, coherence         ║
║  Questions:                                                                  ║
║    • Are the score components actually measurable in practice?               ║
║    • Is uncertainty propagated, or are point estimates overconfident?        ║
║    • Does calibration update beliefs coherently (no contradictions)?         ║
║    • Are the weights and thresholds derived or arbitrary?                    ║
║  Failure mode: Measurements are mushy, overconfident, or incoherent          ║
║                                                                              ║
║  EXPERT 3: COGNITIVE SCIENTIST                                                ║
║  ─────────────────────────────────────                                        ║
║  Domain: Phenomenological validity, decision process accuracy                ║
║  Questions:                                                                  ║
║    • Does the formal model match reported subjective experience?             ║
║    • Are phase transitions (Burst/Crush/Click) cognitively real?             ║
║    • Does the mode distinction (132/213) map to actual mental states?        ║
║    • Can practitioners reliably identify which phase they're in?             ║
║  Failure mode: Model is elegant but doesn't track actual cognition           ║
║                                                                              ║
║  EXPERT 4: SALES PRACTITIONER                                                 ║
║  ─────────────────────────────────────                                        ║
║  Domain: Practical validity, predictive accuracy, real-time usability        ║
║  Questions:                                                                  ║
║    • Did the predicted transition match what actually happened?              ║
║    • Could this be used in real-time without cognitive overload?             ║
║    • Does it improve outcomes vs. intuition alone?                           ║
║    • Is the logging overhead worth the insight gained?                       ║
║  Failure mode: Predictions wrong, too slow, or not actionable                ║
║                                                                              ║
║  EXPERT 5: TOPOLOGIST / MATHEMATICIAN                                         ║
║  ─────────────────────────────────────                                        ║
║  Domain: Structural integrity, invariant preservation, transform validity    ║
║  Questions:                                                                  ║
║    • Are the 5 kernel invariants actually preserved under transitions?       ║
║    • Is the 132↔213 inversion truly structure-preserving?                    ║
║    • Are regime boundaries (Field/Frame/Mixed) well-defined?                 ║
║    • Is the axis space correctly dimensioned (25 states, not 15)?            ║
║  Failure mode: Invariants violated, structure collapses under stress         ║
║                                                                              ║
║  EXPERT 6: SYSTEMS THEORIST                                                   ║
║  ─────────────────────────────────────                                        ║
║  Domain: Emergence, feedback coherence, scale consistency                    ║
║  Questions:                                                                  ║
║    • Do macro patterns actually emerge from micro transitions?               ║
║    • Is feedback closing loops or just accumulating logs?                    ║
║    • Does scale escalation preserve meaning across levels?                   ║
║    • Is the system learning or just recording?                               ║
║  Failure mode: No emergence, feedback doesn't close, scale is nominal        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# =============================================================================
# PART 2: ADVERSARIAL SCENARIOS
# =============================================================================

@dataclass
class AdversarialScenario:
    """A scenario designed to stress-test specific failure modes."""
    name: str
    description: str
    target_expert: str
    expected_failure: str
    parameters: Dict
    severity: str  # "critical", "major", "minor"


ADVERSARIAL_SCENARIOS = [
    # === CONTROL SYSTEMS FAILURES ===
    AdversarialScenario(
        name="Chatter Loop",
        description="Calibration oscillates between SWITCH and STAY every cycle",
        target_expert="Control Systems Engineer",
        expected_failure="Rapid mode switching without convergence",
        parameters={
            "stability_score": 0.5,  # Ambiguous
            "mode_signal_strength": 0.55,  # Just above threshold
            "residue_magnitude": 0.5,  # Moderate
            "cycles": 10
        },
        severity="critical"
    ),
    AdversarialScenario(
        name="Deadlock",
        description="All transition scores are below threshold, system freezes",
        target_expert="Control Systems Engineer",
        expected_failure="No action possible, permanent STAY",
        parameters={
            "stability_score": 0.3,
            "mode_signal_strength": 0.2,
            "task_completion": 0.2,
            "asymmetry_max": 0.2
        },
        severity="critical"
    ),

    # === BAYESIAN FAILURES ===
    AdversarialScenario(
        name="Overconfident Stability",
        description="Stability score 0.99 but interaction fails",
        target_expert="Bayesian Statistician",
        expected_failure="Overconfident measurement doesn't reflect reality",
        parameters={
            "stability_score": 0.99,
            "actual_conversion": False,
            "perturbation_response": "diverged"
        },
        severity="major"
    ),
    AdversarialScenario(
        name="Contradictory Signals",
        description="Mode signal says TERMINATE but stability is REPELLER",
        target_expert="Bayesian Statistician",
        expected_failure="Incoherent calibration bundle",
        parameters={
            "mode_signal": "terminate",
            "stability_type": "repeller",
            "stability_score": 0.2
        },
        severity="major"
    ),

    # === COGNITIVE FAILURES ===
    AdversarialScenario(
        name="Phase Blur",
        description="Practitioner cannot distinguish Burst from Crush",
        target_expert="Cognitive Scientist",
        expected_failure="Phases are theoretically distinct but experientially merged",
        parameters={
            "phase_clarity": 0.3,
            "burst_duration_pct": 0.45,
            "crush_duration_pct": 0.45
        },
        severity="major"
    ),
    AdversarialScenario(
        name="Mode Collision",
        description="Interaction feels both diagnostic AND generative",
        target_expert="Cognitive Scientist",
        expected_failure="132/213 distinction not phenomenologically real",
        parameters={
            "felt_diagnostic": True,
            "felt_generative": True,
            "mode_declared": "132"
        },
        severity="minor"
    ),

    # === PRACTICAL FAILURES ===
    AdversarialScenario(
        name="Prediction Miss",
        description="Model predicts STAY, reality demands SWITCH",
        target_expert="Sales Practitioner",
        expected_failure="Controller doesn't track actual decision",
        parameters={
            "predicted_action": "stay",
            "actual_action": "switch_mode",
            "outcome": "conversion"
        },
        severity="critical"
    ),
    AdversarialScenario(
        name="Cognitive Overload",
        description="Logging takes longer than interaction",
        target_expert="Sales Practitioner",
        expected_failure="Framework is theoretically valid but unusable",
        parameters={
            "interaction_duration_s": 120,
            "logging_duration_s": 180
        },
        severity="major"
    ),

    # === TOPOLOGICAL FAILURES ===
    AdversarialScenario(
        name="Kernel Breach",
        description="Transition preserves 4/5 invariants, violates one",
        target_expert="Topologist",
        expected_failure="Partial kernel failure - is this fatal or recoverable?",
        parameters={
            "kernel_triadic": True,
            "kernel_asymmetric": True,
            "kernel_boundary_load": False,  # BREACH
            "kernel_calibration": True,
            "kernel_dependency": True
        },
        severity="critical"
    ),
    AdversarialScenario(
        name="Regime Leak",
        description="Field logic applied to Frame-native event without translation",
        target_expert="Topologist",
        expected_failure="Regime mismatch produces garbage output",
        parameters={
            "declared_regime": "field",
            "actual_dynamics": "frame",
            "translation_applied": False
        },
        severity="major"
    ),

    # === SYSTEMS FAILURES ===
    AdversarialScenario(
        name="Mode Stagnation",
        description="System stays in 132 for 10+ cycles despite varied inputs",
        target_expert="Systems Theorist",
        expected_failure="Mode switching mechanism is broken or too conservative",
        parameters={
            "mode_history": ["132"] * 10,
            "input_variance": "high"
        },
        severity="major"
    ),
    AdversarialScenario(
        name="Scale Collapse",
        description="Escalate action doesn't change scale parameter",
        target_expert="Systems Theorist",
        expected_failure="Scale is nominal, not functional",
        parameters={
            "action_taken": "escalate",
            "scale_before": "micro",
            "scale_after": "micro"
        },
        severity="minor"
    ),
]


def print_scenarios():
    """Display all adversarial scenarios."""
    print("\n" + "="*78)
    print("ADVERSARIAL SCENARIOS: Designed to Break the Model")
    print("="*78)

    for i, scenario in enumerate(ADVERSARIAL_SCENARIOS, 1):
        print(f"\n[{i}] {scenario.name} ({scenario.severity.upper()})")
        print(f"    Target: {scenario.target_expert}")
        print(f"    Description: {scenario.description}")
        print(f"    Expected Failure: {scenario.expected_failure}")
        print(f"    Parameters: {scenario.parameters}")


# =============================================================================
# PART 3: SENSITIVITY ANALYSIS
# =============================================================================

class TransitionScoreSimulator:
    """
    Monte Carlo sensitivity analysis for transition thresholds.

    Questions answered:
    - Which parameters most affect the winning action?
    - What threshold values minimize prediction error?
    - Where are the cliff edges in parameter space?
    """

    def __init__(self, n_samples: int = 10000):
        self.n_samples = n_samples
        self.results = []

    def compute_scores(self,
                       sigma: float,      # stability
                       e_star: float,     # residue magnitude
                       mu_star: float,    # mode signal strength
                       d_t: float,        # dominant asymmetry
                       c_star: float,     # task completion
                       u_t: float,        # instability
                       q_t: float,        # scale structure
                       theta: float = 0.6,
                       delta: float = 0.15) -> Dict:
        """Compute all transition scores."""

        s_stay = sigma * (1 - e_star) * (1 - d_t)
        s_switch = mu_star * e_star * u_t
        s_invert = d_t * (1 - sigma)
        s_escalate = sigma * e_star * q_t
        s_terminate = sigma * (1 - e_star) * c_star

        scores = {
            'stay': s_stay,
            'switch': s_switch,
            'invert': s_invert,
            'escalate': s_escalate,
            'terminate': s_terminate
        }

        # Apply precedence with thresholds
        if s_terminate > theta and s_terminate > s_stay + delta:
            winner = 'terminate'
        elif s_escalate > theta and s_escalate > s_stay + delta:
            winner = 'escalate'
        elif s_switch > theta and s_switch > s_stay + delta:
            winner = 'switch'
        elif s_invert > s_stay + delta * 0.67:  # lower delta for invert
            winner = 'invert'
        else:
            winner = 'stay'

        return {**scores, 'winner': winner}

    def run_monte_carlo(self) -> Dict:
        """Run Monte Carlo simulation across parameter space."""

        winners = {'stay': 0, 'switch': 0, 'invert': 0, 'escalate': 0, 'terminate': 0}
        parameter_impacts = {
            'sigma': [], 'e_star': [], 'mu_star': [],
            'd_t': [], 'c_star': [], 'u_t': [], 'q_t': []
        }

        for _ in range(self.n_samples):
            # Sample parameters uniformly
            params = {
                'sigma': random.uniform(0, 1),
                'e_star': random.uniform(0, 1),
                'mu_star': random.uniform(0, 1),
                'd_t': random.uniform(0, 1),
                'c_star': random.uniform(0, 1),
                'u_t': random.uniform(0, 1),
                'q_t': random.uniform(0, 1)
            }

            result = self.compute_scores(**params)
            winners[result['winner']] += 1

            # Track parameter values by winner
            for param, value in params.items():
                parameter_impacts[param].append((value, result['winner']))

        # Compute action probabilities
        action_probs = {k: v/self.n_samples for k, v in winners.items()}

        # Compute parameter sensitivity (variance in winning action by parameter)
        sensitivities = {}
        for param, values in parameter_impacts.items():
            # Split by winner
            by_winner = {}
            for val, winner in values:
                if winner not in by_winner:
                    by_winner[winner] = []
                by_winner[winner].append(val)

            # Compute mean parameter value for each winning action
            param_means = {w: np.mean(vals) for w, vals in by_winner.items() if vals}
            sensitivities[param] = param_means

        return {
            'action_probabilities': action_probs,
            'sensitivities': sensitivities,
            'n_samples': self.n_samples
        }

    def find_optimal_thresholds(self,
                                 target_action_rates: Dict[str, float],
                                 n_iterations: int = 1000) -> Dict:
        """
        Find threshold values that produce desired action rates.

        target_action_rates: e.g., {'terminate': 0.15, 'stay': 0.40, ...}
        """

        best_theta = 0.6
        best_delta = 0.15
        best_error = float('inf')

        for _ in range(n_iterations):
            theta = random.uniform(0.3, 0.9)
            delta = random.uniform(0.05, 0.3)

            # Run mini Monte Carlo
            winners = {'stay': 0, 'switch': 0, 'invert': 0, 'escalate': 0, 'terminate': 0}
            for _ in range(1000):
                params = {
                    'sigma': random.uniform(0, 1),
                    'e_star': random.uniform(0, 1),
                    'mu_star': random.uniform(0, 1),
                    'd_t': random.uniform(0, 1),
                    'c_star': random.uniform(0, 1),
                    'u_t': random.uniform(0, 1),
                    'q_t': random.uniform(0, 1),
                    'theta': theta,
                    'delta': delta
                }
                result = self.compute_scores(**params)
                winners[result['winner']] += 1

            action_rates = {k: v/1000 for k, v in winners.items()}

            # Compute error against targets
            error = sum((action_rates.get(k, 0) - v)**2
                       for k, v in target_action_rates.items())

            if error < best_error:
                best_error = error
                best_theta = theta
                best_delta = delta

        return {
            'optimal_theta': round(best_theta, 3),
            'optimal_delta': round(best_delta, 3),
            'error': round(best_error, 4)
        }

    def cliff_edge_analysis(self,
                            base_params: Dict,
                            vary_param: str,
                            n_steps: int = 100) -> List[Tuple[float, str]]:
        """
        Find where small parameter changes flip the winning action.
        These are the "cliff edges" where the model is most sensitive.
        """

        results = []
        for i in range(n_steps + 1):
            value = i / n_steps
            params = base_params.copy()
            params[vary_param] = value
            result = self.compute_scores(**params)
            results.append((value, result['winner']))

        # Find transition points
        transitions = []
        for i in range(1, len(results)):
            if results[i][1] != results[i-1][1]:
                transitions.append({
                    'at_value': results[i][0],
                    'from_action': results[i-1][1],
                    'to_action': results[i][1]
                })

        return transitions


def run_sensitivity_analysis():
    """Run full sensitivity analysis and report."""

    print("\n" + "="*78)
    print("SENSITIVITY ANALYSIS: Parameter Impact on Transitions")
    print("="*78)

    simulator = TransitionScoreSimulator(n_samples=10000)

    # Monte Carlo
    print("\n[1] MONTE CARLO ANALYSIS (n=10,000)")
    print("-" * 40)
    mc_results = simulator.run_monte_carlo()

    print("\nAction Probabilities (uniform parameter sampling):")
    for action, prob in sorted(mc_results['action_probabilities'].items(),
                               key=lambda x: -x[1]):
        bar = "█" * int(prob * 50)
        print(f"  {action:12s}: {prob:.3f} {bar}")

    print("\nParameter Sensitivities (mean value by winning action):")
    for param, means in mc_results['sensitivities'].items():
        print(f"\n  {param}:")
        for action, mean in sorted(means.items(), key=lambda x: -x[1]):
            print(f"    {action:12s}: {mean:.3f}")

    # Threshold optimization
    print("\n\n[2] THRESHOLD OPTIMIZATION")
    print("-" * 40)

    # Target: based on 20/50/30 hypothesis (Crush-heavy)
    # Translate to actions: moderate terminate, low switch, some invert
    targets = {
        'stay': 0.35,
        'terminate': 0.25,
        'invert': 0.15,
        'switch': 0.15,
        'escalate': 0.10
    }

    print(f"Target action rates: {targets}")
    optimal = simulator.find_optimal_thresholds(targets)
    print(f"\nOptimal thresholds found:")
    print(f"  θ_switch = {optimal['optimal_theta']}")
    print(f"  Δ_margin = {optimal['optimal_delta']}")
    print(f"  Fitting error = {optimal['error']}")

    # Cliff edge analysis
    print("\n\n[3] CLIFF EDGE ANALYSIS")
    print("-" * 40)
    print("Finding where small changes flip the winning action...\n")

    # Base case: moderate everything
    base_params = {
        'sigma': 0.5,
        'e_star': 0.3,
        'mu_star': 0.5,
        'd_t': 0.3,
        'c_star': 0.5,
        'u_t': 0.3,
        'q_t': 0.3
    }

    for param in ['sigma', 'e_star', 'c_star', 'd_t']:
        transitions = simulator.cliff_edge_analysis(base_params, param)
        if transitions:
            print(f"  {param}:")
            for t in transitions:
                print(f"    At {param}={t['at_value']:.2f}: "
                      f"{t['from_action']} → {t['to_action']}")
        else:
            print(f"  {param}: No transitions (stable)")

    return mc_results, optimal


# =============================================================================
# PART 4: CALIBRATION PROTOCOL
# =============================================================================

CALIBRATION_PROTOCOL = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EMPIRICAL CALIBRATION PROTOCOL                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PHASE 1: BASELINE COLLECTION (n=20 interactions)                            ║
║  ─────────────────────────────────────────────────                            ║
║  1. Run 132 Protocol on sales floor as usual                                 ║
║  2. Fill interaction log template IMMEDIATELY after                          ║
║  3. Note predicted action vs actual action taken                             ║
║  4. Record conversion outcome                                                ║
║                                                                              ║
║  OUTPUT: Raw data with prediction error rate                                 ║
║                                                                              ║
║  PHASE 2: THRESHOLD TUNING (iterative)                                       ║
║  ─────────────────────────────────────────────────                            ║
║  1. Compute prediction accuracy for current thresholds                       ║
║  2. Identify systematic errors:                                              ║
║     - "Predicted STAY but should have TERMINATED" → lower θ_terminate        ║
║     - "Predicted SWITCH but should have STAYED" → raise θ_switch             ║
║  3. Adjust thresholds by 0.05 increments                                     ║
║  4. Re-run next 10 interactions                                              ║
║  5. Repeat until prediction accuracy > 70%                                   ║
║                                                                              ║
║  PHASE 3: CROSS-VALIDATION                                                   ║
║  ─────────────────────────────────────────────────                            ║
║  1. Hold out 5 interactions from tuning                                      ║
║  2. Test tuned thresholds on held-out set                                    ║
║  3. If accuracy drops > 15%, thresholds are overfit                          ║
║  4. If accuracy holds, thresholds are validated                              ║
║                                                                              ║
║  PHASE 4: STRESS TEST COUNCIL REVIEW                                         ║
║  ─────────────────────────────────────────────────                            ║
║  1. Run all logged interactions through council                              ║
║  2. Aggregate expert verdicts                                                ║
║  3. Identify systematic failures by expert domain                            ║
║  4. Prioritize fixes: Critical > Major > Minor                               ║
║                                                                              ║
║  ACCEPTANCE CRITERIA                                                         ║
║  ─────────────────────────────────────────────────                            ║
║  ✓ Prediction accuracy > 70%                                                 ║
║  ✓ No critical adversarial scenario failures                                 ║
║  ✓ Council pass rate > 5/6 experts                                           ║
║  ✓ Kernel preserved in > 95% of transitions                                  ║
║  ✓ Cross-validation accuracy within 15% of tuning accuracy                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


# =============================================================================
# PART 5: FALSIFICATION CONDITIONS
# =============================================================================

FALSIFICATION_CONDITIONS = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    FALSIFICATION CONDITIONS                                  ║
║                    (What Would Kill This Theory)                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  F1: CORE WITHOUT CRUSH                                                      ║
║  ─────────────────────────────────────                                        ║
║  If a stable Core can be reliably located WITHOUT meaningful boundary-       ║
║  testing (Crush phase < 10% of effort), then T2 (Boundary as Work) fails.    ║
║                                                                              ║
║  Test: Find 10 successful conversions where Crush was minimal.               ║
║  Kill condition: 8+ of them show stable Core without Crush.                  ║
║                                                                              ║
║  F2: EXPANSION WITHOUT BOUNDARY                                              ║
║  ─────────────────────────────────────                                        ║
║  If 213 generative mode can produce stable form WITHOUT eventual boundary    ║
║  stabilization, then the architecture is incomplete.                         ║
║                                                                              ║
║  Test: Run 213 mode and skip boundary crystallization.                       ║
║  Kill condition: Form holds anyway in 8+ of 10 cases.                        ║
║                                                                              ║
║  F3: INVERSION BREAKS KERNEL                                                 ║
║  ─────────────────────────────────────                                        ║
║  If 132→213 inversion systematically violates kernel invariants (not just    ║
║  occasionally), then the modes are not truly inverse.                        ║
║                                                                              ║
║  Test: Log kernel status before and after every mode switch.                 ║
║  Kill condition: > 20% of switches show kernel breach.                       ║
║                                                                              ║
║  F4: ROLES SWAP FREELY                                                       ║
║  ─────────────────────────────────────                                        ║
║  If Ideal, Boundary, and Core can be assigned arbitrarily to any phase       ║
║  without predictive cost, then the roles are nominal, not functional.        ║
║                                                                              ║
║  Test: Deliberately mis-assign roles. Measure prediction accuracy.           ║
║  Kill condition: Accuracy unchanged vs correct assignment.                   ║
║                                                                              ║
║  F5: THRESHOLDS UNSTABLE                                                     ║
║  ─────────────────────────────────────                                        ║
║  If optimal thresholds vary wildly across practitioners or contexts,         ║
║  then the architecture is practitioner-dependent, not universal.             ║
║                                                                              ║
║  Test: Calibrate thresholds for 3 different practitioners.                   ║
║  Kill condition: Optimal θ varies by > 0.2 across practitioners.             ║
║                                                                              ║
║  F6: 20/50/30 IS ARBITRARY                                                   ║
║  ─────────────────────────────────────                                        ║
║  If the Burst/Crush/Click time distribution varies wildly across successful  ║
║  interactions, then the weighting is contingent, not structural.             ║
║                                                                              ║
║  Test: Measure actual phase durations across 30 successful conversions.      ║
║  Kill condition: Standard deviation > mean for any phase.                    ║
║                                                                              ║
║  F7: PREDICTION ≤ CHANCE                                                     ║
║  ─────────────────────────────────────                                        ║
║  If the model's action predictions are not significantly better than         ║
║  random (5 actions → 20% baseline), the controller adds no value.            ║
║                                                                              ║
║  Test: Compute prediction accuracy across 50+ interactions.                  ║
║  Kill condition: Accuracy < 40% (i.e., less than 2x chance).                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


# =============================================================================
# PART 6: MEASUREMENT OPERATIONALIZATION
# =============================================================================

@dataclass
class MeasurementProtocol:
    """
    How to actually measure each score component.
    This is the SENSOR LAYER that was missing.
    """

    @staticmethod
    def measure_stability(interaction: Dict) -> Tuple[float, str]:
        """
        Measure stability score (σ_t) from interaction data.

        Inputs:
        - Customer verbal/nonverbal signals at Click
        - Response to minor perturbation (e.g., mentioning alternative)
        - Clarity of commitment

        Returns: (score 0-1, type: attractor/saddle/repeller)
        """
        signals = []

        # Commitment clarity (0-1)
        commitment = interaction.get('commitment_clarity', 0.5)
        signals.append(commitment)

        # Objection absence (0-1, inverse of new objections at Click)
        new_objections = interaction.get('new_objections_at_click', 0)
        objection_absence = max(0, 1 - new_objections * 0.3)
        signals.append(objection_absence)

        # Perturbation response (did mentioning alternative shake them?)
        perturbation = interaction.get('perturbation_response', 'neutral')
        perturbation_scores = {
            'strengthened': 1.0,  # Perturbation made them MORE committed
            'stable': 0.8,
            'neutral': 0.5,
            'wavered': 0.3,
            'abandoned': 0.0
        }
        signals.append(perturbation_scores.get(perturbation, 0.5))

        score = np.mean(signals)

        # Classify type
        if score > 0.7:
            stability_type = 'attractor'
        elif score > 0.4:
            stability_type = 'saddle'
        else:
            stability_type = 'repeller'

        return (round(score, 2), stability_type)

    @staticmethod
    def measure_residue(interaction: Dict) -> Tuple[float, Dict]:
        """
        Measure residue magnitude (e_t*) from interaction data.

        Inputs:
        - Options explicitly eliminated during Crush
        - Options still contested at Click
        - Questions/aspects that remained unmapped

        Returns: (magnitude 0-1, structured residue dict)
        """
        eliminated = interaction.get('options_eliminated', [])
        contested = interaction.get('options_contested', [])
        unmapped = interaction.get('options_unmapped', [])

        # Weighted sum: eliminated is good, contested/unmapped is debt
        total = len(eliminated) + len(contested) + len(unmapped)
        if total == 0:
            return (0.0, {'eliminated': [], 'contested': [], 'unmapped': []})

        # Low magnitude is good (clean elimination)
        # High magnitude means lots of unresolved stuff
        weighted = len(eliminated)*0.1 + len(contested)*0.5 + len(unmapped)*0.8
        magnitude = min(1.0, weighted / max(total, 1))

        return (round(magnitude, 2), {
            'eliminated': eliminated,
            'contested': contested,
            'unmapped': unmapped
        })

    @staticmethod
    def measure_mode_signal(interaction: Dict) -> Tuple[str, float]:
        """
        Measure mode signal (μ_t) from interaction outcome.

        Logic:
        - If Core is stable and task complete → TERMINATE
        - If Core is real but underdeveloped → SWITCH to 213
        - If Boundary hit resistance that needs retesting → SWITCH to 132
        - If one dimension dominated unnaturally → INVERT
        - If local stable but larger pattern active → ESCALATE

        Returns: (signal, strength 0-1)
        """
        stability = interaction.get('stability_score', 0.5)
        completion = interaction.get('task_completion', 0.5)
        core_developed = interaction.get('core_fully_developed', True)
        boundary_contested = interaction.get('boundary_contested', False)
        scale_residue = interaction.get('scale_bound_residue', False)
        asymmetry = interaction.get('dominant_asymmetry', 0.3)

        # Decision logic
        if stability > 0.7 and completion > 0.7:
            return ('terminate', min(stability, completion))

        if not core_developed and stability > 0.5:
            # Core exists but needs expansion
            return ('switch', 0.6 + (1 - completion) * 0.3)

        if boundary_contested:
            return ('switch', 0.5 + stability * 0.3)

        if scale_residue and stability > 0.6:
            return ('escalate', stability * 0.8)

        if asymmetry > 0.6:
            return ('invert', asymmetry)

        return ('stay', stability * (1 - asymmetry))

    @staticmethod
    def measure_asymmetry(interaction: Dict) -> Dict[str, float]:
        """
        Measure asymmetry vector from interaction dynamics.

        Returns: dict with direction, mode, regime, axis, scale scores
        """
        # Direction asymmetry: was it pulse-heavy or constrain-heavy?
        burst_pct = interaction.get('burst_duration_pct', 0.2)
        crush_pct = interaction.get('crush_duration_pct', 0.5)
        direction = abs(burst_pct - crush_pct) / max(burst_pct + crush_pct, 0.01)

        # Mode asymmetry: did it feel strongly 132 or 213?
        felt_132 = 1.0 if interaction.get('felt_diagnostic', False) else 0.0
        felt_213 = 1.0 if interaction.get('felt_generative', False) else 0.0
        mode = abs(felt_132 - felt_213)

        # Regime asymmetry: Field vs Frame dominance
        regime_declared = interaction.get('regime', 'mixed')
        regime_scores = {'field': 0.8, 'frame': 0.8, 'mixed': 0.3}
        regime = regime_scores.get(regime_declared, 0.5)

        # Axis asymmetry: single vs cross-axis
        axis = interaction.get('axis', 'H')
        axis_score = 0.3 if '→' in str(axis) else 0.7

        # Scale asymmetry: stuck at one scale?
        scale = interaction.get('scale', 'micro')
        scale_scores = {'micro': 0.7, 'meso': 0.3, 'macro': 0.7}
        scale_asym = scale_scores.get(scale, 0.5)

        return {
            'direction': round(direction, 2),
            'mode': round(mode, 2),
            'regime': round(regime, 2),
            'axis': round(axis_score, 2),
            'scale': round(scale_asym, 2)
        }


# =============================================================================
# PART 7: FULL STRESS TEST EXECUTION
# =============================================================================

def run_full_stress_test():
    """Execute the complete stress test protocol."""

    print("\n" + "="*78)
    print("       STRESS TEST COUNCIL: FULL PROTOCOL EXECUTION")
    print("="*78)

    # 1. Council Roster
    print(COUNCIL_ROSTER)

    # 2. Adversarial Scenarios
    print_scenarios()

    # 3. Sensitivity Analysis
    mc_results, optimal = run_sensitivity_analysis()

    # 4. Calibration Protocol
    print(CALIBRATION_PROTOCOL)

    # 5. Falsification Conditions
    print(FALSIFICATION_CONDITIONS)

    # 6. Summary
    print("\n" + "="*78)
    print("STRESS TEST SUMMARY")
    print("="*78)

    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║  WHAT WE NOW HAVE:                                                         ║
║  ─────────────────                                                          ║
║  ✓ 6 expert validators with specific domains and failure modes             ║
║  ✓ 12 adversarial scenarios designed to break the model                    ║
║  ✓ Monte Carlo sensitivity analysis with 10,000 samples                    ║
║  ✓ Threshold optimization protocol                                         ║
║  ✓ Cliff edge detection for parameter sensitivity                          ║
║  ✓ Measurement operationalization for all score components                 ║
║  ✓ 7 explicit falsification conditions                                     ║
║  ✓ Calibration protocol with acceptance criteria                           ║
║                                                                            ║
║  WHAT WE STILL NEED:                                                       ║
║  ─────────────────                                                          ║
║  → ONE REAL INTERACTION, fully instrumented, with actual numbers           ║
║  → Run through the measurement functions                                   ║
║  → Compute transition scores                                               ║
║  → Check if predicted action matches reality                               ║
║  → Submit to council for verdict                                           ║
║                                                                            ║
║  THE QUESTION:                                                             ║
║  ─────────────────                                                          ║
║  Does the controller track reality, or just sound like it should?          ║
║                                                                            ║
║  THE ANSWER:                                                               ║
║  ─────────────────                                                          ║
║  Run the next sales floor interaction through this system.                 ║
║  Fill the template. Compute the scores. Compare to what happened.          ║
║  That comparison IS the test.                                              ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

    return {
        'monte_carlo': mc_results,
        'optimal_thresholds': optimal,
        'n_scenarios': len(ADVERSARIAL_SCENARIOS),
        'n_experts': 6,
        'n_falsifiers': 7
    }


if __name__ == "__main__":
    results = run_full_stress_test()

    print("\n" + "-"*78)
    print("EXECUTION COMPLETE")
    print("-"*78)
    print(f"Monte Carlo samples: {results['monte_carlo']['n_samples']}")
    print(f"Optimal θ: {results['optimal_thresholds']['optimal_theta']}")
    print(f"Optimal Δ: {results['optimal_thresholds']['optimal_delta']}")
    print(f"Adversarial scenarios: {results['n_scenarios']}")
    print(f"Council experts: {results['n_experts']}")
    print(f"Falsification conditions: {results['n_falsifiers']}")
