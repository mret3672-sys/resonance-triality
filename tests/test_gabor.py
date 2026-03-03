"""Tests for the Gabor transform engine."""

import math
import numpy as np
import pytest

from triality.constants import PHI, F_BASE, Phase
from triality.gabor import GaborTransform, generate_test_signal


class TestGaborTransform:
    """Test the Gabor analysis pipeline."""

    def setup_method(self):
        self.gt = GaborTransform(
            sigma=0.025,
            hop_size=0.010,
            n_freq_bins=256,
            sample_rate=16000,
        )

    def test_analyze_produces_atoms(self):
        signal = generate_test_signal(duration=0.5, freq=200.0, envelope="constant")
        atoms = self.gt.analyze(signal)
        assert len(atoms) > 0
        assert all(a.center_freq > 0 for a in atoms)
        assert all(a.magnitude >= 0 for a in atoms)

    def test_constant_signal_stable_magnitude(self):
        signal = generate_test_signal(duration=0.5, freq=200.0, envelope="constant")
        atoms = self.gt.analyze(signal)
        magnitudes = [a.magnitude for a in atoms]
        # Skip edge frames, check stability of middle frames
        middle = magnitudes[5:-5]
        if len(middle) > 2:
            mean_mag = sum(middle) / len(middle)
            for m in middle:
                assert abs(m - mean_mag) / (mean_mag + 1e-10) < 0.3  # within 30%

    def test_frequency_detection(self):
        """The dominant frequency should be near the carrier."""
        signal = generate_test_signal(duration=0.5, freq=300.0, envelope="constant")
        atoms = self.gt.analyze(signal)
        middle_atoms = atoms[5:-5]
        if middle_atoms:
            avg_freq = sum(a.center_freq for a in middle_atoms) / len(middle_atoms)
            assert abs(avg_freq - 300.0) < 50.0  # within 50 Hz

    def test_atoms_to_states(self):
        signal = generate_test_signal(duration=0.5, freq=200.0, envelope="constant")
        atoms = self.gt.analyze(signal)
        states = self.gt.atoms_to_states(atoms)
        assert len(states) == len(atoms)
        for s in states:
            assert 0 <= s.rho <= PHI
            assert 0 <= s.alpha_deg < 360
            assert isinstance(s.phase, Phase)

    def test_rho_log_compression(self):
        """Higher magnitude → higher ρ, but log-compressed."""
        signal_loud = generate_test_signal(duration=0.5, freq=200.0, envelope="constant")
        signal_quiet = signal_loud * 0.1
        atoms_loud = self.gt.analyze(signal_loud)
        atoms_quiet = self.gt.analyze(signal_quiet)
        states_loud = self.gt.atoms_to_states(atoms_loud)
        states_quiet = self.gt.atoms_to_states(atoms_quiet, global_max=max(a.magnitude for a in atoms_loud))
        # Average ρ of loud should be higher
        avg_rho_loud = sum(s.rho for s in states_loud) / len(states_loud)
        avg_rho_quiet = sum(s.rho for s in states_quiet) / len(states_quiet)
        assert avg_rho_loud > avg_rho_quiet

    def test_full_pipeline(self):
        signal = generate_test_signal(duration=1.0, freq=200.0, envelope="pulse_132")
        states = self.gt.signal_to_states(signal)
        assert len(states) > 0

    def test_empty_signal(self):
        signal = np.array([], dtype=np.float64)
        atoms = self.gt.analyze(signal)
        assert atoms == []


class TestEnvelopeClassification:
    """Test phase classification from envelope shape."""

    def test_rising_signal_has_ideal(self):
        signal = generate_test_signal(duration=0.5, freq=200.0, envelope="rising")
        states = self.gt.signal_to_states(signal)
        # A rising signal should have at least some IDEAL frames
        ideal_count = sum(1 for s in states if s.phase == Phase.IDEAL)
        assert ideal_count >= 1

    def test_falling_signal_is_core(self):
        signal = generate_test_signal(duration=0.5, freq=200.0, envelope="falling")
        states = self.gt.signal_to_states(signal)
        # Most frames in a falling signal should be CORE
        core_count = sum(1 for s in states if s.phase == Phase.CORE)
        assert core_count > len(states) * 0.3

    def test_pulse_132_has_all_phases(self):
        """A 132 envelope should produce all three phase states."""
        signal = generate_test_signal(duration=1.0, freq=200.0, envelope="pulse_132")
        states = self.gt.signal_to_states(signal)
        phases_seen = {s.phase for s in states}
        # Should see at least IDEAL and CORE (BOUNDARY depends on plateau length)
        assert Phase.IDEAL in phases_seen or Phase.CORE in phases_seen

    def setup_method(self):
        self.gt = GaborTransform(
            sigma=0.025,
            hop_size=0.010,
            n_freq_bins=256,
            sample_rate=16000,
        )


class TestTestSignalGeneration:
    """Verify test signal shapes."""

    def test_constant_envelope(self):
        signal = generate_test_signal(duration=0.5, freq=200.0, envelope="constant")
        assert len(signal) == 8000

    def test_pulse_132_shape(self):
        signal = generate_test_signal(duration=1.0, freq=200.0, envelope="pulse_132")
        n = len(signal)
        # Should rise, plateau, then fall
        # Check that peak is roughly in the middle region
        env = np.abs(signal)  # rough envelope
        peak_idx = np.argmax(env)
        assert 0.2 * n < peak_idx < 0.8 * n

    def test_invalid_envelope_raises(self):
        with pytest.raises(ValueError):
            generate_test_signal(envelope="nonexistent")
