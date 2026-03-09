# Perceptual Bicycle — Foundational Form

## Minimal machine

The operational core is:

**{0,1} + | + T(♾️) + A**

- `{0,1}`: minimal stable distinction (two-pole frame)
- `|`: coupling operator (chunk boundary)
- `T(♾️)`: mirror/reverse fold around fixed hinge symbol `♾️`
- `A`: attention frame (hinge position, chunk size, direction, scale)

## Canonical closure expression

A closure-grade decimal example (hinge at 6, chunk-size 3):

`(012|345|6)789♾️987(6|543|210)`

Closure laws:

1. `right = T(left)`
2. `T(full) = full`
3. `T² = id`

## Most foundational route: ring-first statement

Work in `Z/9Z` (digital-root residue ring). The triadic ridge is:

`B₃ = {0,3,6}`

This is an order-3 subgroup under addition mod 9. So the "369 ridge" is not extra decoration; it is a structural subset already present in the ring.

### Fold law

For hinge `h`, define fold action:

`T_h(i) = h - i (mod 9)`

If `h ∈ B₃` and `i ∈ B₃`, then `T_h(i) ∈ B₃` because `B₃` is closed under subtraction.

So mirror closure at hinges 0/3/6 preserves the same ridge set.

### Steering law (attention translation)

`A` can shift the observed phase by a residue `a`.

Cosets of `B₃` in `Z/9Z` are:

- `B₃ + 0 = {0,3,6}`
- `B₃ + 1 = {1,4,7}`
- `B₃ + 2 = {2,5,8}`

Therefore, "369" is the zero-origin view of a deeper 3-phase invariant that survives steering.

## Executable surface

The strict runtime implementation is in:

- `src/perceptual_bicycle/core.clj`

That namespace enforces the three closure laws during generation.
