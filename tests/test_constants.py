"""Tests for fundamental constants and mappings."""

import math
import pytest

from triality.constants import (
    PHI, PHI_INV, PHI_SQ, PHI_INV_SQ, SQRT_5,
    PULSE_ENERGY,
    NUM_SECTORS, SECTORS, SECTOR_BY_CODE,
    GSSM_LAYERS, GSSM_BY_CODE,
    Phase, PULSE_SEQUENCE, PHASE_DISTANCE,
    F_BASE,
    frequency_to_sector_index, frequency_to_alpha,
    hp_to_rho, rho_to_hp, rho_to_gssm,
)


class TestGoldenRatio:
    """Verify golden ratio identities."""

    def test_phi_definition(self):
        assert abs(PHI - (1 + math.sqrt(5)) / 2) < 1e-15

    def test_phi_inverse(self):
        assert abs(PHI * PHI_INV - 1.0) < 1e-15

    def test_phi_squared(self):
        assert abs(PHI_SQ - PHI - 1.0) < 1e-14  # φ² = φ + 1

    def test_phi_inv_squared(self):
        assert abs(PHI_INV_SQ - (1 - PHI_INV)) < 1e-14  # φ⁻² = 1 - φ⁻¹

    def test_pulse_energy_is_sqrt5(self):
        """E = φ² - φ⁻² = √5. This is exact, not approximate."""
        assert abs(PULSE_ENERGY - SQRT_5) < 1e-14
        assert abs(PULSE_ENERGY - math.sqrt(5)) < 1e-14


class TestSectors:
    """Verify hexagonal sector definitions."""

    def test_six_sectors(self):
        assert len(SECTORS) == 6

    def test_sector_angles(self):
        for i, sector in enumerate(SECTORS):
            assert sector.angle_deg == i * 60.0
            assert abs(sector.angle_rad - i * math.pi / 3) < 1e-14

    def test_sector_codes_unique(self):
        codes = [s.code for s in SECTORS]
        assert len(set(codes)) == 6

    def test_sector_by_code(self):
        assert SECTOR_BY_CODE["TMP"].angle_deg == 0.0
        assert SECTOR_BY_CODE["GRV"].angle_deg == 120.0
        assert SECTOR_BY_CODE["ORG"].angle_deg == 300.0


class TestFrequencyMapping:
    """Verify the explicit α mapping: f → sector index."""

    def test_base_frequency_maps_to_sector_0(self):
        assert frequency_to_sector_index(F_BASE) == 0

    def test_octave_periodicity(self):
        """Frequencies one octave apart map to the same sector."""
        for f in [125, 200, 300, 440]:
            idx = frequency_to_sector_index(f)
            idx_octave_up = frequency_to_sector_index(f * 2)
            assert idx == idx_octave_up, f"f={f}: sector {idx} != {idx_octave_up}"

    def test_two_octaves_periodic(self):
        """Two octaves up also maps to same sector."""
        for f in [125, 250]:
            assert frequency_to_sector_index(f) == frequency_to_sector_index(f * 4)

    def test_sectors_cover_octave(self):
        """All 6 sectors are hit within one octave."""
        # Sweep from f_base to 2*f_base in small steps
        sectors_hit = set()
        for i in range(600):
            f = F_BASE * (2 ** (i / 600))
            sectors_hit.add(frequency_to_sector_index(f))
        assert sectors_hit == {0, 1, 2, 3, 4, 5}

    def test_sector_boundaries(self):
        """Each sector spans 2^(1/6) frequency ratio."""
        ratio = 2 ** (1.0 / 6)
        # Just below sector boundary → sector 0
        f_just_below = F_BASE * ratio * 0.999
        assert frequency_to_sector_index(f_just_below) == 0
        # Just above sector boundary → sector 1
        f_just_above = F_BASE * ratio * 1.001
        assert frequency_to_sector_index(f_just_above) == 1

    def test_alpha_returns_degrees(self):
        alpha = frequency_to_alpha(F_BASE)
        assert alpha == 0.0
        # A frequency in sector 3 should give 180°
        f_sector3 = F_BASE * (2 ** (3 / 6))
        assert frequency_to_alpha(f_sector3) == 180.0

    def test_negative_frequency_raises(self):
        with pytest.raises(ValueError):
            frequency_to_sector_index(-100)

    def test_zero_frequency_raises(self):
        with pytest.raises(ValueError):
            frequency_to_sector_index(0)


