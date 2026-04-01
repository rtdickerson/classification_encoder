"""
Derivative Classification - Comprehensive Pytest Test Suite

This module provides comprehensive tests for derivative classification functionality,
covering classification level escalation, distribution markings, SCI compartments,
SAP programs, and complex multi-compartment scenarios.

##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##
"""

import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

from lib.classification_encoder import (
    ClassificationEncoder,
    NamedBits,
    DerivativeClassificationEncoder,
    BitmaskManager
)


# ============================================================================
# PYTEST FIXTURES
# ============================================================================

@pytest.fixture
def encoder():
    """Provide a ClassificationEncoder instance with no configuration."""
    return ClassificationEncoder(None)


@pytest.fixture
def encoder_with_sap():
    """Provide a ClassificationEncoder with SAP configuration."""
    return ClassificationEncoder({'sap-a': 'ALPHA', 'sap-b': 'BRAVO', 'sap-c': 'CHARLIE'})


@pytest.fixture
def encoder_with_si_groups():
    """Provide a ClassificationEncoder with SI group configuration."""
    return ClassificationEncoder({'si-groupa': 'ALPHA', 'si-groupb': 'BRAVO', 'si-groupc': 'CHARLIE'})


# ============================================================================
# BASIC DERIVATIVE CLASSIFICATION TESTS
# ============================================================================

class TestDerivativeBasic:
    """Basic derivative classification tests."""
    
    def test_derivative_zero_zero(self):
        """Both masks zero should return zero."""
        newmask = DerivativeClassificationEncoder.constructClassificationString(0, 0)
        assert newmask == 0, f"Got {newmask:08X}, expected 00000000"

    def test_derivative_first_zero(self, encoder):
        """First mask zero should return second."""
        mask = encoder.parseClassificationString("SECRET")
        newmask = DerivativeClassificationEncoder.constructClassificationString(0, mask)
        assert newmask == mask, f"Got {newmask:08X}, expected {mask:08X}"

    def test_derivative_second_zero(self, encoder):
        """Second mask zero should return first."""
        mask = encoder.parseClassificationString("SECRET")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask, 0)
        assert newmask == mask, f"Got {newmask:08X}, expected {mask:08X}"

    def test_derivative_same_classification(self, encoder):
        """Same classification levels should merge correctly."""
        mask1 = encoder.parseClassificationString("SECRET")
        mask2 = encoder.parseClassificationString("SECRET")
        expected = encoder.parseClassificationString("SECRET")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"


# ============================================================================
# CLASSIFICATION LEVEL ESCALATION TESTS
# ============================================================================

class TestDerivativeClassificationLevels:
    """Tests for classification level escalation - highest level wins."""
    
    @pytest.mark.parametrize("level1,level2,expected", [
        ("UNCLASSIFIED", "CONFIDENTIAL", "CONFIDENTIAL"),
        ("UNCLASSIFIED", "SECRET", "SECRET"),
        ("UNCLASSIFIED", "TOP SECRET", "TOP SECRET"),
        ("CONFIDENTIAL", "SECRET", "SECRET"),
        ("CONFIDENTIAL", "TOP SECRET", "TOP SECRET"),
        ("SECRET", "TOP SECRET", "TOP SECRET"),
        # Order independence tests
        ("CONFIDENTIAL", "UNCLASSIFIED", "CONFIDENTIAL"),
        ("SECRET", "UNCLASSIFIED", "SECRET"),
        ("TOP SECRET", "UNCLASSIFIED", "TOP SECRET"),
        ("SECRET", "CONFIDENTIAL", "SECRET"),
        ("TOP SECRET", "CONFIDENTIAL", "TOP SECRET"),
        ("TOP SECRET", "SECRET", "TOP SECRET"),
    ])
    def test_derivative_level_escalation(self, encoder, level1, level2, expected):
        """Test classification level escalation rules."""
        mask1 = encoder.parseClassificationString(level1)
        mask2 = encoder.parseClassificationString(level2)
        expected_mask = encoder.parseClassificationString(expected)
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected_mask, f"{level1} + {level2}: Got {newmask:08X}, expected {expected_mask:08X}"


# ============================================================================
# DISTRIBUTION MARKING TESTS
# ============================================================================

