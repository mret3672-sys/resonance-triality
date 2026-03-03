"""
Gabor Transform engine: signal → S = (ρ, α, ϕ) coordinates.

The Gabor transform decomposes a signal into time-frequency atoms,
each localized in both time and frequency. These atoms map directly
to the triality coordinate system:

    |G|_max  →  ρ  (radial depth via log-magnitude compression)
    ω_peak   →  α  (angular sector via octave-periodic frequency mapping)
    envelope →  ϕ  (phase state via envelope shape classification)
"""

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np

from triality.constants import (
    PHI, F_BASE,
    Phase,
    frequency_to_sector_index, frequency_to_alpha,
)
from triality.coordinates import State


@dataclass
class GaborAtom:
    """A single Gabor atom: a Gaussian-windowed sinusoid."""
    center_time: float        # seconds
    center_freq: float        # Hz
    sigma: float              # Gaussian width (seconds)
    magnitude: float          # |G| peak magnitude
    phase_rad: float          # oscillator phase (radians)


class GaborTransform:
    """
    Compute the Gabor transform of a 1D signal and map to triality coordinates.

    The transform uses a Gaussian window with configurable width σ,
    producing a time-frequency representation where each point has
    magnitude, frequency, and envelope shape.

    Parameters:
        sigma: Gaussian window width in seconds. Default 0.025 (25ms,
               standard for speech analysis).
        hop_size: Hop between analysis windows in seconds. Default 0.010 (10ms).
        n_freq_bins: Number of frequency bins. Default 256.
        sample_rate: Expected sample rate of input signals. Default 16000.
    """

    def __init__(
        self,
        sigma: float = 0.025,
        hop_size: float = 0.010,
        n_freq_bins: int = 256,
        sample_rate: int = 16000,
    ):
        self.sigma = sigma
        self.hop_size = hop_size
        self.n_freq_bins = n_freq_bins
        self.sample_rate = sample_rate

        # Precompute Gaussian window
        self._window_samples = int(6 * sigma * sample_rate)  # ±3σ coverage
        if self._window_samples % 2 == 0:
            self._window_samples += 1
        half = self._window_samples // 2
        t = np.arange(-half, half + 1) / sample_rate
        self._window = np.exp(-t**2 / (2 * sigma**2))
        self._window /= np.sum(self._window)  # normalize

    def analyze(self, signal: np.ndarray) -> list[GaborAtom]:
        """
        Compute Gabor atoms for the input signal.

        Args:
            signal: 1D numpy array of audio samples at self.sample_rate.

        Returns:
            List of GaborAtom objects, one per analysis frame.
        """
        hop_samples = max(1, int(self.hop_size * self.sample_rate))
        n_samples = len(signal)
        half_win = self._window_samples // 2
        atoms = []

        for frame_start in range(0, n_samples - self._window_samples + 1, hop_samples):
            frame_center = frame_start + half_win
            center_time = frame_center / self.sample_rate

            # Extract windowed frame
            frame = signal[frame_start:frame_start + self._window_samples]
            windowed = frame * self._window

            # FFT
            spectrum = np.fft.rfft(windowed, n=self.n_freq_bins * 2)
            magnitudes = np.abs(spectrum)

            # Find peak frequency
            peak_bin = np.argmax(magnitudes[1:]) + 1  # skip DC
            freqs = np.fft.rfftfreq(self.n_freq_bins * 2, d=1.0 / self.sample_rate)
            center_freq = freqs[peak_bin]
            magnitude = magnitudes[peak_bin]
            phase_rad = np.angle(spectrum[peak_bin])

            atoms.append(GaborAtom(
                center_time=center_time,
                center_freq=max(1.0, center_freq),  # floor at 1 Hz
                sigma=self.sigma,
                magnitude=magnitude,
                phase_rad=phase_rad,
            ))

        return atoms

    def atoms_to_states(
        self,
        atoms: list[GaborAtom],
        global_max: Optional[float] = None,
    ) -> list[State]:
        """
        Map Gabor atoms to triality coordinates.

        ρ = φ × log(1 + |G|_max) / log(1 + |G|_global_max)
        α = floor(6 × frac(log₂(f / f_base))) × 60°
        ϕ = envelope shape classification

        Args:
            atoms: List of GaborAtom from analyze().
            global_max: Global maximum magnitude for normalization.
                       If None, uses max from the provided atoms.

        Returns:
            List of State objects, one per atom.
        """
        if not atoms:
            return []

        if global_max is None:
            global_max = max(a.magnitude for a in atoms)
        if global_max <= 0:
            global_max = 1.0

        log_global = math.log(1 + global_max)
        magnitudes = [a.magnitude for a in atoms]
        phases = self._classify_envelope(magnitudes)

        states = []
        for atom, phase in zip(atoms, phases):
            # ρ from log-magnitude (Weber-Fechner)
            rho = PHI * math.log(1 + atom.magnitude) / log_global

            # α from frequency (octave-periodic)
            alpha = frequency_to_alpha(atom.center_freq)

            states.append(State(rho=rho, alpha_deg=alpha, phase=phase))

        return states

    def signal_to_states(
        self,
        signal: np.ndarray,
        global_max: Optional[float] = None,
    ) -> list[State]:
        """Full pipeline: signal → Gabor atoms → triality States."""
        atoms = self.analyze(signal)
        return self.atoms_to_states(atoms, global_max)

    def _classify_envelope(self, magnitudes: list[float]) -> list[Phase]:
        """
        Classify each frame's phase state from envelope dynamics.

        ϕ = IDEAL     if dE/dt > 0 and E > threshold   (rising edge)
        ϕ = BOUNDARY  if dE/dt ≈ 0 and E ≈ peak        (inflection)
        ϕ = CORE      if dE/dt < 0 and E → equilibrium  (settling)

        Uses a simple first-derivative classification with hysteresis.
        """
        if len(magnitudes) <= 1:
            return [Phase.CORE] * len(magnitudes)

        phases = []
        peak = max(magnitudes) if magnitudes else 1.0
        if peak <= 0:
            peak = 1.0
        threshold = 0.1 * peak  # 10% of peak = noise floor

        for i, mag in enumerate(magnitudes):
            if i == 0:
                # First frame: check if rising
                if len(magnitudes) > 1 and magnitudes[1] > mag:
                    phases.append(Phase.IDEAL)
                else:
                    phases.append(Phase.CORE)
                continue

            derivative = magnitudes[i] - magnitudes[i - 1]
            relative_mag = mag / peak

            if derivative > threshold * 0.5 and relative_mag > 0.3:
                phases.append(Phase.IDEAL)      # Rising edge, significant energy
            elif abs(derivative) <= threshold * 0.5 and relative_mag > 0.7:
                phases.append(Phase.BOUNDARY)   # Near peak, flat derivative
            else:
                phases.append(Phase.CORE)       # Falling or low energy

        return phases


