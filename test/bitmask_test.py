import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))


from classification_encoder import BitmaskManager, NamedBits

def test_basic_bitmask_operations():
    bm = BitmaskManager()
    
    # Initially, all bits should be clear
    assert bm.bitmask == 0x00000000
    
    # Set a bit and check
    bm.set_bit(0x00000001)
    assert bm.is_bit_set(0x00000001) == True
    assert bm.bitmask == 0x00000001
    
    # Clear the bit and check
    bm.clear_bit(0x00000001)
    assert bm.is_bit_set(0x00000001) == False
    assert bm.bitmask == 0x00000000

def test_named_bit_operations():
    bm = BitmaskManager()
    
    # Set a named bit and check
    bm.setNamedBit(NamedBits.UNCLASSIFIED)
    assert bm.is_bit_set(NamedBits.UNCLASSIFIED.value) == True
    
    # Clear the named bit and check
    bm.clearNamedBit(NamedBits.UNCLASSIFIED)
    assert bm.is_bit_set(NamedBits.UNCLASSIFIED.value) == False

def test_nibble_and_byte_extraction():
    bm = BitmaskManager()
    bm.bitmask = 0x12345678
    
    assert bm.getFirstNibble() == 0x1
    assert bm.getSecondNibble() == 0x2
    assert bm.getThirdNibble() == 0x3
    assert bm.getFouthNibble() == 0x4
    assert bm.getFifthNibble() == 0x5
    assert bm.getSixthNibble() == 0x6
    assert bm.getSeventhNibble() == 0x7
    assert bm.getEighthNibble() == 0x8
    
    assert bm.getFirstByte() == 0x12
    assert bm.getSecondByte() == 0x34
    assert bm.getThirdByte() == 0x56
    assert bm.getForthByte() == 0x78