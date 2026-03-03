# L1 AXIOMS: The Geometric Coordinate System S = (ρ, α, ϕ)

**Version**: 1.0
**Confidence**: 0.72 (Tier 2 — externally grounded in Gabor analysis, echolocation physics, polar cognition)
**Status**: PROBABLE → implementing for empirical validation

---

## Axiom G-0: The Coordinate Primitive

**Every communicative state S is uniquely specified by three coordinates:**

```
S = (ρ, α, ϕ)
```

Where:
- **ρ** (rho) — Radial depth: pressure magnitude / attentional intensity
- **α** (alpha) — Angular sector: categorical orientation on the hexagonal lattice
- **ϕ** (phi) — Phase state: position within the 132 pulse topology

**Justification**: First-person experience is inherently polar (Yousif & Keil, 2024 — spontaneous spatial cognition uses polar, not Cartesian, coordinates). The body-origin cross (vertical spine × horizontal shoulders) generates radial depth from self as origin.

---

## Axiom G-1: Radial Depth (ρ)

**ρ maps attentional intensity onto the interval [0, φ] where φ = 1.618033...**

### Definition

```
ρ ∈ [0, φ]

where φ = (1 + √5) / 2 = 1.618033988749895...
```

### From Signal (Gabor Transform)

```
ρ = φ × log(1 + |G|_max) / log(1 + |G|_global_max)
```

Where:
- `|G|_max` = peak magnitude of the Gabor transform for the current window
- `|G|_global_max` = global maximum across the entire signal
- Log compression follows standard psychoacoustic Weber-Fechner law

### GSSM Layer Mapping

| Layer       | Code | ρ Range         | HP State  |
|-------------|------|-----------------|-----------|
| GUIDE       | GUI  | [1.294, 1.618]  | HP-12→10  |
| SUPPORT     | SUP  | [0.971, 1.294)  | HP-9→7    |
| STABILIZE   | STA  | [0.647, 0.971)  | HP-6 (Sweet Spot) |
| MARK        | MAR  | [0.324, 0.647)  | HP-5→4    |
| EPICENTER   | EPI  | [0, 0.324)      | LP-3→1    |

Layer boundaries follow φ-subdivision: each boundary = φ × (n/5) for n ∈ {0,1,2,3,4,5}.

### Invariant

```
ρ = 0   ⟹  No attentional energy (silence / absence)
ρ = 1.0 ⟹  Unity threshold (φ⁻¹ reflection point)
ρ = φ   ⟹  Maximum projection (saturation)
```

**Confidence**: 0.78 — Log-magnitude compression is standard signal processing. φ-normalization is a design choice, not derived.

---

## Axiom G-2: Angular Sector (α)

**α quantizes orientation into 6 sectors of 60° each on the hexagonal lattice.**

### Definition

```
α ∈ {0°, 60°, 120°, 180°, 240°, 300°}
```

### Sector Assignment

| Sector | Code | Angle | Domain                    |
|--------|------|-------|---------------------------|
| 0      | TMP  | 0°    | Temporal Navigation       |
| 1      | ACT  | 60°   | Actualize Output          |
| 2      | GRV  | 120°  | Gravity Synthesis         |
| 3      | GRL  | 180°  | Gralv Synthesis           |
| 4      | CDX  | 240°  | Codex Vault               |
| 5      | ORG  | 300°  | Origin (W—O bilateral)    |

### From Signal (Frequency Mapping)

**This is the explicitly defined mapping that closes the α gap:**

```
α = floor( 6 × frac( log₂(f / f_base) ) ) × 60°
```

Where:
- `f` = dominant frequency of the Gabor atom (Hz)
- `f_base` = 125 Hz (base frequency — chosen as C below middle C, the approximate fundamental of relaxed male speech)
- `frac(x)` = fractional part of x (i.e., x mod 1)
- The mapping is **octave-periodic**: frequencies one octave apart map to the same sector
- Within each octave, the 6 sectors correspond to equal divisions of log-frequency space

