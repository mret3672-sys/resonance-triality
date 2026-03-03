# L2 Framework: Geometric Coordinate System S = (ρ, α, ϕ)

**Version**: 1.0
**Confidence**: 0.67 (Tier 2-3)
**Dependencies**: L1_AXIOMS.md, Cl(2,1) geometric algebra, hexagonal Gabor frames, echolocation physics

---

## 1. Architecture Overview

The geometric coordinate system provides a **universal coordinate grammar** for the Resonance Triality framework. Every communicative state — from a single syllable's pressure to a year-long negotiation arc — maps to a point S = (ρ, α, ϕ) in the hexagonal triality space.

```
                    TMP (0°)
                   /       \
            ORG (300°)     ACT (60°)
                |     •     |
            CDX (240°)     GRV (120°)
                   \       /
                    GRL (180°)

        Inner rings: EPI → MAR → STA → SUP → GUI
        Phase pulse: 1(IDEAL) → 3(BOUNDARY) → 2(CORE)
```

### Three Dimensions

| Dimension | Symbol | Domain | Meaning | External Grounding |
|-----------|--------|--------|---------|--------------------|
| Radial | ρ | [0, φ] | Pressure depth / attentional intensity | Weber-Fechner log compression, Gabor magnitude |
| Angular | α | {0°,60°,...,300°} | Categorical orientation on hex lattice | Optimal Gabor sampling (Bastiaans 2000), Tonnetz |
| Phase | ϕ | {IDL, BND, COR} | Position in 132 calibration pulse | Echolocation physics, theta-rhythmic attention |

---

## 2. The Radial Dimension (ρ)

### Transform: Signal → ρ

```python
ρ = φ × log(1 + |G|_max) / log(1 + |G|_global_max)
```

This maps Gabor magnitude to [0, φ] with logarithmic compression matching Weber-Fechner psychophysics: perceived intensity grows as log of physical intensity.

### Concentric Architecture (GSSM Layers)

```
ρ = 0.000 ─────────── EPICENTER (LP-1 to LP-3)
ρ = 0.324 ─────────── MARK (HP-4 to HP-5)
ρ = 0.647 ─────────── STABILIZE (HP-6 Sweet Spot)
ρ = 0.971 ─────────── SUPPORT (HP-7 to HP-9)
ρ = 1.294 ─────────── GUIDE (HP-10 to HP-12)
ρ = 1.618 ─────────── φ (Maximum)
```

Boundaries at `φ × n/5` for n ∈ {0,...,5}.

### HP-12 Lattice Mapping

```python
ρ = hp_level × (φ / 12)    # HP → ρ
hp = round(ρ × 12 / φ)     # ρ → HP
```

Direct bidirectional conversion. HP-6 (sweet spot) maps to ρ ≈ 0.809.

---

## 3. The Angular Dimension (α)

### Transform: Frequency → α

**The explicit mapping that closes the α gap from the epistemic audit:**

```python
α = floor(6 × frac(log₂(f / f_base))) × 60°
```

Where `f_base = 125 Hz`.

### Why f_base = 125 Hz

Three independent convergences:
1. **Speech**: Geometric mean of relaxed male F0 range (85-155 Hz) ≈ 115 Hz → nearest clean value = 125
2. **Music**: 125 Hz ≈ B2, one semitone below C3 (130.81 Hz)
3. **Psychoacoustics**: Below 125 Hz, critical bandwidth ≈ frequency (pitch perception degrades)

### Octave Periodicity

The mapping is **octave-periodic**: 250 Hz maps to the same sector as 125 Hz, 500 Hz maps to the same as both. Within each octave, 6 equal log-frequency bins correspond to the 6 sectors.

Each sector spans a frequency ratio of `2^(1/6) ≈ 1.1225` — exactly one whole tone in musical terms.

### Sector Semantics

| Code | Angle | Name | Domain |
|------|-------|------|--------|
| TMP | 0° | Temporal Navigation | When? Time, urgency, scheduling |
| ACT | 60° | Actualize Output | What? Actions, deliverables, concrete steps |
| GRV | 120° | Gravity Synthesis | Why? Weight, importance, pull toward decision |
| GRL | 180° | Gralv Synthesis | How? Process, mechanism, structure |
| CDX | 240° | Codex Vault | Reference? Rules, policies, stored knowledge |
| ORG | 300° | Origin (W-O bilateral) | Who? Identity, source, bilateral symmetry axis |

---

## 4. The Phase Dimension (ϕ) — 132 Pulse Topology

### The Calibration Probe

The 132 is **not** a temporal sequence. It's a **calibration pulse** following the golden spiral inward:

```
IDEAL (ρ = φ)                    ← emit, project, search
    ↘ × φ⁻¹
BOUNDARY (ρ = 1.0)              ← reflect, detect resistance
    ↘ × φ⁻¹
CORE (ρ = φ⁻¹)                  ← resolve, converge, act
```

### Echolocation Physics

The pulse mirrors biological echolocation:

| Phase | Bat Echolocation | Sales | Breath |
|-------|-------------------|-------|--------|
| IDEAL (1) | Emit pulse, search mode | High anchor, maximum projection | Inhale |
| BOUNDARY (3) | Hit surface, approach | Customer pushback, resistance | Hold |
| CORE (2) | Return signal, terminal buzz | Transaction point, action | Exhale |

**Distance to Core**: `d = c × Δt / 2`

