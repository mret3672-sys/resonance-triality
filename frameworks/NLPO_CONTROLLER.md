# NLPO Transition Controller -- Fabric 36 ENGINE Heart

## Purpose

Arbitrate state changes, rank actions, and enforce ratio-preserving decisions inside the closed topology.

---

## Inputs (from NLPO state vector + logs)

| Input | Description |
|-------|-------------|
| **p(t)** | Current regime: {IDEAL, BOUNDARY, CORE} |
| **phi(t)** | Continuous phase in [0, 2pi) |
| **N(t)** | Channel vector [A, Lambda, V, R, S, ...] |
| **z-scores** | Baseline-normalized + coherence score |
| **Pressure vector** | Cost/relief gradients |
| **Proof-strip flags** | Contradiction, drift, saturation |
| **Temporal scale** | Micro / meso / macro / epoch |

---

## Internal State

- p(t), phi(t), baseline, utility weights (pressure/relief), memory scope (trace retention)
- Governing invariants from constitutional core (ratio survival check)

---

## Actions (6 canonical verbs -- command center palette)

| Action | Description |
|--------|-------------|
| **STAY** | Hold regime |
| **SWITCH** | IDEAL <-> BOUNDARY <-> CORE (with explicit trigger) |
| **INVERT** | Sovereign counter-pole (13 through 2) |
| **ESCALATE** | Widen scope or temporal scale |
| **TERMINATE** | Commit / log / reset to new IDEAL |
| **REPAIR** | Invoke recovery protocol (re-anchor, mirror, simplify) |

---

## Scoring / Utility Equation

Ranks competing actions:

```
Utility = coherence x (relief - pressure) x ratio_survival_factor
```

Where:
- **ratio_survival_factor** = 1 if, after simulated rotation/inversion, the governing invariants (A-01 to A-08) return intact; else 0.
- **Critical damping target:** zeta_nlpo ~ 1 at CORE resolution.

---

## Outputs

| Output | Description |
|--------|-------------|
| Chosen action | + route artifact (map / prompt / trace) |
| Updated NLPO log | Entry + proof-strip link |
| Console command block | For Fabric 36 Command Center |

---

## Acceptance Tests (finish conditions -- run before any further sheets)

| Test | Criterion |
|------|-----------|
| **AT-1** | Transition prediction accuracy >70% within 2x micro-pulse window |
| **AT-2** | Post-repair coherence gain >60% in logged drift/contradiction cases |
| **AT-3** | Ablation: controller with coupling beats uncoupled baseline by >10% |
| **AT-4** | Ratio survival: every action, when inverted/rotated/replayed, returns invariants intact |
| **AT-5** | One-page wiring complete in Fabric 36 (cells traceable to this spec) |

---

## Implementation Note

Wire directly into Fabric 36 _ENGINE and Command Center. First pilot: 3-5 real interaction logs. Parameter revision only from evidence (alpha = 0.7 slow adaptation).

---

## 132 <-> 213 <-> 312 Traversal Modes

The controller now supports three traversal orientations:

| Mode | Reading Order | Description |
|------|--------------|-------------|
| **132** | Origin -> Closure -> Relation | Ingress/diagnostic: how the point enters the field |
| **213** | Relation -> Origin -> Closure | Egress/generative: how the field distributes around the point |
| **312** | Closure -> Origin -> Relation | Governance: how the formed whole gives parts their place |

### The Missing Tooth

132 and 213 alone give reversal but not re-seating. 312 completes the permutation body:

- 132 = lived sequence (in frame)
- 213 = distributed relation (in field)
- 312 = returned structure (from closure)

Without 312, you have motion. With 312, you have jurisdiction.

### The Symmetry of 2

In all three modes, 2 occupies every position exactly once:

- 132: 2 is the receiving edge (terminal)
- 213: 2 is the issuing edge (initial)
- 312: 2 is the held middle (explicit)

The symmetry is orbital, not reflective. 2 is the traveling boundary of the triad.

---

## Known Gaps

1. **Scale engine absent:** ESCALATE has no 8Y-infinity analog yet. The scale-change action needs a concrete operator.
2. **Y-transformer rotation rule unspecified:** When to use i-rotation vs e^gamma-scaling.
3. **Tilt parameter (delta = 0.15):** Treated as fixed in some docs, should remain a free parameter until empirically calibrated.
4. **Workbook wiring incomplete:** Constitutional_Core and Controller_Spec sheets exist in Fabric 36 but have zero formulas wired into them.

---

## Confidence

| Element | Score |
|---------|-------|
| Controller spec as paper contract | 0.88 |
| Action vocabulary completeness | 0.85 |
| Utility equation structure | 0.82 |
| Acceptance test design | 0.90 |
| Live implementation readiness | 0.55 |

**Status:** The decision shell the register declared missing. The constitutional core + controller contract together turn the 458-item register into an operable system. But paper contract != working engine. Wire it, test it, or it remains a throne with no kingdom.
