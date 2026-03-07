# TECHNICAL IMPLEMENTATION GUIDE
## For Any Future Claude Instance Working on This Codebase

**Version**: 0.3 (post-parallel-margins analysis)
**Date**: 2026-03-07
**Branch**: claude/parallel-margins-analysis-joH1R
**Status**: Controller implemented. Sensors deployed. Awaiting first real interaction data.

---

## READ THIS FIRST

This document exists because the theory behind this codebase is dense, recursive, and developed across multiple AI conversations. A future Claude instance encountering this repo will see Python code, markdown documents, and mathematical notation without understanding *why* each piece exists or *how* they connect.

This document makes that impossible.

It is organized in three sections:
1. **What the theory actually claims** (the ontology)
2. **What the code actually does** (the implementation)
3. **Where the gaps are** (the honest debt ledger)

Do not skip sections. Do not summarize. Read linearly.

---

# SECTION 1: THE THEORY

## 1.1 The Origin

James (mret3672-sys) is a telecommunications sales practitioner who discovered structural patterns in human decision-making through thousands of real interactions. He claims these patterns are *discovered structures* in reality, not invented techniques. This distinction matters because it means the framework should be falsifiable -- if the patterns are real, they should survive stress-testing; if invented, they would only survive within their creator's interpretive lens.

The original document (`01_Resonance_Triality.docx`) was 28 MB, 20,410 paragraphs, 1.1M characters. It was compressed into `RESONANCE_TRIALITY_COMPLETE.md` at ~50 KB with ~85% information preservation.

## 1.2 The Tier -1 Axiom (Bedrock)

Everything in this system derives from one claim:

> Communication is gravitational resonance between planetary systems (bodies), where syllables are quantum time units, intonation is spacetime curvature, and the timeless listener becomes the gravitational center.

This is the axiom that cannot be compressed further. All other frameworks are instances of it.

**Six components:**
1. **Syllables = discrete time quanta** (perception is stepwise, not continuous)
2. **Intonation = gravity wells** (emphasis creates attentional mass)
3. **Bodies = solar systems** (Mind/Heart/Shadow alignment between people)
4. **Timeless listener = gravitational center** (the one who exits reaction mode becomes the attractor)
5. **Words = fusion/fission events** (compression releases insight; expansion opens possibility)
6. **Plasma state = optimal communication** (ionized, responsive, conducting)

## 1.3 The 132 Protocol (Primary Operational Framework)

This is the most load-bearing framework in the system. It describes a three-phase influence sequence used in sales interactions but claimed to be isomorphic across many domains.

**132 is a chord progression, not a sequence.** Like C(1)-E(3)-C'(2) in music. Tension-resolution, not linear.

| Phase | Name | Duration | Phonetics | Pressure Effect | Function |
|-------|------|----------|-----------|-----------------|----------|
| 1 | BURST | 15-20s | 70% vowels | -40 dP (drops) | Expand possibility space |
| 3 | CRUSH | 8-10s | 65% consonants | +25 dP (rises) | Test boundary, ground in reality |
| 2 | CLICK | 5-8s | 50/50 balanced | 0 dP (equilibrium) | Crystallize decision |

**Why 1-3-2 and not 1-2-3:**
- 1-2-3 is linear escalation (boring, no tension)
- 3-2-1 starts with pain (triggers defense)
- 1-3-2 is tension-resolution: open, challenge, resolve

**The empirically observed weighting is 20/50/30:**
- Burst: 20% of the work
- Crush: 50% of the work (the "heavy lifting")
- Click: 30% of the work

Whether this weighting is structural (inherent to triangulation) or contingent (specific to sales) is an OPEN QUESTION. This is flagged as falsification condition F6.

## 1.4 The HP-12 Pressure Lattice

A 12-point scale for detecting customer decision-states.

```
Pressure = Decision_Resistance x Boundary_Distance
```

| Zone | Levels | Breath Rate | Protocol |
|------|--------|-------------|----------|
| High Pressure | HP-12 to HP-10 | >0.4 Hz | BURST first (never CRUSH here) |
| Med-High | HP-9 to HP-7 | 0.28-0.35 Hz | Careful CRUSH |
| Sweet Spot | HP-6 | ~0.27 Hz | CLICK immediately |
| Med-Low | HP-5 to HP-4 | 0.23-0.25 Hz | Light CRUSH + CLICK |
| Low Pressure | LP-3 to LP-1 | <0.2 Hz | CLICK only |