class TestDerivativeDistributionMarkings:
    """Tests for distribution marking merging - most restrictive wins."""
    
    @pytest.mark.parametrize("dist1,dist2,expected", [
        # NOFORN is most restrictive
        ("NOFORN", "REL TO FVEY", "NOFORN"),
        ("REL TO FVEY", "NOFORN", "NOFORN"),
        ("NOFORN", "REL TO NATO", "NOFORN"),
        ("REL TO NATO", "NOFORN", "NOFORN"),
        # Same markings
        ("NOFORN", "NOFORN", "NOFORN"),
        ("REL TO FVEY", "REL TO FVEY", "REL TO FVEY"),
        ("REL TO NATO", "REL TO NATO", "REL TO NATO"),
        # FVEY more restrictive than NATO
        ("REL TO NATO", "REL TO FVEY", "REL TO FVEY"),
        ("REL TO FVEY", "REL TO NATO", "REL TO FVEY"),
        # 9EYES more restrictive than 14EYES
        ("REL TO 9EYES", "REL TO 14EYES", "REL TO 9EYES"),
        ("REL TO 14EYES", "REL TO 9EYES", "REL TO 9EYES"),
        # No distribution markings
        ("", "", ""),
    ])
    def test_derivative_distribution_markings(self, encoder, dist1, dist2, expected):
        """Test distribution marking merging rules."""
        base_class = "SECRET"
        mask1 = encoder.parseClassificationString(f"{base_class}//{dist1}" if dist1 else base_class)
        mask2 = encoder.parseClassificationString(f"{base_class}//{dist2}" if dist2 else base_class)
        expected_str = f"{base_class}//{expected}" if expected else base_class
        expected_mask = encoder.parseClassificationString(expected_str)
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected_mask, f"{dist1} + {dist2}: Got {newmask:08X}, expected {expected_mask:08X}"


# ============================================================================
# SCI COMPARTMENT TESTS
# ============================================================================

