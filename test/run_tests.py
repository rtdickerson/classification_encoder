#!/usr/bin/env python3
import sys
import os

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from classification_encoder import ClassificationEncoder, NamedBits, DerivativeClassificationEncoder

print("Testing derivative classification...")
print("=" * 60)

# Test 1: Basic functionality
print("\nTest 1: Basic edge cases")
ce = ClassificationEncoder(None)
mask = ce.parseClassificationString("UNCLASSIFIED")
newmask = DerivativeClassificationEncoder.constructClassificationString(mask, 0)
assert newmask == mask, f"Test 1a failed: Got {newmask:08X}"
print("✓ Test 1a passed: UNCLASSIFIED with 0")

newmask = DerivativeClassificationEncoder.constructClassificationString(0, mask)
assert newmask == mask, f"Test 1b failed: Got {newmask:08X}"
print("✓ Test 1b passed: 0 with UNCLASSIFIED")

# Test 2: Classification escalation
print("\nTest 2: Classification escalation")
mask1 = ce.parseClassificationString("UNCLASSIFIED")
mask2 = ce.parseClassificationString("CONFIDENTIAL")
expected = ce.parseClassificationString("CONFIDENTIAL")
newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
assert newmask == expected, f"Test 2 failed: Got {newmask:08X}, expected {expected:08X}"
print("✓ Test 2 passed: U + C = C")

mask1 = ce.parseClassificationString("CONFIDENTIAL")
mask2 = ce.parseClassificationString("SECRET")
expected = ce.parseClassificationString("SECRET")
newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
assert newmask == expected, f"Test 2b failed: Got {newmask:08X}, expected {expected:08X}"
print("✓ Test 2b passed: C + S = S")

mask1 = ce.parseClassificationString("SECRET")
mask2 = ce.parseClassificationString("TOP SECRET")
expected = ce.parseClassificationString("TOP SECRET")
newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
assert newmask == expected, f"Test 2c failed: Got {newmask:08X}, expected {expected:08X}"
print("✓ Test 2c passed: S + TS = TS")

# Test 3: NOFORN vs FVEY
print("\nTest 3: NOFORN vs FVEY (NOFORN should win)")
mask1 = ce.parseClassificationString("SECRET//NOFORN")
mask2 = ce.parseClassificationString("SECRET//REL TO FVEY")
expected = ce.parseClassificationString("SECRET//NOFORN")
newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
assert newmask == expected, f"Test 3 failed: Got {newmask:08X}, expected {expected:08X}"
print("✓ Test 3 passed: NOFORN + FVEY = NOFORN")

# Test 4: FVEY vs NATO
print("\nTest 4: FVEY vs NATO (FVEY should win)")
mask1 = ce.parseClassificationString("SECRET//REL TO FVEY")
mask2 = ce.parseClassificationString("SECRET//REL TO NATO")
expected = ce.parseClassificationString("SECRET//REL TO FVEY")
newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
assert newmask == expected, f"Test 4 failed: Got {newmask:08X}, expected {expected:08X}"
print("✓ Test 4 passed: FVEY + NATO = FVEY")

# Test 5: SCI preservation
print("\nTest 5: SCI preservation")
cfg = {
    'sap-a': "SAP-ALPHA",
    'si-groupa': 'ALPHA',
}
ce2 = ClassificationEncoder(cfg)
mask1 = ce2.parseClassificationString("SECRET//SCI//NOFORN")
mask2 = ce2.parseClassificationString("SECRET//REL TO FVEY")
expected = ce2.parseClassificationString("SECRET//SCI//NOFORN")
newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
assert newmask == expected, f"Test 5 failed: Got {newmask:08X}, expected {expected:08X}"
print("✓ Test 5 passed: SCI preserved")

# Test 6: Higher classification with SCI
print("\nTest 6: Higher classification with SCI")
mask1 = ce2.parseClassificationString("SECRET//SCI//NOFORN")
mask2 = ce2.parseClassificationString("TOP SECRET//REL TO FVEY")
expected = ce2.parseClassificationString("TOP SECRET//SCI//NOFORN")
newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
assert newmask == expected, f"Test 6 failed: Got {newmask:08X}, expected {expected:08X}"
print("✓ Test 6 passed: TS + SCI + NOFORN")

# Test 7: SI compartment merging
print("\nTest 7: SI compartment merging")
cfg = {'si-groupa': 'ALPHA', 'si-groupb': 'BRAVO'}
ce3 = ClassificationEncoder(cfg)
mask1 = ce3.parseClassificationString("SECRET//SI-ALPHA//NOFORN")
mask2 = ce3.parseClassificationString("SECRET//SI-BRAVO//NOFORN")
newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
assert (newmask & NamedBits.SCI.value) != 0, "Test 7 failed: SCI should be set"
assert (newmask & NamedBits.SI.value) != 0, "Test 7 failed: SI should be set"
# At least one SI group should be set
assert ((newmask & NamedBits.SI_GROUPA.value) != 0 or 
        (newmask & NamedBits.SI_GROUPB.value) != 0), "Test 7 failed: SI groups should be merged"
print("✓ Test 7 passed: SI compartments merged")

# Test 8: Commutative property
print("\nTest 8: Commutative property")
mask1 = ce.parseClassificationString("SECRET//NOFORN")
mask2 = ce.parseClassificationString("TOP SECRET//REL TO FVEY")
result1 = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
result2 = DerivativeClassificationEncoder.constructClassificationString(mask2, mask1)
assert result1 == result2, f"Test 8 failed: {result1:08X} vs {result2:08X}"
print("✓ Test 8 passed: Order doesn't matter")

print("\n" + "=" * 60)
print("All tests passed! ✓")
