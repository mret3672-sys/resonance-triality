"""Tests for the 132 pulse probe."""

import math
import pytest

from triality.constants import PHI, PHI_INV, PHI_INV_SQ, SQRT_5, Phase
from triality.pulse_probe import PulseProbe, ProbeResult


class TestPulseProbe:
    """Test the echolocation pulse probe."""

    def setup_method(self):
        self.probe = PulseProbe()

    def test_default_probe_is_golden(self):
        """Default probe with no overrides follows golden ratio."""
        result = self.probe.probe_sector("TMP")
        assert result.is_golden
        assert abs(result.rho_actual[0] - PHI) < 1e-10
        assert abs(result.rho_actual[1] - 1.0) < 1e-10
        assert abs(result.rho_actual[2] - PHI_INV) < 1e-10

    def test_ideal_energy_is_sqrt5(self):
        """E = φ² - φ⁻² = √5."""
        result = self.probe.probe_sector("TMP")
        assert abs(result.energy - SQRT_5) < 1e-10
        assert abs(PulseProbe.ideal_energy() - SQRT_5) < 1e-10

    def test_convergence_ratio(self):
        result = self.probe.probe_sector("TMP")
        assert abs(result.convergence_ratio - PHI_INV_SQ) < 1e-10

    def test_boundary_reflection(self):
        result = self.probe.probe_sector("TMP")
        assert abs(result.boundary_reflection - PHI_INV) < 1e-10

    def test_probe_all_sectors(self):
        results = self.probe.probe_all_sectors()
        assert len(results) == 6
        codes = [r.sector.code for r in results]
        assert codes == ["TMP", "ACT", "GRV", "GRL", "CDX", "ORG"]

    def test_custom_rho_values(self):
        result = self.probe.probe_sector("ACT", rho_ideal=1.5, rho_boundary=1.0, rho_core=0.5)
        assert result.rho_actual == [1.5, 1.0, 0.5]
        assert not result.is_golden  # not golden ratio

    def test_probe_states_have_correct_phases(self):
        result = self.probe.probe_sector("GRV")
        phases = [s.phase for s in result.states]
        assert phases == [Phase.IDEAL, Phase.BOUNDARY, Phase.CORE]

    def test_probe_states_have_correct_sector(self):
        result = self.probe.probe_sector("CDX")
        for s in result.states:
            assert s.sector.code == "CDX"

    def test_echolocation_distance(self):
        """d = c × Δt / 2."""
        d = self.probe.echolocation_distance(delta_t=2.0)
        assert d == 1.0  # c=1.0, Δt=2.0 → d=1.0

        fast_probe = PulseProbe(propagation_velocity=343.0)  # speed of sound
        d2 = fast_probe.echolocation_distance(delta_t=0.01)
        assert abs(d2 - 1.715) < 0.01

    def test_golden_spiral_trajectory(self):
        trajectory = self.probe.golden_spiral_trajectory("TMP", n_steps=6)
        assert len(trajectory) == 6
        # First three should match 132 targets
        assert abs(trajectory[0].rho - PHI) < 1e-10
        assert abs(trajectory[1].rho - 1.0) < 1e-10
        assert abs(trajectory[2].rho - PHI_INV) < 1e-10
        # Continuing decay
        assert abs(trajectory[3].rho - PHI_INV_SQ) < 1e-10

    def test_diagnose_golden_probe(self):
        result = self.probe.probe_sector("TMP")
        diagnosis = self.probe.diagnose(result)
        assert diagnosis["is_golden"]
        assert abs(diagnosis["energy_efficiency"] - 1.0) < 1e-10
        assert diagnosis["boundary_deviation"] < 0.01
        assert diagnosis["convergence_deviation"] < 0.01

    def test_diagnose_high_pressure(self):
        result = self.probe.probe_sector("TMP", rho_ideal=1.6, rho_boundary=1.4, rho_core=1.3)
        diagnosis = self.probe.diagnose(result)
        assert "BURST" in diagnosis["protocol_recommendation"]

    def test_diagnose_sweet_spot(self):
        result = self.probe.probe_sector("TMP", rho_ideal=0.9, rho_boundary=0.8, rho_core=0.7)
        diagnosis = self.probe.diagnose(result)
        assert "CLICK" in diagnosis["protocol_recommendation"]

    def test_distance_to_core(self):
        result = self.probe.probe_sector("TMP")
        assert abs(result.distance_to_core - (PHI - PHI_INV)) < 1e-10


class TestProbeResult:
    """Test ProbeResult diagnostics."""

    def test_repr(self):
        probe = PulseProbe()
        result = probe.probe_sector("TMP")
        r = repr(result)
        assert "TMP" in r
        assert "E=" in r

    def test_non_golden_detection(self):
        """A probe with linear decay is NOT golden."""
        probe = PulseProbe()
        result = probe.probe_sector("TMP", rho_ideal=1.5, rho_boundary=1.0, rho_core=0.5)
        assert not result.is_golden
