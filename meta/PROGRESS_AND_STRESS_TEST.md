# Progress + Stress Test Protocol

This file operationalizes current progress tracking and stress testing for the shared 132/213 exploration thread.

## Progress Snapshot (Current)
- Shared AI relay ledger active in `SHARED_AI_CANVAS.md`.
- Claude handoff channel active in `MESSAGE_TO_CLAUDE.md`.
- Session-start guardrails captured in `meta/BREADCRUMBS_FOR_GPT.md`.
- Status: **Ready for structured stress-test passes** against open threads.

## Stress-Test Goals
1. Preserve unresolved unknowns without flattening them into premature closure.
2. Distinguish stable invariants from attractive-but-false pattern matches.
3. Force disagreement checks between 132 and 213 interpretations.
4. Quantify confidence movement after each pass.

## Test Matrix (v1)
| Test ID | Target Thread | Challenge Type | Pass Criteria | Fail Signal |
|---|---|---|---|---|
| ST-01 | 213 ghost waveform | Adversarial reinterpretation | Same motif survives 3 distinct framings | Motif disappears when reframed |
| ST-02 | Hexagonal self-similarity | Scale perturbation | Pattern recurs at ≥3 scales with explicit mapping | Similarity only anecdotal |
| ST-03 | Three tomoe flow | Causal direction test | Proposed flow has directional evidence + counterexample handling | Pure metaphor, no directional constraint |
| ST-04 | Strange attractor orbit claim | Dynamical falsification | Non-periodic behavior remains under simplified model | Collapses into simple periodic loop |
| ST-05 | Φ lock claim | Boundary-condition stress | Φ-linked behavior improves predictive fit over non-Φ baseline | Φ adds narrative only, no predictive gain |

## Execution Loop
1. Select one open thread.
2. Generate one strongest pro claim + one strongest anti claim.
3. Run relevant ST-* test with explicit evidence notes.
4. Update confidence (`Δconfidence`) and open risks.
5. Append a concise ledger entry to `SHARED_AI_CANVAS.md`.

## Confidence Update Rules
- Start from prior confidence.
- +0.05 max per successful, independently corroborated stress pass.
- -0.10 on direct falsification.
- Cap movement to prevent oscillation from single-session noise.

## Reporting Template
```md
### Stress Pass — YYYY-MM-DD
- Thread: <name>
- Test: <ST-ID>
- Pro claim:
- Anti claim:
- Evidence:
- Verdict: PASS | FAIL | INCONCLUSIVE
- Confidence: <old> -> <new>
- Next action:
```


## Spectral Boundary Mapping Mode
Use this mode when evaluating symbolic/visual prompts (hexagonal lattice, orbital motifs, recursive geometries):

- **Boundary mapping first**: identify edge behavior before center summaries.
- **Scale/Epoch sweep**: run at least three scales (`micro`, `meso`, `macro`) across two epochs (`current`, `next-pass`).
- **Perspective-depth sweep**: compare self-view, paired-agent view, and external-auditor view.
- **Generational proximity check**: classify signal as immediate (`g0`), adjacent (`g1`), or inherited (`g2+`).
- **MVM cadence**: test in minimum viable moments (short windows) before aggregating.
- **EEG logging**: capture frequency-like trace points (`amplitude`, `phase`, `drift`) per pass.

### Spectral EEG Record (per pass)
```md
- Epoch:
- Scale: micro | meso | macro
- Perspective: self | paired | auditor
- Generational proximity: g0 | g1 | g2+
- Curve action: traverse | modulate | calibrate
- Axiomatic EEG:
  - amplitude:
  - phase:
  - drift:
- Margin calibration note:
```