class TestGSSMLayers:
    """Verify GSSM concentric layer structure."""

    def test_five_layers(self):
        assert len(GSSM_LAYERS) == 5

    def test_layers_cover_full_range(self):
        """Layers should span from 0 to φ."""
        assert GSSM_LAYERS[0].rho_min == 0.0
        assert abs(GSSM_LAYERS[-1].rho_max - PHI) < 1e-14

    def test_layers_contiguous(self):
        """Each layer's max = next layer's min."""
        for i in range(len(GSSM_LAYERS) - 1):
            assert abs(GSSM_LAYERS[i].rho_max - GSSM_LAYERS[i + 1].rho_min) < 1e-14

    def test_epicenter_is_innermost(self):
        assert GSSM_LAYERS[0].code == "EPI"
        assert GSSM_LAYERS[0].rho_min == 0.0

    def test_guide_is_outermost(self):
        assert GSSM_LAYERS[-1].code == "GUI"
        assert abs(GSSM_LAYERS[-1].rho_max - PHI) < 1e-14

    def test_rho_to_gssm_mapping(self):
        assert rho_to_gssm(0.0).code == "EPI"
        assert rho_to_gssm(0.5).code == "MAR"
        # ρ=1.0 falls in SUP layer (boundary between STA and SUP is at φ×3/5 ≈ 0.971)
        assert rho_to_gssm(1.0).code == "SUP"
        assert rho_to_gssm(PHI).code == "GUI"


class TestHPMapping:
    """Verify HP-12 ↔ ρ bidirectional mapping."""

    def test_hp_to_rho_range(self):
        rho_1 = hp_to_rho(1)
        rho_12 = hp_to_rho(12)
        assert rho_1 > 0
        assert abs(rho_12 - PHI) < 1e-14

    def test_rho_to_hp_roundtrip(self):
        for hp in range(1, 13):
            rho = hp_to_rho(hp)
            assert rho_to_hp(rho) == hp

    def test_hp_out_of_range_raises(self):
        with pytest.raises(ValueError):
            hp_to_rho(0)
        with pytest.raises(ValueError):
            hp_to_rho(13)


class TestPhase:
    """Verify 132 pulse phase definitions."""

    def test_phase_values(self):
        assert Phase.IDEAL.value == 1
        assert Phase.BOUNDARY.value == 3
        assert Phase.CORE.value == 2

    def test_phase_codes(self):
        assert Phase.IDEAL.code == "IDL"
        assert Phase.BOUNDARY.code == "BND"
        assert Phase.CORE.code == "COR"

    def test_rho_targets(self):
        assert abs(Phase.IDEAL.rho_target - PHI) < 1e-14
        assert Phase.BOUNDARY.rho_target == 1.0
        assert abs(Phase.CORE.rho_target - PHI_INV) < 1e-14

    def test_sequence_order(self):
        assert [p.sequence_order for p in PULSE_SEQUENCE] == [0, 1, 2]

    def test_golden_ratio_decay(self):
        """Each phase target is φ⁻¹ of the previous."""
        targets = [p.rho_target for p in PULSE_SEQUENCE]
        assert abs(targets[1] / targets[0] - PHI_INV) < 1e-14
        assert abs(targets[2] / targets[1] - PHI_INV) < 1e-14

    def test_phase_distance_symmetric(self):
        for p1 in Phase:
            for p2 in Phase:
                d12 = PHASE_DISTANCE[(p1, p2)]
                d21 = PHASE_DISTANCE[(p2, p1)]
                assert d12 == d21

    def test_phase_distance_self_zero(self):
        for p in Phase:
            assert PHASE_DISTANCE[(p, p)] == 0.0
