import os
import sys

from .bitmask import NamedBits
from .bitmask import BitmaskManager

class DerivativeClassificationEncoder:

    @staticmethod
    def constructClassificationString(mask1 : int, mask2 : int) -> int:
        bitmask1 = BitmaskManager(mask1)
        bitmask2 = BitmaskManager(mask2)

        # IF one or the other is 0, then there's nothing to merge
        result = BitmaskManager(0);
        if mask1 == 0 and mask2 == 0:
            return mask1
        elif mask1 == 0 and mask2 != 0:
            return mask2
        elif mask1 != 0 and mask2 == 0:
            return mask1

        # See who has the highest classification
        H = 0
        L1 = bitmask1.getEighthNibble()
        L2 = bitmask2.getEighthNibble()
        if L1 > L2:
            # First is higher
            H = L1
        elif L2 > L1:
            # Second is higher
            H = L2
        else:
            # They're the same, so just take one
            H = L2       

        if H == 0x01:
            result.set_bit(NamedBits.UNCLASSIFIED.value)
        elif H == 0x02:
            result.set_bit(NamedBits.CONFIDENTIAL.value)
        elif H == 0x04:
            result.set_bit(NamedBits.SECRET.value)
        elif H == 0x08:
            result.set_bit(NamedBits.TOPSECRET.value)

        # Merge the SCI containers.
        if bitmask1.is_bit_set(NamedBits.SCI.value) or bitmask2.is_bit_set(NamedBits.SCI.value):
            result.set_bit(NamedBits.SCI.value)
            # Any SAP containers need to be brought forward
            for bit in [NamedBits.SAP_A, NamedBits.SAP_B, NamedBits.SAP_C, NamedBits.SI, NamedBits.TK, NamedBits.HCS_P, NamedBits.HCS_O, NamedBits.GAMMA]:
                if bitmask1.is_bit_set(bit.value) or bitmask2.is_bit_set(bit.value):
                    result.set_bit(bit.value)
            for bit in [NamedBits.SI, NamedBits.SI_GROUPA, NamedBits.SI_GROUPB, NamedBits.SI_GROUPC, NamedBits.TK, NamedBits.HCS_P, NamedBits.HCS_O, NamedBits.GAMMA]:
                if bitmask1.is_bit_set(bit.value) and bitmask2.is_bit_set(bit.value):
                    result.set_bit(bit.value)

        # Now look at the distrbution markings.
        for bit in [NamedBits.RELIDO]:
            if bitmask1.is_bit_set(bit.value) or bitmask2.is_bit_set(bit.value):
                result.set_bit(bit.value)         

        ALLREL=[NamedBits.RELTO_FVEY, NamedBits.RELTO_NINEEYES, NamedBits.RELTO_FOURTEENEYES, 
             NamedBits.RELTO_NATO, NamedBits.RELTO_A, NamedBits.RELTO_B, NamedBits.RELTO_C]
        # if there is no relto on either, return as is.
        if not bitmask1.anyNamedBitsSet(ALLREL) and not bitmask2.anyNamedBitsSet(ALLREL):
            return result.bitmask
        
        # Most restrictive
        if bitmask1.is_bit_set(NamedBits.NOFORN.value) or bitmask2.is_bit_set(NamedBits.NOFORN.value):
            result.set_bit(NamedBits.NOFORN.value)
            return result.bitmask
        # FVEY is next
        if bitmask1.is_bit_set(NamedBits.RELTO_FVEY.value) or bitmask2.is_bit_set(NamedBits.RELTO_FVEY.value):
            result.set_bit(NamedBits.RELTO_FVEY.value)
            return result.bitmask
        # NINEEYES is next
        if bitmask1.is_bit_set(NamedBits.RELTO_NINEEYES.value) or bitmask2.is_bit_set(NamedBits.RELTO_NINEEYES.value):
            result.set_bit(NamedBits.RELTO_NINEEYES.value)
            return result.bitmask
        # FOURTEENEYES is next
        if bitmask1.is_bit_set(NamedBits.RELTO_FOURTEENEYES.value) or bitmask2.is_bit_set(NamedBits.RELTO_FOURTEENEYES.value):
            result.set_bit(NamedBits.RELTO_FOURTEENEYES.value)
            return result.bitmask
        # NATO is next
        if bitmask1.is_bit_set(NamedBits.RELTO_NATO.value) or bitmask2.is_bit_set(NamedBits.RELTO_NATO.value):
            result.set_bit(NamedBits.RELTO_NATO.value)
            return result.bitmask
        # OK, at this point we're into the custom groups A,B,C.
        # The only way to resolve this is to generate the minimual intersection set of 
        # countries.  For example, REL TO USA, CAN and REL TO USA, FRA  then REL TO USA is the only 
        # common element, and given we only handle the fixed lists in A, B and C,
        # we're going to punt to NOFORN in the interest of security.
        result.set_bit(NamedBits.NOFORN.value)
        return result.bitmask