### Derivation of f_base = 125 Hz

This is NOT arbitrary. It is the convergence of:
1. **Speech fundamental**: Relaxed male F0 ≈ 85-155 Hz, geometric mean ≈ 115 Hz, nearest power-of-two-friendly value = 125 Hz
2. **Musical grounding**: 125 Hz ≈ B2, one semitone below C3 (130.81 Hz). This places middle C at the boundary between sectors, giving musically meaningful divisions
3. **Psychoacoustic**: Below 125 Hz, pitch perception becomes ambiguous (critical band width ≈ frequency). This is the floor of clear tonal perception

### Sector-Frequency Correspondence (one octave, f_base = 125 Hz)

| Sector | Code | Frequency Range (Hz) | Musical Interval |
|--------|------|---------------------|------------------|
| 0      | TMP  | 125.0 – 139.8       | Unison → ~M2     |
| 1      | ACT  | 139.8 – 156.3       | ~M2 → ~M3        |
| 2      | GRV  | 156.3 – 174.6       | ~M3 → ~tritone   |
| 3      | GRL  | 174.6 – 195.2       | ~tritone → ~m6   |
| 4      | CDX  | 195.2 – 218.1       | ~m6 → ~M7        |
| 5      | ORG  | 218.1 – 250.0       | ~M7 → octave     |

Each sector spans exactly one whole tone (2^(1/6) ≈ 1.1225 frequency ratio).

**Confidence**: 0.65 — Mapping is now explicit and testable. f_base requires empirical validation against speech data. The sector-semantic assignments (TMP, ACT, etc.) are structural, not derived from the frequency mapping.

---

## Axiom G-3: Phase State (ϕ) — The 132 Pulse Topology

**ϕ encodes position within the calibration pulse as one of three distinguished states.**

### Definition

```
ϕ ∈ {IDEAL, BOUNDARY, CORE}

Notation: ϕ₁ = IDEAL, ϕ₃ = BOUNDARY, ϕ₂ = CORE
```

The subscripts follow the 132 sequence, NOT numerical order.

### Echolocation Grounding

The 132 pulse is a **calibration probe**, not a temporal sequence:

| Phase | Code | ρ Target | Action              | Echolocation Analog      |
|-------|------|----------|---------------------|--------------------------|
| ϕ₁    | IDL  | φ        | Maximum projection  | Emit pulse (search mode) |
| ϕ₃    | BND  | 1.0      | Detect reflection   | Hit surface (approach)   |
| ϕ₂    | COR  | φ⁻¹      | Resolve to action   | Return signal (terminal) |

### Golden Ratio Decay

The pulse contracts along the golden spiral:

```
ρ(ϕ₁) = φ    = 1.618   (IDEAL — maximum outward projection)
ρ(ϕ₃) = 1.0             (BOUNDARY — unity reflection surface)
ρ(ϕ₂) = φ⁻¹  = 0.618   (CORE — convergence point)
```

Ratio between consecutive targets:
```
ρ(ϕ₃) / ρ(ϕ₁) = 1 / φ = φ⁻¹ ≈ 0.618
ρ(ϕ₂) / ρ(ϕ₃) = φ⁻¹ / 1 = φ⁻¹ ≈ 0.618
```

Each step contracts by exactly φ⁻¹. This IS the golden spiral.

### From Signal (Envelope Analysis)

```
Given Gabor envelope E(t):

ϕ = IDEAL     if  dE/dt > 0  and  E(t) > E_threshold     (rising edge)
ϕ = BOUNDARY  if  dE/dt ≈ 0  and  E(t) ≈ E_peak          (inflection)
ϕ = CORE      if  dE/dt < 0  and  E(t) approaching E_eq   (settling)
```

### Critical Damping Connection

