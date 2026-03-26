##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##

import os
import sys
from enum import Enum

from .bitmask import BitmaskManager
from .bitmask import NamedBits

class MaskComparatorClass:
    """
    Utility class for comparing classification bitmasks.
    
    Provides static methods to compare classification levels and determine
    which classification is more restrictive.
    """

    COMPARE_EQUAL = 0
    COMPARE_FIRST = -1
    COMPARE_SECOND = 1
    COMPARE_THIRD = 2

    # 0x4000000
    #   ^--- this nibble is the classification level, so we can compare that first 
    # 
    @staticmethod
    def getClassificationLevel(mask: BitmaskManager) -> int:
        """
        Extract the classification level from a bitmask.
        
        Args:
            mask: Classification bitmask
            
        Returns:
            Classification level (0-15)
        """
        
        return mask.getEighthNibble()


    @staticmethod
    def getSCI(mask: BitmaskManager) -> bool:
        """Check if SCI bit is set."""
        return mask.is_bit_set(NamedBits.SCI.value)

    @staticmethod
    def getSAP(mask: BitmaskManager) -> int:
        result = 0
        if mask.is_bit_set(NamedBits.SAP_A.value):
            result += 1
        if mask.is_bit_set(NamedBits.SAP_B.value):
            result += 1
        if mask.is_bit_set(NamedBits.SAP_C.value):
            result += 1
        return result

    @staticmethod
    def getSIGroups(mask: BitmaskManager) -> bool:
        """Check if any SI group bits are set."""
        return mask.anyNamedBitsSet([NamedBits.SI_GROUPA, 
            NamedBits.SI_GROUPB, 
            NamedBits.SI_GROUPC,
            NamedBits.GAMMA])

    @staticmethod
    def getSIBit(mask: BitmaskManager) -> bool:
        """Check if SI bit is set."""
        return mask.is_bit_set(NamedBits.SI.value)

    @staticmethod
    def getTKBit(mask: BitmaskManager) -> bool:
        """Check if TK bit is set."""
        return mask.is_bit_set(NamedBits.TK.value)    

    @staticmethod
    def getHCSBit(mask: BitmaskManager) -> bool:
        """Check if HCS bit is set."""
        return mask.is_bit_set(NamedBits.HCS.value)

    @staticmethod
    def getCUIBit(mask: BitmaskManager) -> bool:
        """Check if CUI bit is set."""
        return mask.is_bit_set(NamedBits.CUI.value)

    @staticmethod
    def getUnclassifiedBit(mask: BitmaskManager) -> bool:
        """Check if UNCLASSIFIED bit is set."""
        return mask.is_bit_set(NamedBits.UNCLASSIFIED.value)

    @staticmethod
    def getSAP(mask: BitmaskManager) -> bool:
        """Check if any SAP bits are set."""
        return mask.anyNamedBitsSet([NamedBits.SAP_A, NamedBits.SAP_B,
                                  NamedBits.SAP_C])

    @staticmethod
    def getNOFORN(mask: BitmaskManager) -> bool:
        """Check if NOFORN bit is set."""
        return mask.is_bit_set(NamedBits.NOFORN.value)

    @staticmethod
    def getFVEY(mask: BitmaskManager) -> bool:
        """Check if FVEY bit is set."""
        return mask.is_bit_set(NamedBits.RELTO_FVEY.value)
        
    @staticmethod
    def getNATO(mask: BitmaskManager) -> bool:
        """Check if NATO bit is set."""
        return mask.is_bit_set(NamedBits.RELTO_NATO.value)

    @staticmethod
    def checkRelto(nb: NamedBits, mask1: BitmaskManager, mask2: BitmaskManager) -> int:
        """
        Check RELTO bits in two masks and compare.
        
        Args:
            nb: NamedBits value to check
            mask1: First mask
            mask2: Second mask
            
        Returns:
            -1 if both have the bit set (equal)
            1 if only mask1 has it (mask1 more restrictive)
            2 if only mask2 has it (mask2 more restrictive)
            0 if neither has it
        """
        if mask1.is_bit_set(nb.value) and mask2.is_bit_set(nb.value):
            return -1
        if mask1.is_bit_set(nb.value) and not mask2.is_bit_set(nb.value):
            return 1
        elif not mask1.is_bit_set(nb.value) and mask2.is_bit_set(nb.value):
            return 2 
        return 0
        

    @staticmethod
    def compareTwo(mask1: int, mask2: int) -> int:
        """
        Compare two classification masks.
        
        Args:
            mask1: First classification bitmask
            mask2: Second classification bitmask
            
        Returns:
            COMPARE_EQUAL (0) if equal
            COMPARE_FIRST (-1) if mask1 is more restrictive
            COMPARE_SECOND (1) if mask2 is more restrictive
        """
        if mask1 == mask2:
            return MaskComparatorClass.COMPARE_EQUAL
        if mask1 == 0 and mask2 != 0:
            return MaskComparatorClass.COMPARE_SECOND 
        if mask2 == 0 and mask1 != 0:
            return MaskComparatorClass.COMPARE_FIRST
            
        bits1 = BitmaskManager(mask1)
        bits2 = BitmaskManager(mask2)

        # For now, just compare the classification levels
        C1 = MaskComparatorClass.getClassificationLevel(bits1)
        C2 = MaskComparatorClass.getClassificationLevel(bits2)
        if C1 > C2:
            return MaskComparatorClass.COMPARE_FIRST
        elif C2 > C1:
            return MaskComparatorClass.COMPARE_SECOND

        # Special handling for Unclassified
        if MaskComparatorClass.getUnclassifiedBit(bits1):
            if MaskComparatorClass.getCUIBit(bits1):
                if not MaskComparatorClass.getCUIBit(bits2):
                    return MaskComparatorClass.COMPARE_FIRST
                else:
                    return MaskComparatorClass.COMPARE_EQUAL
            else:
                if MaskComparatorClass.getCUIBit(bits2):
                    return MaskComparatorClass.COMPARE_SECOND
                else:
                    return MaskComparatorClass.COMPARE_EQUAL
                        
        # Classification is the same (e.g., SECRET : SECRET)
        # Check if there are SAP programs involved
        C1_SAP = MaskComparatorClass.getSAP(bits1)
        C2_SAP = MaskComparatorClass.getSAP(bits2)
        if C1_SAP > 0 and C2_SAP == 0:
            return MaskComparatorClass.COMPARE_FIRST
        if C2_SAP > 0 and C1_SAP == 0:
            return MaskComparatorClass.COMPARE_SECOND

        C1_SCI = MaskComparatorClass.getSCI(bits1)
        C2_SCI = MaskComparatorClass.getSCI(bits2)
        if C1_SCI and not C2_SCI:
            return MaskComparatorClass.COMPARE_FIRST
        if C2_SCI and not C1_SCI:
            return MaskComparatorClass.COMPARE_SECOND
        
        C1_SIG = MaskComparatorClass.getSIGroups(bits1)
        C2_SIG = MaskComparatorClass.getSIGroups(bits2)
        if C1_SIG and not C2_SIG:
            return MaskComparatorClass.COMPARE_FIRST
        if C2_SIG and not C1_SIG:
            return MaskComparatorClass.COMPARE_SECOND

        if MaskComparatorClass.getSIBit(bits1) and not MaskComparatorClass.getSIBit(bits2):
            return MaskComparatorClass.COMPARE_FIRST
        if MaskComparatorClass.getSIBit(bits2) and not MaskComparatorClass.getSIBit(bits1):
            return MaskComparatorClass.COMPARE_SECOND
        
        if MaskComparatorClass.getTKBit(bits1) and not MaskComparatorClass.getTKBit(bits2):
            return MaskComparatorClass.COMPARE_FIRST
        if MaskComparatorClass.getTKBit(bits2) and not MaskComparatorClass.getTKBit(bits1):
            return MaskComparatorClass.COMPARE_SECOND

        # Everything is equal to here, look at distribution restrictions
        M_1 = mask1 & 0xFF
        M_2 = mask2 & 0xFF
        if M_1 == M_2:
            return MaskComparatorClass.COMPARE_EQUAL
            
        # You don't have to have dissemination controls
        if M_1 == 0 and M_2 != 0:
            return MaskComparatorClass.COMPARE_SECOND
        if M_1 != 0 and M_2 == 0:
            return MaskComparatorClass.COMPARE_FIRST

        # These seem to be in order from most to less restrictive
        for part in [NamedBits.NOFORN, NamedBits.RELTO_FVEY, NamedBits.RELTO_NATO,
                     NamedBits.RELTO_NINEEYES, NamedBits.RELTO_FOURTEENEYES]:
            V = MaskComparatorClass.checkRelto(part, bits1, bits2)
            if V == 1:
                return MaskComparatorClass.COMPARE_FIRST
            elif V == 2:
                return MaskComparatorClass.COMPARE_SECOND
            elif V == -1:
                return MaskComparatorClass.COMPARE_EQUAL

        # At this point all that remains is the custom REL TO groups
        # and we have no clear way to score them
        return MaskComparatorClass.COMPARE_EQUAL

##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##
