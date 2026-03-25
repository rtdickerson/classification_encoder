# Quick Start Guide

Get up and running with classification_encoder in 5 minutes!

## Installation

```bash
# Navigate to the project directory
cd classification_encoder

# Install the package
pip install -e .
```

## Basic Usage

### 1. Simple Encoding/Decoding

```python
from classification_encoder import ClassificationEncoder

# Create encoder
ce = ClassificationEncoder(None)

# Encode a classification string
mask = ce.encode("SECRET//NOFORN")
print(f"Encoded: 0x{mask:08X}")  # Output: 0x40000080

# Decode back to string
classification = ce.decode(mask)
print(f"Decoded: {classification}")  # Output: SECRET//NOFORN
```

### 2. Working with Different Classifications

```python
from classification_encoder import ClassificationEncoder

ce = ClassificationEncoder(None)

# Try different classification levels
classifications = [
    "UNCLASSIFIED",
    "CUI",
    "SECRET//NOFORN",
    "TOP SECRET//SCI//TK//NOFORN",
    "SECRET//REL TO FVEY"
]

for cls in classifications:
    mask = ce.encode(cls)
    print(f"{cls:40} -> 0x{mask:08X}")
```

**Output:**
```
UNCLASSIFIED                             -> 0x10000000
CUI                                      -> 0x10002000
SECRET//NOFORN                           -> 0x40000080
TOP SECRET//SCI//TK//NOFORN              -> 0x810C0080
SECRET//REL TO FVEY                      -> 0x40000020
```

### 3. Custom Configuration

```python
from classification_encoder import ClassificationEncoder

# Define custom SAP programs and SI groups
config = {
    'sap-a': 'PROGRAM-ALPHA',
    'si-groupa': 'CODEWORD-ONE',
    'relto-a': 'REL TO USA, GBR, CAN'
}

ce = ClassificationEncoder(config)

# Use custom markings
mask = ce.encode("SECRET//SAR-PROGRAM-ALPHA//SI/CODEWORD-ONE//NOFORN")
decoded = ce.decode(mask)
print(decoded)
```

### 4. Comparing Classifications

```python
from classification_encoder import ClassificationEncoder

ce = ClassificationEncoder(None)

mask1 = ce.encode("SECRET//NOFORN")
mask2 = ce.encode("TOP SECRET//NOFORN")

result = ce.compareTwo(mask1, mask2)

if result == ce.COMPARE_FIRST:
    print("First is more restrictive")
elif result == ce.COMPARE_SECOND:
    print("Second is more restrictive")  # This will print
else:
    print("Equal")
```

### 5. Working with Country Codes

```python
from classification_encoder import CountryDatabase

db = CountryDatabase()

# Parse RELTO strings
countries = db.parseAndValidateRelto("REL TO US, GB, CA, AU, NZ")
print(countries)  # ['USA', 'GBR', 'CAN', 'AUS', 'NZL']

# Check if it's Five Eyes
if db.isFVEY(countries):
    print("This is Five Eyes!")  # This will print
```

## Common Patterns

### Pattern 1: Encode, Store, Retrieve, Decode

```python
from classification_encoder import ClassificationEncoder

ce = ClassificationEncoder(None)

# Encode for storage
classification_text = "SECRET//SCI//SI//NOFORN"
classification_int = ce.encode(classification_text)

# Store in database (as integer)
# db.execute("INSERT INTO documents (classification) VALUES (?)", (classification_int,))

# Later, retrieve and decode
# classification_int = db.execute("SELECT classification FROM documents WHERE id=?", (doc_id,)).fetchone()[0]
classification_text = ce.decode(classification_int)
print(classification_text)
```

### Pattern 2: Access Control Check

```python
from classification_encoder import ClassificationEncoder

ce = ClassificationEncoder(None)

# User's clearance
user_clearance = ce.encode("TOP SECRET//SCI//SI//TK//REL TO FVEY")

# Document classification
document_class = ce.encode("SECRET//SCI//SI//NOFORN")

# Simple check (you'd need more sophisticated logic in production)
ce.bits.bitmask = document_class
has_access = ce.checkAccess(user_clearance)

if has_access:
    print("Access granted")
else:
    print("Access denied")
```

### Pattern 3: Batch Processing

```python
from classification_encoder import ClassificationEncoder

ce = ClassificationEncoder(None)

# Process multiple classifications
documents = [
    ("doc1.txt", "SECRET//NOFORN"),
    ("doc2.txt", "TOP SECRET//SCI//NOFORN"),
    ("doc3.txt", "UNCLASSIFIED"),
]

# Encode all
encoded_docs = [
    (filename, ce.encode(classification))
    for filename, classification in documents
]

# Store or process...
for filename, mask in encoded_docs:
    print(f"{filename}: 0x{mask:08X}")
```

## Running the Examples

```bash
# Run the comprehensive examples
python examples/basic_usage.py
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test/parser_test.py

# Run with coverage
pytest --cov=classification_encoder
```

## Common Issues

### Issue: ModuleNotFoundError

**Problem:**
```
ModuleNotFoundError: No module named 'classification_encoder'
```

**Solution:**
```bash
# Make sure you've installed the package
pip install -e .

# Or add the lib directory to your Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/classification_encoder/lib"
```

### Issue: Import Error in Tests

**Problem:**
```
ImportError: cannot import name 'ClassificationEncoder'
```

**Solution:**
Make sure you're importing correctly:
```python
# Correct
from classification_encoder import ClassificationEncoder

# Not this
from lib.classification_encoder import ClassificationEncoder
```

### Issue: Tests Failing

**Problem:**
Tests fail with import errors or assertion errors.

**Solution:**
```bash
# Make sure you have the fixed version
git pull  # or download the latest version

# Reinstall
pip install -e .

# Run tests
pytest -v
```

## Next Steps

1. **Read the full documentation:** Check `README.md` for detailed API docs
2. **Review examples:** Look at `examples/basic_usage.py` for more patterns
3. **Check the changelog:** See `CHANGELOG.md` for recent changes
4. **Explore the code:** Browse the source in `lib/classification_encoder/`

## Support

- **Documentation:** See `README.md`
- **Examples:** See `examples/basic_usage.py`
- **Changes:** See `CHANGELOG.md`
- **Fixes:** See `FIXES_SUMMARY.md`

## Quick Reference

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

### Format
```
CLASSIFICATION // SAR PROGRAM // SCI CONTAINERS // DISTRIBUTION
```

Examples:
- `UNCLASSIFIED`
- `SECRET//NOFORN`
- `TOP SECRET//SCI//SI//TK//NOFORN`
- `SECRET//SAR-PROGRAM//SI/CODEWORD//REL TO FVEY`

---

**UNCLASSIFIED** - Classification markings are for code purposes only.

Happy coding! 🚀
