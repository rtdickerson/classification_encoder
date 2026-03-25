# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-03-24

### Fixed
- **CRITICAL**: Fixed SCI compartment separator format
  - Codewords within a compartment now use `-` (dash) instead of `/` (slash)
  - Correct format: `SECRET//SI-GAMMA//TK//NOFORN`
  - Old format: `SECRET//SI/GAMMA//TK//NOFORN` (wrong)
  - Parser now accepts both formats for backward compatibility
  - Output always uses correct format with `-` for codewords
- Updated `_parseSI()` to split codewords on `-` instead of `/`
- Updated `_parseTK()` to handle `TK-CODEWORD` format
- Updated `_parseHCS()` to handle `HCS-CODEWORD` format
- Added new `_parseSCICompartments()` method to handle complex SCI sections
- Updated `constructClassificationString()` to output correct format

### Added
- `SEPARATOR_FORMAT.md` - Comprehensive format documentation
- `SEPARATOR_FIX.md` - Detailed fix documentation
- `SEPARATOR_VISUAL.md` - Visual guide with diagrams
- Enhanced docstrings explaining separator usage

### Changed
- SCI compartment parsing now properly handles:
  - Single compartment with codewords: `SI-GAMMA-DELTA`
  - Multiple compartments: `SI-GAMMA/TK/HCS`
  - Complex combinations: `SI-ALPHA-BRAVO/TK-ABLE/HCS-P`

## [0.1.0] - 2025-03-24

### Fixed
- **CRITICAL**: Fixed import statements in `classification_encoder.py` to use relative imports (`.bitmask`, `.countrydatabase`)
- **CRITICAL**: Fixed import statements in `mask_compare.py` to use relative imports
- **CRITICAL**: Fixed logic bug in `_parseSAP()` method - changed `elif` to `if` so multiple SAP programs can be recognized
- **CRITICAL**: Fixed logic bug in `_parseSI()` method - changed `elif` to `if` so multiple SI groups can be recognized
- **CRITICAL**: Fixed typo in `_parseSAP()` - third condition was checking `sap-b` instead of `sap-c`
- Fixed typo: `getFouthNibble()` → `getFourthNibble()`
- Fixed typo: `getForthByte()` → `getFourthByte()`
- Fixed incorrect type check: `not x is int` → `not isinstance(x, int)`
- Removed class variable `sections = {}` from ClassificationEncoder (was shared across instances)
- Fixed `anySCISet()` to include HCS bit

### Added
- Type hints throughout all modules
- Comprehensive docstrings for all classes and public methods
- `encode()` and `decode()` methods as aliases for better API consistency
- Input validation in `parseClassificationString()` (empty string, max length checks)
- `setup.py` for package installation
- `pyproject.toml` for modern Python packaging
- `requirements-dev.txt` for development dependencies
- Enhanced README.md with usage examples and API documentation
- `.gitignore` file
- `CHANGELOG.md` (this file)
- `FIXES_SUMMARY.md` - Detailed list of all fixes
- `QUICKSTART.md` - 5-minute quick start guide
- `examples/basic_usage.py` - Working code examples

### Changed
- Standardized string formatting to use f-strings throughout
- Improved error messages with more context
- Enhanced code comments and documentation
- Made `decode()` functional (was returning empty string)
- Made `encode()` functional (was returning 0x00000000)

### Improved
- Better separation of concerns in code organization
- More consistent naming conventions
- Clearer variable names in comparison logic
- Better handling of edge cases

## [Unreleased]

### TODO
- Implement `compareThree()` method for three-way comparison
- Add caching for CountryDatabase to improve performance
- Create reverse lookup dictionary for bit values to improve search performance
- Add more comprehensive error handling
- Add logging support
- Create Sphinx documentation
- Add CI/CD configuration (GitHub Actions)
- Add code coverage reporting
- Add more edge case tests
- Consider using Enum for comparison constants
- Refactor long `__init__` method in ClassificationEncoder
- Add JSON schema validation for world.json
- Add support for additional classification systems (UK, NATO, etc.)
- Performance optimization for repeated parsing operations
- Track individual TK and HCS codewords (currently only base compartment is tracked)

## Known Issues

- `compareThree()` is not implemented (raises NotImplementedError)
- No validation of world.json structure on load
- Country database is loaded on every CountryDatabase instantiation (no caching)
- Limited to 32-bit integer (31 usable bits due to sign bit)
- Individual TK and HCS codewords are not tracked (only SI codewords are tracked)
- Custom RELTO groups cannot be ordered by restrictiveness

## Migration Guide

### From 0.1.0 to 0.1.1

**SCI Compartment Format Change:**

If you have code or data using the old format:

```python
# Old format (still accepted for input)
"SECRET//SI/GAMMA//TK//NOFORN"

# New format (always used for output)
"SECRET//SI-GAMMA//TK//NOFORN"
```

**What you need to do:**
- ✅ Input parsing: No changes needed - both formats accepted
- ✅ Output: Code now outputs correct format automatically
- ⚠️ String comparisons: Update any hardcoded strings to use `-` instead of `/`
- ⚠️ Database: Old stored strings will parse correctly, but consider migrating to new format

**Example migration:**
```python
from classification_encoder import ClassificationEncoder

ce = ClassificationEncoder(None)

# Old format strings will parse correctly
old_format = "SECRET//SI/GAMMA//TK//NOFORN"
mask = ce.encode(old_format)

# But output will be in new format
new_format = ce.decode(mask)
print(new_format)  # "SECRET//SI-GAMMA//TK//NOFORN"

# Update your database
# UPDATE documents SET classification = ? WHERE classification = ?
# (new_format, old_format)
```

### From Previous Version to 0.1.0

If you were using the package before these fixes:

1. **Import Changes**: No changes needed if importing from package level
   ```python
   # This still works
   from classification_encoder import ClassificationEncoder
   ```

2. **Method Name Changes**: Update any direct calls to typo'd methods
   ```python
   # Old (will cause AttributeError)
   nibble = bm.getFouthNibble()
   
   # New
   nibble = bm.getFourthNibble()
   ```

3. **Behavior Changes**: 
   - `encode()` now actually encodes (previously returned 0)
   - `decode()` now actually decodes (previously returned empty string)
   - Multiple SAP programs and SI groups are now properly recognized

4. **Type Checking**: If you were passing non-integers to `decode()`, you'll now get proper ValueError exceptions

## Format Reference

### Correct SCI Compartment Format

```
Separators:
  //  = Main sections (Classification, SAP, SCI, Distribution)
  /   = Compartments within SCI (SI, TK, HCS)
  -   = Codewords within a compartment

Examples:
  ✅ SECRET//SI-GAMMA//NOFORN
  ✅ SECRET//SI-GAMMA/TK//NOFORN
  ✅ TOP SECRET//SI-ALPHA-BRAVO/TK/HCS-P//NOFORN
  
  ❌ SECRET//SI/GAMMA//NOFORN (wrong)
  ❌ SECRET//SI/GAMMA/TK//NOFORN (wrong)
```

See `SEPARATOR_FORMAT.md` for complete documentation.

## Security Notes

- This library handles classification markings but does not enforce access control
- Classification strings are parsed and validated, but the library trusts input data
- No cryptographic operations are performed
- Country codes are validated against a static JSON file

---

**UNCLASSIFIED** - Classification markings are for code purposes only and do not indicate classification.
