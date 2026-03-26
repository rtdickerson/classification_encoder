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
    
    assert bm.getFirstNibble() == 0x8, f"got 0x{bm.getFirstNibble:x}"
    assert bm.getSecondNibble() == 0x7, f"got 0x{bm.getSecondNibble:x}"
    assert bm.getThirdNibble() == 0x6, f"got 0x{bm.getThirdNibble:x}"
    assert bm.getFourthNibble() == 0x5, f"got 0x{bm.getFourthNibble:x}"
    assert bm.getFifthNibble() == 0x4, f"got 0x{bm.getFifthNibble:x}"
    assert bm.getSixthNibble() == 0x3, f"got 0x{bm.getSixthNibble:x}"
    assert bm.getSeventhNibble() == 0x2, f"got 0x{bm.getSeventhNibble:x}"
    assert bm.getEighthNibble() == 0x1, f"got 0x{bm.getEighthNibble:x}"
    
    assert bm.getFirstByte() == 0x78, f"got 0x{bm.getFirstByte():x}"
    assert bm.getSecondByte() == 0x56, f"got 0x{bm.getSecondByte():x}"
    assert bm.getThirdByte() == 0x34, f"got 0x{bm.getThirdByte():x}"
    assert bm.getFourthByte() == 0x12, f"got 0x{bm.getFourthByte():x}"

def test_nibblecheck():
    bm = BitmaskManager()
    bm.bitmask = 0x87654321

    assert bm.getEighthNibble() == 0x8
    assert bm.is_bit_set(NamedBits.TOPSECRET.value) == True