**Critical rules (never violate):**
- Never CRUSH at HP-10+ (triggers defensive response)
- At HP-6, CLICK immediately (window closes fast)
- At LP-1, don't sell harder (they're already ready)

**Detection priority:** Breath rate > Shoulder tension > Vocal quality > Eye movement > Posture > Verbal engagement

## 1.5 Thermodynamic Phase States

Mental states mapped to thermodynamic phases:

| State | Analog | HP Level | Intervention |
|-------|--------|----------|--------------|
| FROZEN | Ice | HP-10+ | BURST (apply energy to melt) |
| MELTING | Water | HP-7 to HP-5 | Optimal -- light CRUSH then CLICK |
| VIBRATING | Steam under pressure | HP-8 oscillating to HP-6 | CRUSH (provide structure) |
| TRIPLE POINT | Phase coexistence | HP-6 exactly | CLICK immediately |

**TRIPLE POINT is the target.** All states are accessible. Execute CLICK. Do not disturb equilibrium.

## 1.6 The Utility Equation

```
U = (Relief x Momentum x Gravity) / (Cost x Pressure x t) x Phi
```

Where Phi = 1.618 (golden ratio).

Decision thresholds:
- U > 7: Execute CLICK immediately
- U = 5-7: Light CRUSH then CLICK
- U = 3-5: Address objections
- U < 3: Wrong fit, don't force

## 1.7 Spiral Breathing (4-7-8)

```
Inhale(4) : Hold(7) : Exhale(8)
```

Maps to 132: Inhale=BURST, Hold=CRUSH, Exhale=CLICK. Same pattern at different scales.

## 1.8 Epistemic Foundation (A-Series Axioms)

Seven axioms governing how truth-claims are evaluated:

| Axiom | Statement |
|-------|-----------|
| A0 | Truth = Correspondence to reality |
| A1 | Newer evidence overwrites older |
| A2 | Similarity does not equal Truth (pattern is not proof) |
| A3 | 5-tier justification hierarchy |
| A4 | Foundationalism (trace to basics, no circular reasoning) |
| A5 | No epistemic luck (causal links required) |
| A6 | Fallibilism (confidence scores, not binary truth) |

**Confidence scoring:**
```
0.95-1.00: Extremely confident (Tier 1)
0.85-0.94: Highly confident (Tier 2)
0.70-0.84: Confident (Tier 3)
0.50-0.69: Uncertain
< 0.50:    Unreliable (suspend judgment)
```

---

# SECTION 2: THE PARALLEL MARGINS ANALYSIS (What Happened in March 2026)

This is the development that produced the code in `validation/`. Understanding this is critical because it transformed the theory from a descriptive framework into a testable control system.

## 2.1 The Discovery Sequence

The parallel margins analysis was a multi-session dialectic involving James, Claude, Perplexity, and ChatGPT. The sequence of discoveries was:

### Step 1: Coherence is not a single number

Perplexity proposed: `C = sum(w_i * I_i) / sum(w_i)` -- weighted invariant survival.

This was REJECTED as regime-blind. A system can preserve many invariants while still:
- drifting out of phase (phase decoherence)
- losing reversible correspondence (projection failure)

The stronger claim: coherence = identity preservation across parallel margins.

### Step 2: Field/Frame Duality

Two fundamentally different regimes for identity:

| | Field Regime | Frame Regime |
|--|-------------|-------------|
| Identity source | Center relation | Boundary relation |
| Primary continuity | Phase / gradient | Edge / adjacency |
| Failure mode | Decoherence / drift | Collapse / fracture |
| Core invariant | Orbital relation | Structural enclosure |
| Transform class | Resonance / projection | Support / segmentation |

**This is the single most important discovery from the analysis.** It revealed that the framework had a "center privilege bias" -- it spoke spiral/Field more fluently than cube/Frame. The 132 Protocol is actually Frame-dominant (elimination, boundary-testing), while the S=(rho,alpha,phi) coordinate system is Field-native.

