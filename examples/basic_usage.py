#!/usr/bin/env python
"""
Basic usage examples for classification_encoder library.

This script demonstrates the core functionality of the classification_encoder package.
"""

import sys
import os

# Add parent directory to path to import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from classification_encoder import ClassificationEncoder, NamedBits, CountryDatabase


def example_basic_encoding():
    """Demonstrate basic encoding and decoding."""
    print("=" * 60)
    print("Example 1: Basic Encoding and Decoding")
    print("=" * 60)
    
    ce = ClassificationEncoder(None)
    
    # Test various classification strings
    test_strings = [
        "UNCLASSIFIED",
        "CUI",
        "SECRET//NOFORN",
        "TOP SECRET//TK//NOFORN",
        "SECRET//REL TO FVEY",
        "TOP SECRET//SI-GAMMA/TK//REL TO AUS, CAN, NZL, GBR, USA",
    ]
    
    for classification in test_strings:
        mask = ce.encode(classification)
        decoded = ce.decode(mask)
        print(f"\nOriginal:  {classification}")
        print(f"Encoded:   0x{mask:08X}")
        print(f"Decoded:   {decoded}")


def example_custom_config():
    """Demonstrate custom configuration with SAP programs and SI groups."""
    print("\n" + "=" * 60)
    print("Example 2: Custom Configuration")
    print("=" * 60)
    
    # Define custom SAP programs and SI groups
    config = {
        'sap-a': 'PROGRAM ALPHA',
        'sap-b': 'PROGRAM BRAVO',
        'si-groupa': 'CODEWORDONE',
        'si-groupb': 'CODEWORDTWO',
        'relto-a': 'REL TO USA, GBR, CAN'
    }
    
    ce = ClassificationEncoder(config)
    
    test_strings = [
        "SECRET//SAR-PROGRAM ALPHA//NOFORN",
        "TOP SECRET//SAR-PROGRAM BRAVO//SI/CODEWORDONE/TK//NOFORN",
        "SECRET//REL TO USA, GBR, CAN",
    ]
    
    for classification in test_strings:
        mask = ce.encode(classification)
        decoded = ce.decode(mask)
        print(f"\nOriginal:  {classification}")
        print(f"Encoded:   0x{mask:08X}")
        print(f"Decoded:   {decoded}")


def example_comparison():
    """Demonstrate classification comparison."""
    print("\n" + "=" * 60)
    print("Example 3: Classification Comparison")
    print("=" * 60)
    
    ce = ClassificationEncoder(None)
    
    comparisons = [
        ("SECRET//NOFORN", "TOP SECRET//NOFORN"),
        ("SECRET//SCI//NOFORN", "SECRET//NOFORN"),
        ("UNCLASSIFIED", "SECRET"),
        ("SECRET//REL TO FVEY", "SECRET//REL TO FVEY"),
    ]
    
    for class1, class2 in comparisons:
        mask1 = ce.encode(class1)
        mask2 = ce.encode(class2)
        result = ce.compareTwo(mask1, mask2)
        
        print(f"\nComparing:")
        print(f"  1: {class1}")
        print(f"  2: {class2}")
        
        if result == ce.COMPARE_EQUAL:
            print("  Result: Equal")
        elif result == ce.COMPARE_FIRST:
            print("  Result: First is more restrictive")
        elif result == ce.COMPARE_SECOND:
            print("  Result: Second is more restrictive")


def example_country_codes():
    """Demonstrate country code handling."""
    print("\n" + "=" * 60)
    print("Example 4: Country Code Handling")
    print("=" * 60)
    
    db = CountryDatabase()
    
    # Test RELTO parsing
    test_reltos = [
        "REL TO US, GB, CA",
        "REL TO USA, GBR, CAN, AUS, NZL",
        "REL TO NATO",
    ]
    
    for relto in test_reltos:
        countries = db.parseAndValidateRelto(relto)
        print(f"\nInput:     {relto}")
        print(f"Parsed:    {', '.join(countries)}")
        
        # Check alliance memberships
        if db.isFVEY(countries):
            print("Alliance:  Five Eyes")
        elif db.isNineEyes(countries):
            print("Alliance:  Nine Eyes")
        elif db.isFourteenEyes(countries):
            print("Alliance:  Fourteen Eyes")
        elif db.isNATO(countries):
            print("Alliance:  NATO")
        else:
            print("Alliance:  Custom")


def example_bit_operations():
    """Demonstrate direct bit manipulation."""
    print("\n" + "=" * 60)
    print("Example 5: Direct Bit Operations")
    print("=" * 60)
    
    from classification_encoder import BitmaskManager
    
    bm = BitmaskManager()
    
    # Set some bits
    bm.setNamedBit(NamedBits.SECRET)
    bm.setNamedBit(NamedBits.SCI)
    bm.setNamedBit(NamedBits.SI)
    bm.setNamedBit(NamedBits.NOFORN)
    
    print(f"\nBitmask: 0x{bm.bitmask:08X}")
    print(f"Binary:  {bin(bm.bitmask)}")
    
    # Check nibbles
    print(f"\nFirst nibble (classification):  0x{bm.getFirstNibble():X}")
    print(f"Second nibble (SAP):             0x{bm.getSecondNibble():X}")
    print(f"Third nibble (SCI):              0x{bm.getThirdNibble():X}")
    print(f"Eighth nibble (distribution):    0x{bm.getEighthNibble():X}")
    
    # Check specific bits
    print(f"\nIs SECRET set?  {bm.is_bit_set(NamedBits.SECRET.value)}")
    print(f"Is SCI set?     {bm.is_bit_set(NamedBits.SCI.value)}")
    print(f"Is TK set?      {bm.is_bit_set(NamedBits.TK.value)}")
    print(f"Is NOFORN set?  {bm.is_bit_set(NamedBits.NOFORN.value)}")


def example_access_check():
    """Demonstrate access control checking."""
    print("\n" + "=" * 60)
    print("Example 6: Access Control Check")
    print("=" * 60)
    
    ce = ClassificationEncoder(None)
    
    # User's clearance
    user_clearance = ce.encode("TOP SECRET//SCI//SI//TK//REL TO FVEY")
    
    # Documents with various classifications
    documents = [
        ("Document A", "UNCLASSIFIED"),
        ("Document B", "SECRET//NOFORN"),
        ("Document C", "TOP SECRET//SI//NOFORN"),
        ("Document D", "TOP SECRET//SI/TK/HCS//NOFORN"),
    ]
    
    print(f"User clearance: {ce.decode(user_clearance)}")
    print(f"Clearance mask: 0x{user_clearance:08X}\n")
    
    for doc_name, doc_class in documents:
        doc_mask = ce.encode(doc_class)
        
        # Simple access check (this is a basic example)
        # In a real system, you'd need more sophisticated logic
        ce.bits.bitmask = doc_mask
        has_access = ce.checkAccess(user_clearance)
        
        print(f"{doc_name}:")
        print(f"  Classification: {doc_class}")
        print(f"  Access: {'✓ GRANTED' if has_access else '✗ DENIED'}")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Classification Encoder - Usage Examples".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        example_basic_encoding()
        example_custom_config()
        example_comparison()
        example_country_codes()
        example_bit_operations()
        example_access_check()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
