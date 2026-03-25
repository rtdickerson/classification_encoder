# classification_encoder

A Python library to encode/decode classification strings to/from easily used/stored unsigned 32-bit integers.

## Overview

This library provides a robust way to convert classification markings (like "SECRET//NOFORN" or "TOP SECRET//SCI//TK") into compact 32-bit integer representations and back. This is useful for:

- Efficient storage of classification levels in databases
- Fast comparison of classification restrictions
- Compact transmission of classification metadata
- Access control systems

## Bit Layout

```
|              ||              |
|      ||      ||      ||      |
+--++--++--++--++--++--++--++--+
    3         2         1    
10987654321098765432109876543210
|||||||||||||||||||||||||||||||+ 0x00000001 - RELTO_NINE_EYES
||||||||||||||||||||||||||||||+- 0x00000002 - RELTO_FOURTEEN_EYES
|||||||||||||||||||||||||||||+-- 0x00000004 - RELTO_C
||||||||||||||||||||||||||||+--- 0x00000008 - RELTO_B
|||||||||||||||||||||||||||+---- 0x00000010 - RELTO_A
||||||||||||||||||||||||||+----- 0x00000020 - RELTO_FVEY
|||||||||||||||||||||||||+------ 0x00000040 - RELTO_NATO
||||||||||||||||||||||||+------- 0x00000080 - NOFORN
|||||||||||||||||||||||+-------- 0x00000100 - RELIDO
||||||||||||||||||||||+--------- 0x00000200 - Reserved
|||||||||||||||||||||+---------- 0x00000400 - Reserved
||||||||||||||||||||+----------- 0x00000800 - Reserved
|||||||||||||||||||+------------ 0x00001000 - SBU
||||||||||||||||||+------------- 0x00002000 - CUI
|||||||||||||||||+-------------- 0x00004000 - Reserved
||||||||||||||||+--------------- 0x00008000 - Reserved
|||||||||||||||+---------------- 0x00010000 - HCS
||||||||||||||+----------------- 0x00020000 - Reserved
|||||||||||||+------------------ 0x00040000 - SI
||||||||||||+------------------- 0x00080000 - TK
|||||||||||+-------------------- 0x00100000 - "GAMMA"
||||||||||+--------------------- 0x00200000 - SI-GROUPA
|||||||||+---------------------- 0x00400000 - SI-GROUPB
||||||||+----------------------- 0x00800000 - SI-GROUPC
|||||||+------------------------ 0x01000000 - SCI
||||||+------------------------- 0x02000000 - SAP-A
|||||+-------------------------- 0x04000000 - SAP-B
||||+--------------------------- 0x08000000 - SAP-C 
|||+---------------------------- 0x10000000 - UNCLASSIFIED
||+----------------------------- 0x20000000 - CONFIDENTIAL
|+------------------------------ 0x40000000 - SECRET
+------------------------------- 0x80000000 - TOP SECRET
```

## Installation

### From source:

```bash
pip install -e .
```

### For development:

```bash
pip install -e ".[dev]"
# or
pip install -r requirements-dev.txt
```

## Usage

### Basic Encoding/Decoding

```python
from classification_encoder import ClassificationEncoder

# Create encoder with default configuration
ce = ClassificationEncoder(None)

# Encode a classification string to integer
mask = ce.parseClassificationString("SECRET//NOFORN")
print(f"Encoded: 0x{mask:08X}")  # Output: 0x40000080

# Decode back to string
classification = ce.constructClassificationString(mask)
print(f"Decoded: {classification}")  # Output: SECRET//NOFORN
```

### Using Aliases

```python
# encode() and decode() are aliases for convenience
mask = ce.encode("TOP SECRET//SCI//TK//NOFORN")
classification = ce.decode(mask)
```

### Custom Configuration

```python
# Define custom SAP programs, SI groups, and RELTO lists
config = {
    'sap-a': 'PROGRAM-ALPHA',
    'sap-b': 'PROGRAM-BRAVO',
    'si-groupa': 'CODEWORD-ONE',
    'si-groupb': 'CODEWORD-TWO',
    'relto-a': 'REL TO USA, GBR, CAN, AUS'
}

ce = ClassificationEncoder(config)

# Now you can use custom markings
mask = ce.encode("SECRET//SAR-PROGRAM-ALPHA//SI/CODEWORD-ONE//NOFORN")
```