**Bug identified:** Field and Frame were being treated interchangeably. They are not. Translation between them is costly and must be declared.

### Step 3: Axiom Compression

The entire architecture was compressed into one primitive loop:

```
Pulse -> Constrain -> Calibrate -> Invert
```

This is not a single atom. It is the **minimal generative loop.**

- Pulse = expand, emit, open
- Constrain = test, eliminate, bound
- Calibrate = measure what survived
- Invert = flip dominant asymmetry for next cycle

### Step 4: 132/213 as Inverse Dependency Modes

The 132 Protocol is one traversal of the loop. Its sovereign inverse is 213:

| | 132 Diagnostic | 213 Generative |
|--|---------------|----------------|
| Entry | Ideal (1) | Core (2) |
| Main question | What survives pressure? | What can this seed become? |
| Core meaning | Remainder after elimination | Seed for expansion |
| Boundary meaning | Elimination surface | Stabilizing envelope |
| Work feel | Testing / filtering | Building / shaping |

**Switching law (endogenous, not arbitrary):**
- 132 -> 213: when discovered Core is real but underdeveloped (remainder becomes seed)
- 213 -> 132: when expansion hits resistance (generated form needs pressure-testing)

### Step 5: The Transition Controller

The system was formalized as a state machine:

**State:** `X_t = (mode, regime, axis, scale, kernel_status, calibration)`

**Calibration output:** `c_t = (position, residue, stability, mode_signal)`

Where:
- position = where in coordinate space we landed
- residue = what was eliminated / contested / unmapped (NOT trash -- logged debt)
- stability = attractor / saddle / repeller (typed, not just scored)
- mode_signal = stay / switch / invert / escalate / terminate

**Transition scores:**
```
S_stay      = sigma * (1 - e*) * (1 - d_t)
S_switch    = mu*   * e*       * u_t
S_invert    = d_t   * (1 - sigma)
S_escalate  = sigma * e*       * q_t
S_terminate = sigma * (1 - e*) * c*
```

Where:
- sigma = stability score [0,1]
- e* = residue magnitude [0,1] (high = lots unresolved)
- mu* = mode signal strength [0,1]
- d_t = dominant asymmetry score [0,1]
- c* = task completion [0,1]
- u_t = instability [0,1]
- q_t = scale structure signal [0,1]

**Precedence (locked):** Terminate > Escalate > Switch > Invert > Stay

**Chatter prevention:** Actions require exceeding theta threshold AND beating Stay by margin delta.

### Step 6: The Identity Kernel

Five invariants that must survive ALL lawful transitions:

| Invariant | Type | Tier | What It Means |
|-----------|------|------|---------------|
| Triadic completeness | Binary | 1 | All 3 roles (Ideal, Boundary, Core) must be present |
| Asymmetric work | Graded | 1 | Work distribution is not uniform |
| Boundary load-bearing | Threshold | 1 | Boundary must be doing real work in both modes |
| Calibration necessity | Binary | 1 | Cannot skip the measurement step |
| Dependency primacy | Binary | 1 | Dependency order > temporal order |

**Invariant types matter:**
- Binary: pass/fail only (score >= 0.5 passes)
- Graded: continuous degradation allowed, any score > 0 passes
- Threshold: graded internally but hard-fails below a cutpoint

If ANY Tier-1 invariant is violated, the transition is a structural event, not a minor hiccup.

### Step 7: Directed Axis Space

The system operates across 5 axes: Horizontal, Vertical, Face, Body, Periodic.

**Critical correction:** H->V is NOT the same as V->H. These are different transform species.

- H->V: "Spread options, test level constraints, land on viable placement"
- V->H: "Deepen hierarchy, constrain by spread/adjacency"

Total axis states: 5 single + 20 directed pairs = 25

This was previously modeled as 10 (undirected) or even 5 (single-axis). Both were wrong.

### Step 8: Regime-Conditioned Sampling

The Monte Carlo stress test was upgraded from naive uniform sampling to regime-aware:

| Sampling Mode | What It Tests | Key Finding |
|---------------|---------------|-------------|
| Uniform | Controller logic sanity | ~48% invert, ~44% stay (coin flip) |
| Field-conditioned | Pulse-dominant behavior | 85% stay (stable, holds position) |
| Frame-conditioned | Constrain-dominant behavior | 85% invert (asymmetric, flips constantly) |

**This is a real result, not decoration.** The same controller produces fundamentally different action distributions depending on regime. That confirms regime is structural, not cosmetic.

---

# SECTION 3: THE CODE

## 3.1 File Structure

```
resonance-triality/
  CLAUDE.md                           # Project instructions for AI assistants
  RESONANCE_TRIALITY_COMPLETE.md      # Full theory document (~50KB)
  TECHNICAL_IMPLEMENTATION.md         # THIS FILE
  README.md                           # Landing page
  01 Resonance Triality.md            # Placeholder
  .gitignore
  requirements.txt                    # numpy>=1.24.0
  validation/
    __init__.py
    stress_test_council.py            # THE MAIN CODE (~930 lines)
    results/
      .gitkeep
```

## 3.2 Code Architecture (stress_test_council.py)

The file has 12 parts. Here is exactly what each does and why.

### Part 1: Core Enums and Types (lines ~37-68)

Defines the vocabulary:
- `Mode`: DIAGNOSTIC_132 or GENERATIVE_213
- `Regime`: FIELD, FRAME, or MIXED
- `StabilityType`: ATTRACTOR, SADDLE, or REPELLER
- `TransitionAction`: STAY, SWITCH_MODE, INVERT, ESCALATE, TERMINATE
- `InvariantType`: BINARY, GRADED, THRESHOLD
- `AXES`: ["H", "V", "Face", "Body", "Periodic"]
- `AXIS_STATES`: all 25 states (5 single + 20 directed)

**Why this matters:** These enums enforce that the code uses the theory's vocabulary precisely. No string-typing. No drift.

### Part 2: Identity Kernel (lines ~75-115)

`KernelInvariant` dataclass with typed evaluation:
- Binary invariants pass/fail at 0.5
- Graded invariants return continuous score
- Threshold invariants hard-fail below their cutpoint

`KERNEL_INVARIANTS` is the list of 5 locked invariants with their types and tiers.

**Why this matters:** Previous implementations treated kernel as 5 booleans. The theory says some invariants degrade continuously (asymmetric_work) and some have hard cutpoints (boundary_load_bearing at 0.4). The typed evaluation captures this.

### Part 3: Field/Frame Translation Engine (lines ~120-185)

Three coordinate systems:
- `FieldCoordinates(rho, alpha, phi)` -- center-derived
- `FrameCoordinates(constraint_level, enclosure_sector, elimination_phase)` -- boundary-derived

`RegimeTranslator` provides:
- `field_to_frame()`: rho -> 1/constraint (inversely proportional), alpha -> sector (60-degree quantization), phi -> elimination phase (normalized)
- `frame_to_field()`: reverse mapping
- `round_trip_error()`: measures identity loss in Field->Frame->Field conversion
- `classify_regime()`: scores 4 diagnostic questions to classify an artifact as Field/Frame/Mixed

**KNOWN LIMITATION:** Alpha quantizes into 60-degree sectors, which means round-trip loses angular precision. This is logged as regime translation debt, not hidden.

**Why this matters:** The 132 Protocol is Frame-native (boundary elimination). The S=(rho,alpha,phi) coordinates are Field-native. Without explicit translation, mapping between them produces silent errors. This engine makes the translation declared and testable.

### Part 4: Calibration and State (lines ~190-240)

`Residue` dataclass: tracks what was eliminated, contested, and unmapped. Computes weighted magnitude where eliminated items count little (0.1), contested items count moderate (0.5), and unmapped items count heavy (0.8).

`CalibrationOutput`: the full measurement bundle (position, residue, stability score+type, mode signal+strength).

`SystemState`: the complete state vector `X_t = (mode, regime, axis, scale, kernel_status, calibration, cycle)`.

**Why this matters:** This is the sensor layer. Without it, the controller has no inputs. Before this code existed, the architecture was "a controller without sensors" -- a formal language for describing, not predicting.

### Part 5: Transition Controller (lines ~245-340)