At ζ = 1 (critical damping), the system sits at the bifurcation boundary:
- ζ < 1: Underdamped (oscillatory — signal rings, no convergence)
- ζ = 1: **Critical** (fastest convergence to equilibrium without overshoot)
- ζ > 1: Overdamped (sluggish — signal converges but too slowly)

ζ = 1 is NOT "equilibrium unavoided" — it is the **optimal convergence rate**. The 132 pulse naturally wants to critically damp: project maximally (IDEAL), hit the reflection surface (BOUNDARY), converge without oscillation (CORE).

**Confidence**: 0.71 — Pulse topology grounded in echolocation physics. Golden ratio decay is a design choice with aesthetic coherence but is not derived from first principles. Envelope classification thresholds require empirical calibration.

---

## Axiom G-4: Cartesian Projection

**The polar coordinates (ρ, α) project to Cartesian (X, Y) via:**

```
X = ρ × cos(α)
Y = ρ × sin(α)
```

This enables standard vector operations: addition, distance, interpolation between states.

---

## Axiom G-5: Scale Invariance

**The 132 pulse topology operates identically at all dimensional scales.**

The same S = (ρ, α, ϕ) structure applies whether:
- ρ measures syllabic pressure (milliseconds)
- ρ measures conversational momentum (seconds)
- ρ measures negotiation position (minutes)
- ρ measures life trajectory (years)

The propagation velocity `c` is context-dependent, but the pulse shape is invariant:

```
d = c × Δt / 2
```

Where `d` = distance to Core, `c` = context propagation speed, `Δt` = round-trip time.

**Confidence**: 0.55 — Scale invariance is asserted from phenomenology, not derived. Requires cross-scale empirical validation.

---

## Derived Quantities

### Pressure Index (PI)

```
PI = ρ / φ × 12

Maps ρ ∈ [0, φ] → PI ∈ [0, 12]
Directly corresponds to HP-12 lattice positions
```

### Pulse Energy (E_pulse)

```
E_pulse = ρ(ϕ₁)² - ρ(ϕ₂)²
        = φ² - φ⁻²
        = 2.618 - 0.382
        = 2.236
        = √5
```

The energy released by one complete 132 pulse is exactly √5. This is a consequence of the golden ratio structure, not imposed.

### State Distance

```
d(S₁, S₂) = √( (ρ₁cos(α₁) - ρ₂cos(α₂))² + (ρ₁sin(α₁) - ρ₂sin(α₂))² + w_ϕ × δ(ϕ₁, ϕ₂)² )
```

Where `w_ϕ` is the phase weight and `δ(ϕ₁, ϕ₂)` maps phase differences to distances:
- δ(IDL, BND) = φ⁻¹
- δ(BND, COR) = φ⁻¹
- δ(IDL, COR) = 1.0
- δ(same, same) = 0

---

## Epistemic Status Summary

| Component | Confidence | Tier | External Grounding |
|-----------|------------|------|--------------------|
| ρ radial via Gabor log-magnitude | 0.78 | 2 | Weber-Fechner, standard DSP |
| α hexagonal via log-frequency | 0.65 | 2-3 | Gabor frame theory, Tonnetz; f_base needs validation |
| ϕ 132 pulse via envelope | 0.71 | 2 | Echolocation physics, theta oscillations |
| Golden ratio normalization | 0.60 | 3 | Aesthetic coherence; not derived from physics |
| Scale invariance | 0.55 | 3-4 | Phenomenological assertion |
| **Overall S = (ρ, α, ϕ)** | **0.67** | **2-3** | **Coherent + externally anchored, needs empirical test** |

---

## What Would Increase Confidence

1. **Run 10 sales interactions through the prototype** → If coordinates predict outcomes: +0.15
2. **Validate f_base against speech corpus** → If 125 Hz is optimal: +0.05
3. **Cross-scale test** → Same topology works at conversation and negotiation scale: +0.10
4. **Independent replication** → Another practitioner assigns coordinates predictively: +0.15
