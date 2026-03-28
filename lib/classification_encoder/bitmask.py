##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##

import os
import sys
from enum import Enum
from json import loads as json_loads
from typing import List


'''
The NamedBits enum defines named constants for each bit in the classification bitmask.
'''
class NamedBits(Enum):
    RELTO_NINEEYES = 0x00000001
    RELTO_FOURTEENEYES = 0x00000002
    RELTO_C = 0x00000004
    RELTO_B = 0x00000008
    RELTO_A = 0x00000010
    RELTO_FVEY = 0x00000020
    RELTO_NATO = 0x00000040
    RELIDO = 0x00000100
    NOFORN = 0x00000080
    SBU = 0x00001000
    CUI = 0x00002000
    HCS = 0x00010000
    HCS_P = 0x00004000
    HCS_O = 0x00008000
    SI = 0x00040000
    TK = 0x00080000
    GAMMA = 0x00100000
    SI_GROUPA = 0x00200000
    SI_GROUPB = 0x00400000
    SI_GROUPC = 0x00800000
    SCI = 0x01000000
    SAP_A = 0x02000000
    SAP_B = 0x04000000
    SAP_C = 0x08000000 
    UNCLASSIFIED = 0x10000000 
    CONFIDENTIAL = 0x20000000 
    SECRET = 0x40000000 
    TOPSECRET = 0x80000000

'''
The BitmaskManager class provides methods for managing a classification bitmask.
'''
class BitmaskManager:
    def __init__(self, VAL: int = 0x00000000):
        """
        Initialize the BitmaskManager.
        
        Args:
            VAL: Initial bitmask value (default: 0x00000000)
        """
        self.bitmask = VAL

    def set_bit(self, bit: int) -> None:
        """Set a specific bit in the bitmask."""
        self.bitmask |= bit

    def clear_bit(self, bit: int) -> None:
        """Clear a specific bit in the bitmask."""
        self.bitmask &= ~bit

    def is_bit_set(self, bit: int) -> bool:
        """Check if a specific bit is set in the bitmask."""
        return (self.bitmask & bit) != 0
    
    def setNamedBit(self, namedbit: NamedBits) -> None:
        """
        Set a bit using a NamedBits enum value.
        
        Args:
            namedbit: NamedBits enum value
            
        Raises:
            ValueError: If namedbit is not a NamedBits enum
        """
        if not isinstance(namedbit, NamedBits):
            raise ValueError(f"Expected a NamedBits enum value, got {type(namedbit)}")
        self.set_bit(namedbit.value)

    def anyBitSet(self, bitList: List[int]) -> bool:
        """
        Check if any bit in a list is set.
        
        Args:
            bitList: List of bit values to check
            
        Returns:
            True if any bit is set, False otherwise
        """
        for namedBit in bitList:
            if self.is_bit_set(namedBit):
                return True
        return False

    def anyNamedBitsSet(self, bitList: List[NamedBits]) -> bool:
        """
        Check if any NamedBits in a list is set.
        
        Args:
            bitList: List of NamedBits enum values
            
        Returns:
            True if any bit is set, False otherwise
        """
        for namedBit in bitList:
            if not isinstance(namedBit, NamedBits):
                continue
            if self.is_bit_set(namedBit.value):
                return True
        return False

    def clearNamedBit(self, namedbit: NamedBits) -> None:
        """
        Clear a bit using a NamedBits enum value.
        
        Args:
            namedbit: NamedBits enum value
            
        Raises:
            ValueError: If namedbit is not a NamedBits enum
        """
        if not isinstance(namedbit, NamedBits):
            raise ValueError(f"Expected a NamedBits enum value, got {type(namedbit)}")
        self.clear_bit(namedbit.value)
    
    def getFirstNibble(self) -> int:
        """Get the first (most significant) nibble (4 bits) of the bitmask."""
        return self.bitmask & 0xF
    
    def getSecondNibble(self) -> int:
        """Get the second nibble of the bitmask."""
        return (self.bitmask >> 4) & 0xF   
    
    def getThirdNibble(self) -> int:
        """Get the third nibble of the bitmask."""
        return (self.bitmask >> 8) & 0xF
    
    def getFourthNibble(self) -> int:
        """Get the fourth nibble of the bitmask."""
        return (self.bitmask >> 12) & 0xF
        
    def getFifthNibble(self) -> int:
        """Get the fifth nibble of the bitmask."""
        return (self.bitmask >> 16) & 0xF
    
    def getSixthNibble(self) -> int:
        """Get the sixth nibble of the bitmask."""
        return (self.bitmask >> 20) & 0xF    
    
    def getSeventhNibble(self) -> int:
        """Get the seventh nibble of the bitmask."""
        return (self.bitmask >> 24) & 0xF
    
    def getEighthNibble(self) -> int:
        """Get the eighth (least significant) nibble of the bitmask."""
        return (self.bitmask >> 28) & 0xF
    
    def getFirstByte(self) -> int:
        """Get the first (most significant) byte of the bitmask."""
        return self.bitmask  & 0xFF
    
    def getSecondByte(self) -> int:
        """Get the second byte of the bitmask."""
        return (self.bitmask >> 8) & 0xFF
    
    def getThirdByte(self) -> int:
        """Get the third byte of the bitmask."""
        return (self.bitmask >> 16) & 0xFF
    
    def getFourthByte(self) -> int:
        """Get the fourth (least significant) byte of the bitmask."""
        return (self.bitmask >> 24) & 0xFF

    def anySet(self, bitlist: List[int]) -> bool:
        """
        Check if any bit in a list is set.
        
        Args:
            bitlist: List of bit values
            
        Returns:
            True if any bit is set, False otherwise
        """
        for bit in bitlist:
            if self.is_bit_set(bit):
                return True
        return False

    def anySCISet(self) -> bool:
        """Check if any SCI (Sensitive Compartmented Information) bit is set."""
        return self.anySet([NamedBits.SI_GROUPA.value, NamedBits.SI_GROUPB.value, 
            NamedBits.SI_GROUPC.value, NamedBits.SI.value, NamedBits.TK.value,
            NamedBits.GAMMA.value, NamedBits.HCS.value])
    
    def anySIGroup(self) -> bool:
        """Check if any SI group bit is set."""
        return self.anySet([NamedBits.SI_GROUPA.value, NamedBits.SI_GROUPB.value, 
            NamedBits.SI_GROUPC.value, NamedBits.GAMMA.value])

    def anyRelto(self) -> bool:
        """Check if any RELTO (release to) bit is set."""
        if self.anySet([NamedBits.RELTO_NINEEYES.value, NamedBits.RELTO_FOURTEENEYES.value, 
            NamedBits.RELTO_C.value, NamedBits.RELTO_B.value, NamedBits.RELTO_A.value,
            NamedBits.RELTO_FVEY.value, NamedBits.RELTO_NATO.value]):
            return True
        return False

##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##