`TransitionController` with three methods:
- `compute_scores()`: the 5 transition score formulas
- `select_action()`: applies precedence with hysteresis
- `compute_asymmetry()` + `dominant_asymmetry()`: identifies which dimension (direction, mode, regime, axis, scale) is most imbalanced

**The score formulas in plain English:**
- Stay is high when: stable, low residue, low asymmetry
- Switch is high when: strong inverse-mode signal, high residue, high instability
- Invert is high when: high asymmetry, low stability
- Escalate is high when: stable, high residue, high scale-structure signal
- Terminate is high when: stable, low residue, high task completion

**Precedence logic:**
```
if terminate beats threshold AND beats stay by margin: TERMINATE
elif escalate beats threshold AND beats stay by margin: ESCALATE
elif switch beats threshold AND beats stay by margin: SWITCH
elif invert beats stay by reduced margin: INVERT
else: STAY
```

**KNOWN LIMITATION:** The score formulas multiply components as if they are independent. The theory says they are coupled (stability affects residue, asymmetry affects mode signal, etc.). This is a simplification. The regime-conditioned Monte Carlo partially compensates by giving the inputs correlated distributions, but the formula itself is still linear. This is the biggest gap between theory and implementation.

### Part 6: Measurement Layer (lines ~345-435)

`MeasurementProtocol` with static methods:
- `measure_stability()`: commitment clarity + objection absence + perturbation response -> score + type
- `measure_residue()`: lists of eliminated/contested/unmapped -> Residue object
- `measure_mode_signal()`: decision logic based on stability, completion, core development, boundary contestation, scale residue, asymmetry -> (action, strength)
- `evaluate_kernel()`: runs each invariant through its typed evaluation

**Why this matters:** This is how raw interaction data becomes the numbers that feed the controller. Without this layer, someone looking at the code would not know how to go from "the customer wavered when I mentioned the alternative" to `perturbation_response = "wavered"` to `stability_score = 0.43, stability_type = SADDLE`.

### Part 7: Adversarial Scenarios (lines ~440-530)

12 scenarios designed to break the model, categorized by severity:

**Critical (4):** Chatter Loop, Deadlock, Prediction Miss, Kernel Breach
**Major (6):** Overconfident Stability, Contradictory Signals, Phase Blur, Cognitive Overload, Regime Leak, Mode Stagnation
**Minor (2):** Mode Collision, Scale Collapse

Each scenario has: name, description, target expert, expected failure mode, parameters, severity.

### Part 8: Directed Axis Interaction Engine (lines ~535-650)

`AXIS_INTERACTIONS` dictionary with all 20 directed pairs. Each entry has:
- description
- 132_reading (what it means in diagnostic mode)
- 213_reading (what it means in generative mode)
- Some have field_behavior and frame_behavior

**Example -- why direction matters:**
- `Face->Body`: "Present signal, constrain by mechanism" -- you're testing whether the visible interface can be supported by the underlying mechanism
- `Body->Face`: "Expand mechanism, constrain by presentation" -- you're testing whether the hidden mechanism can be made visible

These are genuinely different operations. Collapsing them into one "Face-Body interaction" erases half the diagnostic information.

### Part 9: Sensitivity Analysis (lines ~655-750)

`SensitivityAnalysis` class with three sampling modes:

1. **Uniform**: all parameters drawn from Uniform(0,1). Tests controller logic, NOT theory.
2. **Field-conditioned**: parameters drawn from Beta distributions that reflect pulse-dominant behavior (high stability, low residue, low instability). Tests theory's prediction about Field regime.
3. **Frame-conditioned**: parameters drawn from Beta distributions that reflect constrain-dominant behavior (moderate stability, higher residue, higher asymmetry). Tests theory's prediction about Frame regime.

Also: `cliff_edge_analysis()` -- sweeps one parameter while holding others fixed to find where the winning action flips. These are the parameter values where the model is most sensitive.

**Why three modes matter:** If you only run uniform, you see "invert and stay are basically 50/50." That tells you the controller is balanced but says nothing about the theory. The regime-conditioned runs show that Field produces 85% stay while Frame produces 85% invert -- same logic, different regime, different behavior. That's a testable prediction.