Bats increase pulse rate during approach (terminal buzz at 200 clicks/sec). The same topology: as you approach Core, calibration frequency increases.

### Pulse Energy

```
E = ρ(IDEAL)² - ρ(CORE)²
  = φ² - φ⁻²
  = (φ + φ⁻¹)(φ - φ⁻¹)
  = √5 × 1
  = √5 ≈ 2.236
```

The energy of one complete 132 pulse is exactly √5. Not approximately — exactly.

### Envelope Classification

From a Gabor transform, the phase is classified by envelope dynamics:

```
Rising edge + significant energy    → IDEAL
Flat derivative + near peak         → BOUNDARY
Falling or low energy               → CORE
```

---

## 5. Derived Quantities

### Pressure Index

```
PI = (ρ / φ) × 12    maps ρ ∈ [0, φ] → PI ∈ [0, 12]
```

### State Distance

```
d(S₁, S₂) = √( (x₁-x₂)² + (y₁-y₂)² + w_ϕ × δ(ϕ₁,ϕ₂)² )
```

Where x = ρcos(α), y = ρsin(α), and δ(ϕ₁,ϕ₂) uses the phase distance matrix.

### Cartesian Projection

```
X = ρ × cos(α)
Y = ρ × sin(α)
```

Standard polar → Cartesian for vector operations.

---

## 6. Implementation

The Python package `triality` implements the full coordinate system:

```
src/triality/
├── constants.py      # φ, sectors, GSSM layers, frequency mapping
├── coordinates.py    # State object, transforms, distance metric
├── gabor.py          # Signal → S = (ρ, α, ϕ) pipeline
├── pulse_probe.py    # 132 calibration probe engine
└── hp_lattice.py     # HP-12 pressure state detection
```

### Quick Start

```python
from triality import State, Phase, PulseProbe, HPLattice, GaborTransform

# Create a state directly
s = State(rho=1.0, alpha_deg=120.0, phase=Phase.BOUNDARY)
print(s)  # S(ρ=1.000, α=120°[GRV], ϕ=BND)

# From HP level and sector
s2 = State.from_hp_level(hp_level=6, sector_code="TMP", phase=Phase.CORE)
print(s2.gssm_layer.name)  # Stabilize

# Run a 132 pulse probe
probe = PulseProbe()
result = probe.probe_sector("GRV")
print(result.energy)      # 2.236 (√5)
print(result.is_golden)   # True

# Diagnose with actual measurements
result = probe.probe_sector("ACT",
    rho_ideal=1.5, rho_boundary=1.1, rho_core=0.7)
diagnosis = probe.diagnose(result)
print(diagnosis["protocol_recommendation"])

# HP-12 decision tree
lattice = HPLattice()
decision = lattice.decision_tree(breath_rate_hz=0.45)
print(decision["recommended_protocol"])  # BURST first

# Process audio signal
import numpy as np
from triality.gabor import generate_test_signal
signal = generate_test_signal(duration=1.0, freq=200.0, envelope="pulse_132")
gt = GaborTransform()
states = gt.signal_to_states(signal)
for s in states[:5]:
    print(s)
```

---

## 7. Epistemic Status

### What Is Grounded

| Claim | Confidence | Evidence |
|-------|------------|----------|
| Polar coordinates as cognitive default | 0.82 | Yousif & Keil 2024 |
| Hexagonal sampling optimal for Gabor | 0.85 | Bastiaans 2000, Ricaud 2013 |
| Log-magnitude compression | 0.90 | Weber-Fechner law, standard DSP |
| Theta-rhythmic attentional sampling | 0.78 | Fiebelkorn & Kastner 2020 |
| Echolocation pulse topology | 0.75 | Bat biosonar literature |
| Body-origin vestibular coordinates | 0.80 | Vestibular cognition research |

### What Is Asserted (Not Derived)

| Claim | Confidence | Gap |
|-------|------------|-----|
| f_base = 125 Hz | 0.65 | Convergent reasoning, not empirically validated on speech |
| Sector semantics (TMP, ACT, etc.) | 0.50 | Structural assignment, no derivation from frequency |
| Golden ratio normalization | 0.60 | Aesthetic coherence, not derived from physics |
| Scale invariance of 132 | 0.55 | Phenomenological assertion |

### Path to Validation

1. **Process 10 sales recordings** → assign S coordinates pre-outcome → check predictive power
2. **Validate f_base** on speech corpus → is 125 Hz optimal for sector discrimination?
3. **Cross-scale test** → same probe topology at syllabic, conversational, negotiation scales
4. **Independent replication** → another practitioner assigns coordinates predictively

---

## 8. Cross-References

- **L1 Axioms**: `core/L1_AXIOMS.md` — formal definitions, confidence scores
- **132 Protocol**: Burst→Crush→Click as echolocation pulse, not temporal sequence
- **HP-12 Lattice**: 12-point topology integrated via `hp_to_rho()` / `rho_to_hp()`
- **Utility Equation**: U = (R×M×G)/(C×P×t) × φ — integrated in `HPLattice.utility_score()`
- **Spiral Breathing**: 4-7-8 maps to 132 via Inhale(IDEAL)→Hold(BOUNDARY)→Exhale(CORE)
- **Gabor Frame Theory**: Hexagonal Gabor frames as the signal-theoretic basis
- **Cl(2,1) Geometric Algebra**: Recommended algebraic engine for future formalization
- **Contact Geometry**: Recommended for native dissipation modeling (ζ=1 critical damping)
