"""Tests for the HP-12 pressure lattice."""

import pytest

from triality.constants import PHI, Phase
from triality.hp_lattice import HPLattice, ThermoState


class TestHPLattice:
    """Test the 12-point pressure lattice."""

    def setup_method(self):
        self.lattice = HPLattice()

    def test_all_12_states(self):
        states = self.lattice.all_states()
        assert len(states) == 12
        assert states[0].hp_level == 12  # highest first
        assert states[-1].hp_level == 1   # lowest last

    def test_hp6_is_sweet_spot(self):
        assert self.lattice.is_sweet_spot(6)
        assert not self.lattice.is_sweet_spot(5)
        assert not self.lattice.is_sweet_spot(7)

    def test_hp10_plus_is_frozen(self):
        assert self.lattice.is_frozen(10)
        assert self.lattice.is_frozen(11)
        assert self.lattice.is_frozen(12)
        assert not self.lattice.is_frozen(9)

    def test_thermo_states(self):
        assert self.lattice.get_state(12).thermo_state == ThermoState.FROZEN
        assert self.lattice.get_state(8).thermo_state == ThermoState.VIBRATING
        assert self.lattice.get_state(6).thermo_state == ThermoState.TRIPLE_POINT
        assert self.lattice.get_state(3).thermo_state == ThermoState.MELTING

    def test_from_rho(self):
        state = self.lattice.from_rho(PHI)
        assert state.hp_level == 12

        state_low = self.lattice.from_rho(0.15)
        assert state_low.hp_level in [1, 2]

    def test_from_breath_rate(self):
        # High breath rate → high pressure
        state = self.lattice.from_breath_rate(0.45)
        assert state.hp_level >= 10

        # Sweet spot breath rate
        state_mid = self.lattice.from_breath_rate(0.27)
        assert state_mid.hp_level == 6

        # Low breath rate → low pressure
        state_low = self.lattice.from_breath_rate(0.10)
        assert state_low.hp_level <= 2

    def test_protocol_recommendations(self):
        assert "BURST" in self.lattice.recommend_protocol(12)
        assert "CRUSH" in self.lattice.recommend_protocol(8)
        assert "CLICK" in self.lattice.recommend_protocol(6)
        assert "CLICK" in self.lattice.recommend_protocol(1)

    def test_utility_score(self):
        # High utility scenario
        u = self.lattice.utility_score(
            relief=8, momentum=7, gravity=9,
            cost=3, pressure=2, time=2,
        )
        assert u > 7  # Execute immediately

        # Low utility scenario
        u_low = self.lattice.utility_score(
            relief=2, momentum=1, gravity=1,
            cost=8, pressure=9, time=7,
        )
        assert u_low < 3  # Wrong fit

    def test_utility_zero_denominator(self):
        u = self.lattice.utility_score(
            relief=5, momentum=5, gravity=5,
            cost=0, pressure=5, time=5,
        )
        assert u == float("inf")

    def test_utility_verdict(self):
        assert self.lattice.utility_verdict(8.0) == "Execute immediately"
        assert self.lattice.utility_verdict(6.0) == "Strong buy"
        assert self.lattice.utility_verdict(4.0) == "Address objections"
        assert self.lattice.utility_verdict(1.0) == "Wrong fit"

    def test_decision_tree(self):
        result = self.lattice.decision_tree(breath_rate_hz=0.45)
        assert result["pressure_state"].hp_level >= 10
        assert result["start_phase"] == Phase.IDEAL
        assert "BURST" in result["recommended_protocol"]
        assert result["thermo_state"] == "frozen"

        result_mid = self.lattice.decision_tree(breath_rate_hz=0.27)
        assert result_mid["pressure_state"].hp_level == 6
        assert "CLICK" in result_mid["recommended_protocol"]

    def test_gssm_layer_assignment(self):
        state = self.lattice.get_state(12)
        assert state.gssm_layer == "GUI"

        state_low = self.lattice.get_state(1)
        assert state_low.gssm_layer == "EPI"

    def test_invalid_hp_raises(self):
        with pytest.raises(ValueError):
            self.lattice.get_state(0)
        with pytest.raises(ValueError):
            self.lattice.get_state(13)