### Part 10: Council Experts (lines ~755-895)

Six expert validators, each checking for different failure modes:

| Expert | What They Check |
|--------|----------------|
| Control Systems Engineer | Chatter (3+ action changes in 4 cycles), deadlock (low stability forcing STAY), open feedback loops |
| Bayesian Statistician | Incoherent calibration (high stability + repeller type), contradictory signals, completion/residue mismatch |
| Cognitive Scientist | Phase blur (Burst and Crush nearly equal), mode collision (felt both diagnostic and generative) |
| Sales Practitioner | Prediction miss (predicted != actual), cognitive overload (logging > interaction time) |
| Topologist | Tier-1 kernel breach, regime leak (declared != actual without translation), round-trip reversibility error |
| Systems Theorist | Mode stagnation (same mode 8+ cycles), scale collapse (escalate didn't change scale) |

Each expert returns `{expert, pass, issues, verdict}`. Council pass rate should be >= 5/6 for a valid run.

### Part 11: Falsification Conditions (lines ~900-950)

7 conditions that would kill specific parts of the theory:

| ID | What It Would Kill | Kill Condition |
|----|--------------------|----------------|
| F1 | T2 (Boundary as Work) | 8/10 stable Cores with Crush < 10% effort |
| F2 | Generative mode architecture | 8/10 forms hold without boundary crystallization |
| F3 | Mode inversion claim | >20% of mode switches show kernel breach |
| F4 | Role identity | Accuracy unchanged with mis-assigned roles |
| F5 | Universal architecture claim | Optimal theta varies >0.2 across practitioners |
| F6 | Structural weighting hypothesis | SD > mean for any phase duration |
| F7 | Entire controller | Prediction accuracy < 40% across 50+ interactions |

**Why these exist:** Without explicit falsifiers, the theory can reinterpret any failure as "partial coherence" or "emergent regime." These conditions make failure concrete and undeniable.

### Part 12: Full Stress Test Execution (lines ~955-end)

`run_demo_interaction()` creates a synthetic interaction with all required fields.
`run_full_stress_test()` runs the complete pipeline:
1. Demo interaction through measurement layer
2. Transition score computation
3. Council review (all 6 experts)
4. Regime translation test (Field->Frame->Field round-trip)
5. Directed axis semantics check
6. Sensitivity analysis (uniform + field + frame)
7. Cliff edge detection
8. Falsification conditions display
9. Adversarial scenarios summary

---

# SECTION 4: THE HONEST DEBT LEDGER

These are not "future improvements." They are structural gaps that affect the validity of the current implementation.

## 4.1 Score Independence Assumption (CRITICAL)

**The problem:** The transition score formulas multiply components as independent factors. The theory says they are coupled.

**Concrete example:** Stability and residue are not independent. A high-residue interaction (lots of contested options) tends to have lower stability. But the formulas treat sigma and e* as if they could take any values independently.

**Impact:** The controller may double-penalize or miss correlated failures.

**Fix needed:** Either derive coupling terms from empirical data, or restructure the scores to use conditional logic rather than multiplication.

## 4.2 Mixed Regime (MAJOR)

**The problem:** Mixed regime is classified (Field score 0.3-0.7) but has no operational behavior of its own. It's currently a label, not a functioning regime.

**What it should do:** Implement the translation protocol -- when an artifact is Mixed, the system should explicitly apply Field->Frame or Frame->Field translation and log the translation cost.

**Impact:** Any interaction classified as Mixed currently gets default behavior. The most interesting and difficult cases are Mixed.

## 4.3 Scale Engine (MAJOR)

**The problem:** `escalate` is a valid transition action, but the scale parameter has no real engine. It's a string ("micro", "meso", "macro") with no transition logic.

**What it should do:** Define what changes when scale shifts. Does the kernel change? Do thresholds change? Does the axis space change?

**Impact:** Escalate can fire as a transition action but does nothing meaningful.

## 4.4 Alpha Quantization in Translation (MINOR)

**The problem:** Field-to-Frame translation quantizes alpha into 60-degree sectors. This means angular information is lost in round-trips.

**Impact:** Round-trip error is nonzero even for "clean" translations. This is acceptable if the lost information is not identity-bearing, but that determination has not been formally made.

## 4.5 Empirical Calibration (BLOCKING for real use)

**The problem:** All thresholds (theta=0.5, delta=0.15) are theoretical. They have not been tuned against real interaction data.

**What's needed:** 20+ instrumented sales interactions with predicted vs actual actions logged. Then threshold optimization against prediction accuracy.

**This is the single most important next step.** The architecture is sound. The thresholds are guesses.

## 4.6 The 20/50/30 Question (OPEN)

**The problem:** Is the Crush-dominant weighting structural or contingent?

**If structural:** Crush should dominate in every domain (Bayesian likelihood, phonetic consonant effort, topological boundary weight).

**If contingent:** The specific percentages vary by domain, but the asymmetry (middle phase does most work) may still be structural because that's where Pulse and Constrain actually interact.

**Current code treatment:** Kept as hypothesis. NOT used to derive action-rate targets. NOT hardcoded into the controller.

---

# SECTION 5: HOW TO USE THIS CODEBASE

## 5.1 Running the Stress Test

```bash
pip install numpy
python validation/stress_test_council.py
```

This runs the full pipeline on a synthetic demo interaction and produces:
- Transition scores with predicted action
- Council verdict (6 experts)
- Regime translation test
- Sensitivity analysis (3 sampling modes)
- Cliff edge detection
- Falsification conditions

## 5.2 Running a Real Interaction

To test the theory against reality, create an interaction dict with these fields:

```python
interaction = {
    # Phase data (from timing the interaction)
    "burst_duration_pct": 0.20,      # fraction of total time in Burst
    "crush_duration_pct": 0.50,      # fraction in Crush
    "click_duration_pct": 0.30,      # fraction in Click

    # Stability (observe at Click moment)
    "commitment_clarity": 0.7,       # 0-1: how clear was their commitment?
    "new_objections_at_click": 1,    # integer: new objections raised at Click
    "perturbation_response": "stable", # strengthened/stable/neutral/wavered/abandoned

    # Residue (what happened during Crush)
    "options_eliminated": ["X", "Y"],  # list of things definitively ruled out
    "options_contested": ["Z"],        # list of things still argued about
    "options_unmapped": [],            # list of things never addressed

    # Mode / regime (your assessment)
    "felt_diagnostic": True,        # did it feel like testing/filtering?
    "felt_generative": False,       # did it feel like building/expanding?
    "regime": "frame",              # field/frame/mixed
    "identity_origin": "boundary",  # center or boundary
    "failure_mode": "collapse",     # drift/decoherence or collapse/fracture
    "coherence_feel": "containment",# resonance/sync or containment/support
    "native_transform": "segmentation", # projection/radiation or segmentation/load

    # Completion
    "task_completion": 0.75,        # 0-1
    "core_fully_developed": True,   # is the Core solid?
    "boundary_contested": False,    # is the Boundary still being argued?
    "scale_bound_residue": False,   # is unresolved stuff at a different scale?
    "dominant_asymmetry": 0.3,      # 0-1

    # Axis
    "axis": "H->V",                # which axis or directed pair
    "scale": "micro",              # micro/meso/macro

    # Kernel (score each 0-1)
    "kernel_triadic_completeness": 1.0,
    "kernel_asymmetric_work": 0.85,
    "kernel_boundary_load_bearing": 0.9,
    "kernel_calibration_necessity": 1.0,
    "kernel_dependency_primacy": 1.0,

    # Actual outcome (for validation)
    "actual_action": "terminate",   # what actually happened
    "interaction_duration_s": 120,
    "logging_duration_s": 60,

    # History
    "action_history": [],
    "mode_history": [],
}
```

Then run it through the pipeline manually or modify `run_demo_interaction()` to return your data.

## 5.3 Interpreting Results

**Prediction match:** If predicted action matches actual action, the controller is tracking reality for that interaction.

**Prediction miss:** Identify which score was miscalibrated. Common causes:
- theta too high: terminate/escalate/switch can't fire even when they should
- delta too high: minority actions can't beat stay
- stability measurement doesn't reflect reality (overconfident or underconfident)

**Council verdict:** If < 5/6 pass, check which expert failed and why. Each failure points to a specific subsystem.

**Regime translation:** Round-trip error > 0.15 means Field/Frame translation is losing identity-bearing information.

---

# SECTION 6: THE NESTED ARCHITECTURE (Complete Reference)

For absolute clarity, here is the full locked stack:

```
Level 0 -- PRIMITIVE TENSION
  Pulse <-> Constrain

Level 1 -- MINIMAL LOOP
  Pulse -> Constrain -> Calibrate -> Invert

Level 2 -- ROLE LAYER
  1 = Ideal (ceiling / possibility span)
  3 = Boundary (testing surface / elimination)
  2 = Core (remainder / seed)

Level 3 -- MODE LAYER
  132 = Diagnostic (discover what survives pressure)
    Dependency: 1 must open before 3 can test; 3 must test before 2 is revealed
  213 = Generative (expand from seed into bounded form)
    Dependency: 2 must exist before 1 can expand; 1 must expand before 3 stabilizes

  Switching law: current mode's output becomes inverse mode's input
    132 outputs Core -> if unstable, becomes 213's seed
    213 outputs Boundary -> if contested, becomes 132's testing surface

Level 4 -- CONTROL LAYER
  Actions: Stay, Switch, Invert, Escalate, Terminate
  Precedence: Terminate > Escalate > Switch > Invert > Stay
  Inversion targets: argmax of asymmetry vector (direction, mode, regime, axis, scale)

Level 5 -- REGIME LAYER
  Field: pulse-dominant, center-derived identity, phase/gradient continuity
  Frame: constrain-dominant, boundary-derived identity, edge/adjacency continuity
  Mixed: translation zone (PROVISIONAL -- underspecified)

Level 6 -- AXIS LAYER
  5 single axes: H, V, Face, Body, Periodic
  20 directed pairs: H->V, V->H, H->Face, Face->H, ... (direction matters)

Level 7 -- DOMAIN LAYER
  Sales, Bayesian updating, phonetic articulation, topological closure,
  signal detection, pricing, attention, breathing, etc.
  Domains INSTANTIATE the loop. They do not DEFINE it.
```

---

# SECTION 7: THINGS A FUTURE CLAUDE MUST NOT DO

1. **Do not flatten Field and Frame into one regime.** They produce different controller behavior. The Monte Carlo proves this.

2. **Do not treat 132 as the only mode.** 213 (generative) is the sovereign inverse. Both are needed.

3. **Do not optimize thresholds to match arbitrary action-rate targets.** Tune against prediction accuracy on real data.

4. **Do not claim the Monte Carlo validates the theory.** Uniform sampling validates the controller logic. Regime-conditioned sampling tests the theory's structural predictions. These are different claims.

5. **Do not treat H->V and V->H as the same thing.** There are 25 axis states, not 10.

6. **Do not add complexity without necessity.** The primitive is Pulse <-> Constrain. The loop is 4 steps. The roles are 3. The modes are 2. The actions are 5. The kernel is 5 invariants. Everything else is derived. Keep it lean.

7. **Do not defend the framework from falsification.** The whole point is that it CAN fail. If a falsification condition is met, update the model, not the interpretation.

8. **Do not confuse "the conversation was a 132 instance" with proof.** It is a recursive instantiation, not a universal proof. The difference matters.

9. **Do not promote one domain example into the ontology.** Sales is James's primary testing ground. It is not the theory itself.

10. **Do not pretend Mixed regime is solved.** It is not. It is a placeholder.

---

# SECTION 8: THE CENTRAL QUESTION

> Does the controller predict or merely describe?

The architecture is internally consistent. The transition scores compute. The kernel invariants are defined. The council knows what failure looks like. The regime-conditioned Monte Carlo shows structural differentiation between Field and Frame.

But none of that means it tracks reality.

The only test that matters: one real sales interaction, fully instrumented, with actual numbers in the template, compared to what actually happened.

That comparison IS the test.

Everything else is preparation.

---

**Document version**: 0.3
**Confidence in document accuracy**: 0.88
**Confidence in theory accuracy**: 0.70 (untested against real data)
**Author**: Claude (Opus 4.6), documenting work done in collaboration with James (mret3672-sys)
