#!/usr/bin/env python3
"""Quick verification that the NOFORN bug is fixed."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.classification_encoder import ClassificationEncoder, DerivativeClassificationEncoder

def test_noforn_preserved():
    """Test that NOFORN + NOFORN = NOFORN (not lost)."""
    encoder = ClassificationEncoder(None)
    
    mask1 = encoder.parseClassificationString("SECRET//NOFORN")
    mask2 = encoder.parseClassificationString("SECRET//NOFORN")
    expected = encoder.parseClassificationString("SECRET//NOFORN")
    
    result = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
    
    print(f"Mask1 (SECRET//NOFORN):  {mask1:08X}")
    print(f"Mask2 (SECRET//NOFORN):  {mask2:08X}")
    print(f"Result:                  {result:08X}")
    print(f"Expected:                {expected:08X}")
    print(f"Match: {result == expected}")
    
    if result == expected:
        print("\n✓ FIX VERIFIED: NOFORN is correctly preserved!")
        return True
    else:
        print("\n✗ BUG STILL EXISTS: NOFORN was lost!")
        # Debug: show what we got
        result_str = encoder.formatClassificationString(result)
        print(f"Result string: {result_str}")
        return False

if __name__ == "__main__":
    success = test_noforn_preserved()
    sys.exit(0 if success else 1)
