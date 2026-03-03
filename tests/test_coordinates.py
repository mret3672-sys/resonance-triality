"""Tests for the State object and coordinate transforms."""

import math
import pytest

from triality.constants import PHI, PHI_INV, Phase
from triality.coordinates import (
    State,
    polar_to_cartesian,
    cartesian_to_polar,
    state_distance,
    interpolate_rho,
    golden_spiral_rho,
)


class TestState:
    """Test the State coordinate object."""

    def test_basic_creation(self):
        s = State(rho=1.0, alpha_deg=60.0, phase=Phase.IDEAL)
        assert s.rho == 1.0
        assert s.alpha_deg == 60.0
        assert s.phase == Phase.IDEAL

    def test_rho_clamping(self):
        s = State(rho=5.0, alpha_deg=0.0, phase=Phase.CORE)
        assert s.rho == PHI  # clamped to max

        s2 = State(rho=-1.0, alpha_deg=0.0, phase=Phase.CORE)
        assert s2.rho == 0.0  # clamped to min

    def test_alpha_wrapping(self):
        s = State(rho=1.0, alpha_deg=420.0, phase=Phase.CORE)
        assert s.alpha_deg == 60.0

    def test_cartesian_projection(self):
        # At α=0°, x=ρ, y=0
        s = State(rho=1.0, alpha_deg=0.0, phase=Phase.CORE)
        assert abs(s.x - 1.0) < 1e-14
        assert abs(s.y - 0.0) < 1e-14

        # At α=90°, x=0, y=ρ
        s2 = State(rho=1.0, alpha_deg=90.0, phase=Phase.CORE)
        assert abs(s2.x) < 1e-14
        assert abs(s2.y - 1.0) < 1e-14

    def test_from_frequency(self):
        s = State.from_frequency(rho=1.0, freq=125.0, phase=Phase.IDEAL)
        assert s.alpha_deg == 0.0  # f_base maps to sector 0

    def test_from_sector_code(self):
        s = State.from_sector_code(rho=1.0, sector_code="GRV", phase=Phase.BOUNDARY)
        assert s.alpha_deg == 120.0

    def test_from_hp_level(self):
        s = State.from_hp_level(hp_level=6, sector_code="TMP", phase=Phase.CORE)
        assert s.hp_level == 6
        assert s.alpha_deg == 0.0

    def test_sector_property(self):
        s = State(rho=1.0, alpha_deg=120.0, phase=Phase.CORE)
        assert s.sector.code == "GRV"

    def test_gssm_layer(self):
        s = State(rho=0.1, alpha_deg=0.0, phase=Phase.CORE)
        assert s.gssm_layer.code == "EPI"

    def test_pressure_index(self):
        s = State(rho=PHI, alpha_deg=0.0, phase=Phase.IDEAL)
        assert abs(s.pressure_index - 12.0) < 1e-10

        s2 = State(rho=0.0, alpha_deg=0.0, phase=Phase.CORE)
        assert s2.pressure_index == 0.0

    def test_repr(self):
        s = State(rho=1.0, alpha_deg=120.0, phase=Phase.BOUNDARY)
        r = repr(s)
        assert "ρ=1.000" in r
        assert "α=120°" in r
        assert "GRV" in r
        assert "BND" in r


class TestPolarCartesian:
    """Test polar ↔ Cartesian conversions."""

    def test_roundtrip(self):
        for alpha in [0, 60, 120, 180, 240, 300]:
            x, y = polar_to_cartesian(1.0, alpha)
            rho_back, alpha_back = cartesian_to_polar(x, y)
            assert abs(rho_back - 1.0) < 1e-10
            assert abs(alpha_back - alpha) < 1e-10

    def test_origin(self):
        x, y = polar_to_cartesian(0.0, 45.0)
        assert abs(x) < 1e-14
        assert abs(y) < 1e-14


class TestStateDistance:
    """Test distance metric in triality space."""

    def test_same_state_zero(self):
        s = State(rho=1.0, alpha_deg=0.0, phase=Phase.CORE)
        assert state_distance(s, s) == 0.0

    def test_spatial_only(self):
        # Same phase, different position
        s1 = State(rho=1.0, alpha_deg=0.0, phase=Phase.CORE)
        s2 = State(rho=1.0, alpha_deg=180.0, phase=Phase.CORE)
        d = state_distance(s1, s2)
        # Should be 2.0 (opposite points on unit circle)
        assert abs(d - 2.0) < 1e-10

    def test_phase_only(self):
        # Same position, different phase
        s1 = State(rho=0.0, alpha_deg=0.0, phase=Phase.IDEAL)
        s2 = State(rho=0.0, alpha_deg=0.0, phase=Phase.CORE)
        d = state_distance(s1, s2)
        # At origin, spatial distance is 0; only phase contributes
        assert d == 1.0  # δ(IDEAL, CORE) = 1.0

    def test_symmetric(self):
        s1 = State(rho=1.0, alpha_deg=60.0, phase=Phase.IDEAL)
        s2 = State(rho=0.5, alpha_deg=120.0, phase=Phase.CORE)
        assert abs(state_distance(s1, s2) - state_distance(s2, s1)) < 1e-14


class TestGoldenSpiral:
    """Test golden spiral trajectory generation."""

    def test_first_three_are_132(self):
        values = golden_spiral_rho(3)
        assert abs(values[0] - PHI) < 1e-14
        assert abs(values[1] - 1.0) < 1e-14
        assert abs(values[2] - PHI_INV) < 1e-14

    def test_decay_ratio(self):
        values = golden_spiral_rho(5)
        for i in range(1, len(values)):
            ratio = values[i] / values[i - 1]
            assert abs(ratio - PHI_INV) < 1e-14

    def test_interpolate_endpoints(self):
        assert interpolate_rho(0.0, 1.0, 0.0) == 0.0
        assert interpolate_rho(0.0, 1.0, 1.0) == 1.0
        assert abs(interpolate_rho(0.0, 1.0, 0.5) - 0.5) < 1e-14