### Comparing Classifications

```python
ce = ClassificationEncoder(None)

mask1 = ce.encode("SECRET//NOFORN")
mask2 = ce.encode("TOP SECRET//SCI//NOFORN")

result = ce.compareTwo(mask1, mask2)
if result == ce.COMPARE_FIRST:
    print("mask1 is more restrictive")
elif result == ce.COMPARE_SECOND:
    print("mask2 is more restrictive")
else:
    print("Classifications are equal")
```

### Checking Access

```python
# Check if a user's clearance allows access to a document
user_clearance = ce.encode("SECRET//SI//TK//REL TO FVEY")
document_classification = ce.encode("SECRET//NOFORN")

ce.bits.bitmask = document_classification
if ce.checkAccess(user_clearance):
    print("Access granted")
else:
    print("Access denied")
```

### Working with Country Codes

```python
from classification_encoder import CountryDatabase

db = CountryDatabase()

# Parse and validate RELTO strings
countries = db.parseAndValidateRelto("REL TO US, GB, CA")
print(countries)  # ['USA', 'GBR', 'CAN']

# Check alliance memberships
if db.isFVEY(countries):
    print("This is a Five Eyes release")
```

## Supported Classifications

### Classification Levels
- `UNCLASSIFIED`
- `CONFIDENTIAL`
- `SECRET`
- `TOP SECRET`

### Special Markings
- `CUI` - Controlled Unclassified Information
- `SBU` - Sensitive But Unclassified

### SCI Containers
- `SCI` - Sensitive Compartmented Information
- `SI` - Special Intelligence
- `TK` - TALENT KEYHOLE
- `HCS` - HUMINT Control System
- `GAMMA` - Special SI codeword

### Distribution Controls
- `NOFORN` - Not Releasable to Foreign Nationals
- `REL TO FVEY` - Releasable to Five Eyes
- `REL TO NATO` - Releasable to NATO
- `REL TO <countries>` - Custom country lists

### Special Access Programs (SAP)
- Configurable SAP-A, SAP-B, SAP-C

### Custom SI Groups
- Configurable SI-GROUPA, SI-GROUPB, SI-GROUPC

## Classification Format

Classifications follow this general format:

```
CLASSIFICATION // SAR PROGRAM // SCI CONTAINERS // DISTRIBUTION
```

Examples:
- `UNCLASSIFIED`
- `CUI`
- `SECRET//NOFORN`
- `TOP SECRET//SCI//NOFORN`
- `SECRET//SI/GAMMA//TK//REL TO FVEY`
- `TOP SECRET//SAR-PROGRAM-NAME//SI//TK//HCS//NOFORN`

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=classification_encoder --cov-report=html

# Run specific test file
pytest test/parser_test.py
```

## Development

### Code Formatting

```bash
# Format code with black
black lib/ test/

# Sort imports
isort lib/ test/

# Check with flake8
flake8 lib/ test/
```

### Type Checking

```bash
mypy lib/
```

## Features

- ✅ Encode classification strings to 32-bit integers
- ✅ Decode integers back to classification strings
- ✅ Support for standard classification levels
- ✅ Support for SCI containers (SI, TK, HCS, GAMMA)
- ✅ Support for distribution markings (NOFORN, FVEY, NATO, etc.)
- ✅ Configurable SAP programs
- ✅ Configurable SI codeword groups
- ✅ Configurable custom RELTO lists
- ✅ Country code validation and normalization
- ✅ Classification comparison
- ✅ Type hints throughout
- ✅ Comprehensive test coverage

## Limitations

- Maximum 3 custom SAP programs
- Maximum 3 custom SI groups (plus GAMMA)
- Maximum 3 custom RELTO lists
- Does not support TK or HCS sub-compartments
- 32-bit integer limits total number of distinct markings

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Disclaimer

**UNCLASSIFIED**

Classification markings in this code are for demonstration purposes only and do not indicate actual classification of the software or its contents.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

For issues, questions, or contributions, please open an issue on GitHub.