class TestDerivativeSCICompartments:
    """Tests for SCI compartment merging - union of compartments."""
    
    def test_derivative_SI_no_SI(self, encoder):
        """SI + no SI = SI."""
        mask1 = encoder.parseClassificationString("TOP SECRET//SI//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//NOFORN")
        expected = encoder.parseClassificationString("TOP SECRET//SI//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_SI_SI(self, encoder):
        """SI + SI = SI."""
        mask1 = encoder.parseClassificationString("TOP SECRET//SI//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//SI//NOFORN")
        expected = encoder.parseClassificationString("TOP SECRET//SI//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_TK_no_TK(self, encoder):
        """TK + no TK = TK."""
        mask1 = encoder.parseClassificationString("TOP SECRET//TK//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//NOFORN")
        expected = encoder.parseClassificationString("TOP SECRET//TK//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_SI_TK_combined(self, encoder):
        """SI + TK = SI/TK (both compartments)."""
        mask1 = encoder.parseClassificationString("TOP SECRET//SI//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//TK//NOFORN")
        expected = encoder.parseClassificationString("TOP SECRET//SI/TK//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_HCS_no_HCS(self, encoder):
        """HCS + no HCS = HCS."""
        mask1 = encoder.parseClassificationString("TOP SECRET//HCS//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//NOFORN")
        expected = encoder.parseClassificationString("TOP SECRET//HCS//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_HCS_P_HCS_O(self, encoder):
        """HCS-P + HCS-O = both HCS variants."""
        mask1 = encoder.parseClassificationString("TOP SECRET//HCS-P//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//HCS-O//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        bits = BitmaskManager(newmask)
        assert bits.is_bit_set(NamedBits.HCS.value), "HCS bit should be set"
        assert bits.is_bit_set(NamedBits.HCS_P.value), "HCS-P bit should be set"
        assert bits.is_bit_set(NamedBits.HCS_O.value), "HCS-O bit should be set"

    def test_derivative_SI_GAMMA(self, encoder):
        """SI-GAMMA should be preserved."""
        mask1 = encoder.parseClassificationString("TOP SECRET//SI-G//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//NOFORN")
        expected = encoder.parseClassificationString("TOP SECRET//SI-G//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_SI_GAMMA_no_GAMMA(self, encoder):
        """GAMMA + no GAMMA = GAMMA."""
        mask1 = encoder.parseClassificationString("TOP SECRET//SI-G//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//SI//NOFORN")
        expected = encoder.parseClassificationString("TOP SECRET//SI-G//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"


# ============================================================================
# SAP PROGRAM TESTS
# ============================================================================

class TestDerivativeSAPPrograms:
    """Tests for SAP program merging - union of programs."""
    
    def test_derivative_SAP_no_SAP(self, encoder_with_sap):
        """SAP + no SAP = SAP."""
        mask1 = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-ALPHA//NOFORN")
        mask2 = encoder_with_sap.parseClassificationString("TOP SECRET//NOFORN")
        expected = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-ALPHA//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_SAP_SAP_same(self, encoder_with_sap):
        """Same SAP + same SAP = SAP."""
        mask1 = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-ALPHA//NOFORN")
        mask2 = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-ALPHA//NOFORN")
        expected = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-ALPHA//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_SAP_SAP_different(self, encoder_with_sap):
        """Different SAPs should both be present."""
        mask1 = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-ALPHA//NOFORN")
        mask2 = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-BRAVO//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        bits = BitmaskManager(newmask)
        assert bits.is_bit_set(NamedBits.SAP_A.value), "SAP-A bit should be set"
        assert bits.is_bit_set(NamedBits.SAP_B.value), "SAP-B bit should be set"

    def test_derivative_SAP_with_SI(self, encoder_with_sap):
        """SAP + SI should merge both."""
        mask1 = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-ALPHA//NOFORN")
        mask2 = encoder_with_sap.parseClassificationString("TOP SECRET//SI//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        bits = BitmaskManager(newmask)
        assert bits.is_bit_set(NamedBits.SAP_A.value), "SAP-A bit should be set"
        assert bits.is_bit_set(NamedBits.SI.value), "SI bit should be set"
        assert bits.is_bit_set(NamedBits.SCI.value), "SCI bit should be set"

    def test_derivative_multiple_SAP_programs(self, encoder_with_sap):
        """Multiple SAP programs should all be preserved."""
        mask1 = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-ALPHA//NOFORN")
        mask2 = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-BRAVO//NOFORN")
        mask3 = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-CHARLIE//NOFORN")
        
        # First merge
        newmask1 = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        # Then merge with third
        newmask2 = DerivativeClassificationEncoder.constructClassificationString(newmask1, mask3)
        
        bits = BitmaskManager(newmask2)
        assert bits.is_bit_set(NamedBits.SAP_A.value), "SAP-A bit should be set"
        assert bits.is_bit_set(NamedBits.SAP_B.value), "SAP-B bit should be set"
        assert bits.is_bit_set(NamedBits.SAP_C.value), "SAP-C bit should be set"


# ============================================================================
# SI GROUP TESTS
# ============================================================================

class TestDerivativeSIGroups:
    """Tests for SI group merging - union of groups."""
    
    def test_derivative_SI_GROUPA_no_group(self, encoder_with_si_groups):
        """SI-GROUPA + no group = SI-GROUPA."""
        mask1 = encoder_with_si_groups.parseClassificationString("TOP SECRET//SI-ALPHA//NOFORN")
        mask2 = encoder_with_si_groups.parseClassificationString("TOP SECRET//SI//NOFORN")
        expected = encoder_with_si_groups.parseClassificationString("TOP SECRET//SI-ALPHA//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_SI_GROUPA_GROUPB(self, encoder_with_si_groups):
        """SI-GROUPA + SI-GROUPB = both groups."""
        mask1 = encoder_with_si_groups.parseClassificationString("TOP SECRET//SI-ALPHA//NOFORN")
        mask2 = encoder_with_si_groups.parseClassificationString("TOP SECRET//SI-BRAVO//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        bits = BitmaskManager(newmask)
        assert bits.is_bit_set(NamedBits.SI_GROUPA.value), "SI-GROUPA bit should be set"
        assert bits.is_bit_set(NamedBits.SI_GROUPB.value), "SI-GROUPB bit should be set"

    def test_derivative_SI_same_group(self, encoder_with_si_groups):
        """Same SI group should be preserved."""
        mask1 = encoder_with_si_groups.parseClassificationString("TOP SECRET//SI-ALPHA//NOFORN")
        mask2 = encoder_with_si_groups.parseClassificationString("TOP SECRET//SI-ALPHA//NOFORN")
        expected = encoder_with_si_groups.parseClassificationString("TOP SECRET//SI-ALPHA//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"


# ============================================================================
# COMPLEX MULTI-COMPARTMENT TESTS
# ============================================================================

class TestDerivativeComplex:
    """Complex multi-compartment derivative tests."""
    
    def test_derivative_complex_SAP_SI_TK(self, encoder_with_sap):
        """SAP + SI + TK should merge all compartments."""
        mask1 = encoder_with_sap.parseClassificationString("TOP SECRET//SAR-ALPHA//NOFORN")
        mask2 = encoder_with_sap.parseClassificationString("TOP SECRET//SI/TK//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        bits = BitmaskManager(newmask)
        assert bits.is_bit_set(NamedBits.SAP_A.value), "SAP-A bit should be set"
        assert bits.is_bit_set(NamedBits.SI.value), "SI bit should be set"
        assert bits.is_bit_set(NamedBits.TK.value), "TK bit should be set"
        assert bits.is_bit_set(NamedBits.SCI.value), "SCI bit should be set"
        assert bits.is_bit_set(NamedBits.NOFORN.value), "NOFORN bit should be set"

    def test_derivative_complex_different_levels_compartments(self, encoder):
        """SECRET//SI + TOP SECRET//TK = TOP SECRET//SI/TK."""
        mask1 = encoder.parseClassificationString("SECRET//SI//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//TK//NOFORN")
        expected = encoder.parseClassificationString("TOP SECRET//SI/TK//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_complex_HCS_SI_TK(self, encoder):
        """HCS + SI + TK should merge all."""
        mask1 = encoder.parseClassificationString("TOP SECRET//HCS//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//SI/TK//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        bits = BitmaskManager(newmask)
        assert bits.is_bit_set(NamedBits.HCS.value), "HCS bit should be set"
        assert bits.is_bit_set(NamedBits.SI.value), "SI bit should be set"
        assert bits.is_bit_set(NamedBits.TK.value), "TK bit should be set"
        assert bits.is_bit_set(NamedBits.SCI.value), "SCI bit should be set"

    def test_derivative_complex_distribution_escalation(self, encoder):
        """Different distributions with compartments - NOFORN wins."""
        mask1 = encoder.parseClassificationString("SECRET//SI//REL TO FVEY")
        mask2 = encoder.parseClassificationString("SECRET//TK//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        bits = BitmaskManager(newmask)
        assert bits.is_bit_set(NamedBits.SI.value), "SI bit should be set"
        assert bits.is_bit_set(NamedBits.TK.value), "TK bit should be set"
        assert bits.is_bit_set(NamedBits.NOFORN.value), "NOFORN bit should be set"


# ============================================================================
# CUI/SBU TESTS
# ============================================================================

class TestDerivativeCUI:
    """Tests for CUI/SBU derivative classification."""
    
    def test_derivative_CUI_CUI(self, encoder):
        """CUI + CUI = CUI."""
        mask1 = encoder.parseClassificationString("CUI")
        mask2 = encoder.parseClassificationString("CUI")
        expected = encoder.parseClassificationString("CUI")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_CUI_SBU(self, encoder):
        """CUI + SBU should handle appropriately."""
        mask1 = encoder.parseClassificationString("CUI")
        mask2 = encoder.parseClassificationString("UNCLASSIFIED//SBU")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        bits = BitmaskManager(newmask)
        assert bits.is_bit_set(NamedBits.UNCLASSIFIED.value), "UNCLASSIFIED bit should be set"

    def test_derivative_SBU_SBU(self, encoder):
        """SBU + SBU = SBU."""
        mask1 = encoder.parseClassificationString("UNCLASSIFIED//SBU")
        mask2 = encoder.parseClassificationString("UNCLASSIFIED//SBU")
        expected = encoder.parseClassificationString("UNCLASSIFIED//SBU")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_CUI_classified(self, encoder):
        """CUI + classified = classified level."""
        mask1 = encoder.parseClassificationString("CUI")
        mask2 = encoder.parseClassificationString("SECRET")
        expected = encoder.parseClassificationString("SECRET")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestDerivativeEdgeCases:
    """Edge case tests."""
    
    def test_derivative_GAMMA_GAMMA(self, encoder):
        """GAMMA + GAMMA = GAMMA."""
        mask1 = encoder.parseClassificationString("TOP SECRET//SI-G//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//SI-G//NOFORN")
        expected = encoder.parseClassificationString("TOP SECRET//SI-G//NOFORN")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        assert newmask == expected, f"Got {newmask:08X}, expected {expected:08X}"

    def test_derivative_9eyes_14eyes(self, encoder):
        """9EYES + 14EYES should take most restrictive (9EYES)."""
        mask1 = encoder.parseClassificationString("SECRET//REL TO 9EYES")
        mask2 = encoder.parseClassificationString("SECRET//REL TO 14EYES")
        newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        bits = BitmaskManager(newmask)
        assert bits.is_bit_set(NamedBits.RELTO_NINEEYES.value), "9EYES bit should be set"

    def test_derivative_commutativity(self, encoder):
        """Derivative classification should be commutative (order independent)."""
        mask1 = encoder.parseClassificationString("SECRET//SI//NOFORN")
        mask2 = encoder.parseClassificationString("TOP SECRET//TK//REL TO FVEY")
        
        result1 = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        result2 = DerivativeClassificationEncoder.constructClassificationString(mask2, mask1)
        
        assert result1 == result2, f"Order matters: {result1:08X} != {result2:08X}"

    def test_derivative_associativity(self, encoder):
        """Derivative classification should be associative."""
        mask1 = encoder.parseClassificationString("SECRET//SI//NOFORN")
        mask2 = encoder.parseClassificationString("CONFIDENTIAL//TK//REL TO FVEY")
        mask3 = encoder.parseClassificationString("TOP SECRET//HCS//NOFORN")
        
        # (mask1 + mask2) + mask3
        result1 = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
        result1 = DerivativeClassificationEncoder.constructClassificationString(result1, mask3)
        
        # mask1 + (mask2 + mask3)
        result2 = DerivativeClassificationEncoder.constructClassificationString(mask2, mask3)
        result2 = DerivativeClassificationEncoder.constructClassificationString(mask1, result2)
        
        assert result1 == result2, f"Associativity failed: {result1:08X} != {result2:08X}"


##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##