def generate_test_signal(
    duration: float = 1.0,
    sample_rate: int = 16000,
    freq: float = 200.0,
    envelope: str = "pulse_132",
) -> np.ndarray:
    """
    Generate a test signal for coordinate system validation.

    Args:
        duration: Signal duration in seconds.
        sample_rate: Sample rate in Hz.
        freq: Carrier frequency in Hz.
        envelope: Envelope shape — one of:
            "pulse_132": Golden-ratio modulated pulse (IDEAL→BOUNDARY→CORE)
            "constant": Flat amplitude
            "rising": Linear ramp up
            "falling": Linear ramp down

    Returns:
        1D numpy array of samples.
    """
    n_samples = int(duration * sample_rate)
    t = np.arange(n_samples) / sample_rate

    # Carrier
    carrier = np.sin(2 * np.pi * freq * t)

    # Envelope
    if envelope == "pulse_132":
        # Golden ratio envelope: rise to peak, brief plateau, decay
        # Phase 1 (IDEAL): rise for φ⁻² of duration
        # Phase 3 (BOUNDARY): plateau for φ⁻¹ - φ⁻² of duration
        # Phase 2 (CORE): decay for 1 - φ⁻¹ of duration
        phi_inv = 1.0 / PHI
        t1 = phi_inv ** 2  # ≈ 0.382
        t2 = phi_inv       # ≈ 0.618
        env = np.zeros(n_samples)
        for i, ti in enumerate(t / duration):
            if ti < t1:
                env[i] = ti / t1  # linear rise to peak
            elif ti < t2:
                env[i] = 1.0      # plateau at peak
            else:
                env[i] = 1.0 - (ti - t2) / (1.0 - t2)  # linear decay
        env = np.maximum(env, 0.0)
    elif envelope == "constant":
        env = np.ones(n_samples)
    elif envelope == "rising":
        env = np.linspace(0, 1, n_samples)
    elif envelope == "falling":
        env = np.linspace(1, 0, n_samples)
    else:
        raise ValueError(f"Unknown envelope: {envelope}")

    return carrier * env
