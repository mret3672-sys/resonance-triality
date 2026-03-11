# Street Test Protocol v0.1 -- Minimal Pilot

Zero extra sheets. Zero apps. Phone notes only. 3 sweeps max. Laser-vector minimal: one fixed probe per pass, sweep for phase edges only. Run today. Log -> Controller acceptance test tonight.

---

## Core Contract (from constitutional core + controller spec)

**Goal:** 3 real dyadic street interactions. Prove transition triggers work, coherence moves, ratio survives rotation.

**Acceptance (must hit 2/3 passes):**
- At least one visible IDEAL -> BOUNDARY -> CORE cycle per sweep
- Post-sweep coherence gain > 0.6 (subjective 0-1)
- Ratio survival: invert the log (flip 13) and core invariant still reads the same

**If fails:** Abort expansion. Revise priors from raw log only.

---

## Setup (5 min prep)

1. Choose one street block with steady foot traffic (coffee queue, crosswalk, bus stop).
2. Fixed probe (same every time, spoken verbatim):
   > "Excuse me -- quick question. What's the fastest way you've found to [local landmark]?"
   - Forces boundary contact + latent topology recovery
   - Keeps you in witness seat
3. You are Actor 1 (origin). Stranger = Actor 2 (witness). No names. No follow-ups beyond natural rhythm.
4. Phone in pocket. After each sweep only: voice-note or quick text the 7 minimal NLPO fields.

---

## Sweep Protocol (one pass = one stranger, <90 seconds total)

| Laser | Phase | Duration |
|-------|-------|----------|
| **Laser 1** | Pre-contact (IDEAL baseline) | 5 s |
| **Laser 2** | Contact (BOUNDARY trigger) | 20-40 s |
| **Laser 3** | Resolution or stall (CORE or stuck) | 10-30 s |

---

## Log Template (type exactly this after walking away -- 20 seconds)

```
Time
Subject
Phase (I/B/C)
Latency (slow/normal/fast)
Sync (0-1)
Board (B3/B7/B9)
Confidence (low/med/high)
```

Example:
```
14:12
stranger-1
B
slow
0.4
B3
med
```

Add one line only: **"Trigger that moved it: ___"** (latency spike / contradiction / stabilization / commit).

---

## Rotation Check (10 s, after all 3 sweeps)

Invert the log (13): read it as if the stranger was asking YOU the same question.

Does the core invariant ("topology recovered from partial signals") still hold?

**Yes/No + one word why.**

---

## End Condition

3 sweeps done. Copy the 3x7 table + inversion note into one message.

Controller scoring (utility equation) runs live and returns pass/fail + exact parameter revision (if any).

---

## Rules of the Laser (non-negotiable)

1. No extra questions.
2. No recording voices.
3. If someone says "no" or walks off -> log as BOUNDARY -> IDEAL bounce (valid data).
4. Total street time < 12 minutes.

---

## Controller Run Template (post-sweep)

| Metric | Criterion |
|--------|-----------|
| Phase cycle complete? | Full 132 in < 2 min |
| Coherence gain | Start -> End delta |
| Utility score | coherence x relief x ratio_survival |
| Damping | zeta_nlpo ~ 1.0 at final CORE |
| Ablation | Coupled trace beats uncoupled baseline by >10% |
| Ratio survival | Full rotation returns A-01 to A-08 unchanged |

**Verdict:** PASS / FAIL + parameter revision notes.

---

## Extended: 8Y-infinity Field Logging

For interactions run after the 8Y-infinity grammar is wired:

| Field | Description |
|-------|-------------|
| Re(f) | Real component of signal |
| Im(f) | Imaginary component of signal |
| abs(f)^2 | Probability density |
| theta / tilt | Current orientation |
| rho threshold | Pass/fail |
| alpha margin | Margin-over-stay |
| Y-op chosen | Invert / symmetry / rotate |
| Notch entry | 132 or 213 |
| Notch exit | 132 or 213 |
| Kernel survived? | Yes/No |

---

## Boldness <= Evidence Scorecard

After each logged interaction, score:

| Axis | Score (1-9) |
|------|-------------|
| Evidence Discipline | |
| Testability | |
| Claim Force | |
| Uncertainty Handling | |
| Scrutiny Survival | |

**Governing law:** Boldness score must not exceed Evidence score.

---

## Confidence

| Element | Score |
|---------|-------|
| Protocol design (minimal, falsifiable) | 0.90 |
| Log template (captures minimum viable signal) | 0.85 |
| Rotation check (tests ratio survival) | 0.88 |
| Extended 8Y-infinity fields | 0.70 |

**Status:** Ready to deploy. The protocol is proven on paper. It needs 3-5 real runs to become empirically grounded. That is the single most important next step in the entire system.
