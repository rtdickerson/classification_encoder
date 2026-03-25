# Visual Guide: SCI Compartment Separators

## The Three Separators

```
SECRET  //  SI-GAMMA  /  TK  //  NOFORN
       ^^^^         ^^^^  ^^^^
       ||||         ||||  ||||
       |||+---------|-----|------- Double slash: Separates MAIN SECTIONS
       ||+----------|-------------  (Classification, SCI, Distribution)
       |+-----------|
       +------------|
                    |
                    +-------------- Single slash: Separates COMPARTMENTS
                                    (SI, TK, HCS within SCI)
                    
SECRET  //  SI - GAMMA - DELTA  //  NOFORN
            ^^^^^^^^^^^^^^^^^^
            ||||||||||||||||||
            |||||||||||||||||+---- Dash: Separates CODEWORDS
            ||||||||||||||||+----- within a compartment
            |||||||||||||||+------ (GAMMA, DELTA are codewords in SI)
            ||||||||||||||+-------
            |||||||||||||+--------
            ||||||||||||+---------
            |||||||||||+----------
            ||||||||||+-----------
            |||||||||+------------
            ||||||||+-------------
            |||||||+--------------
            ||||||+---------------
            |||||+----------------
            ||||+-----------------
            |||+------------------
            ||+-------------------
            |+--------------------
            +---------------------
```

## Hierarchical View

```
Classification String
│
├── MAIN SECTION 1: Classification Level
│   └── "SECRET"
│
├── MAIN SECTION 2: SAP Programs (if any)
│   └── "SAR-PROGRAM-NAME"
│
├── MAIN SECTION 3: SCI Compartments
│   │
│   ├── COMPARTMENT 1: SI
│   │   ├── Base: SI
│   │   ├── Codeword 1: GAMMA
│   │   └── Codeword 2: DELTA
│   │   → Output: "SI-GAMMA-DELTA"
│   │
│   ├── COMPARTMENT 2: TK
│   │   ├── Base: TK
│   │   └── Codeword 1: ABLE
│   │   → Output: "TK-ABLE"
│   │
│   └── COMPARTMENT 3: HCS
│       ├── Base: HCS
│       └── Codeword 1: P
│       → Output: "HCS-P"
│   
│   → Combined: "SI-GAMMA-DELTA/TK-ABLE/HCS-P"
│
└── MAIN SECTION 4: Distribution
    └── "NOFORN"

→ Final: "SECRET//SI-GAMMA-DELTA/TK-ABLE/HCS-P//NOFORN"
```

## Side-by-Side Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                         CORRECT FORMAT                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SECRET // SI-GAMMA / TK // NOFORN                             │
│         ^^        ^^   ^^                                       │
│         ||        ||   ||                                       │
│         ||        ||   |+--- Double slash: Main sections        │
│         ||        ||   +---- Single slash: Compartments         │
│         ||        |+-------- Dash: Codewords                    │
│         |+--------+--------- Double slash: Main sections        │
│         +------------------- Double slash: Main sections        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         WRONG FORMAT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SECRET // SI / GAMMA // TK // NOFORN                          │
│         ^^   ^^      ^^                                         │
│         ||   ||      ||                                         │
│         ||   ||      |+--- Double slash: Main sections          │
│         ||   ||      +---- Double slash: Main sections          │
│         ||   |+----------- Slash: WRONG! Should be dash         │
│         |+---+------------ Double slash: Main sections          │
│         +------------------ Double slash: Main sections         │
│                                                                 │
│  ❌ This treats GAMMA as a separate compartment!               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Real-World Examples

### Example 1: Simple
```
┌──────────────────────────────────────────────┐
│ Input:  SECRET//SI-GAMMA//NOFORN            │
├──────────────────────────────────────────────┤
│                                              │
│ Parse:                                       │
│   Section 1: "SECRET"                        │
│   Section 2: "SI-GAMMA"                      │
│     ├─ Split on '/': ["SI-GAMMA"]           │
│     └─ Split on '-': ["SI", "GAMMA"]        │
│         ├─ Set SI bit                        │
│         └─ Set GAMMA bit                     │
│   Section 3: "NOFORN"                        │
│                                              │
│ Output: SECRET//SI-GAMMA//NOFORN            │
│                                              │
└──────────────────────────────────────────────┘
```

### Example 2: Multiple Compartments
```
┌──────────────────────────────────────────────┐
│ Input:  SECRET//SI-GAMMA/TK//NOFORN         │
├──────────────────────────────────────────────┤
│                                              │
│ Parse:                                       │
│   Section 1: "SECRET"                        │
│   Section 2: "SI-GAMMA/TK"                   │
│     ├─ Split on '/': ["SI-GAMMA", "TK"]     │
│     ├─ Process "SI-GAMMA":                   │
│     │   └─ Split on '-': ["SI", "GAMMA"]    │
│     │       ├─ Set SI bit                    │
│     │       └─ Set GAMMA bit                 │
│     └─ Process "TK":                         │
│         └─ Set TK bit                        │
│   Section 3: "NOFORN"                        │
│                                              │
│ Output: SECRET//SI-GAMMA/TK//NOFORN         │
│                                              │
└──────────────────────────────────────────────┘
```

### Example 3: Multiple Codewords
```
┌──────────────────────────────────────────────┐
│ Input:  TOP SECRET//SI-ALPHA-BRAVO//NOFORN  │
├──────────────────────────────────────────────┤
│                                              │
│ Parse:                                       │
│   Section 1: "TOP SECRET"                    │
│   Section 2: "SI-ALPHA-BRAVO"                │
│     ├─ Split on '/': ["SI-ALPHA-BRAVO"]     │
│     └─ Split on '-': ["SI","ALPHA","BRAVO"] │
│         ├─ Set SI bit                        │
│         ├─ Set ALPHA bit                     │
│         └─ Set BRAVO bit                     │
│   Section 3: "NOFORN"                        │
│                                              │
│ Output: TOP SECRET//SI-ALPHA-BRAVO//NOFORN  │
│                                              │
└──────────────────────────────────────────────┘
```

### Example 4: Complex
```
┌──────────────────────────────────────────────────────────────┐
│ Input:  TOP SECRET//SI-GAMMA-DELTA/TK-ABLE/HCS-P//NOFORN    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Parse:                                                       │
│   Section 1: "TOP SECRET"                                    │
│   Section 2: "SI-GAMMA-DELTA/TK-ABLE/HCS-P"                 │
│     ├─ Split on '/': ["SI-GAMMA-DELTA", "TK-ABLE", "HCS-P"]│
│     ├─ Process "SI-GAMMA-DELTA":                            │
│     │   └─ Split on '-': ["SI", "GAMMA", "DELTA"]          │
│     │       ├─ Set SI bit                                   │
│     │       ├─ Set GAMMA bit                                │
│     │       └─ Set DELTA bit                                │
│     ├─ Process "TK-ABLE":                                   │
│     │   └─ Split on '-': ["TK", "ABLE"]                    │
│     │       └─ Set TK bit (ABLE not tracked)               │
│     └─ Process "HCS-P":                                     │
│         └─ Split on '-': ["HCS", "P"]                      │
│             └─ Set HCS bit (P not tracked)                 │
│   Section 3: "NOFORN"                                        │
│                                                              │
│ Output: TOP SECRET//SI-GAMMA-DELTA/TK/HCS//NOFORN          │
│         (Note: TK-ABLE and HCS-P simplified to TK and HCS)  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Memory Aid

Think of it like a file path:

```
/home/user/documents/file.txt
 ^^^^      ^^^^      ^^^^^^^^^
 |         |         |
 |         |         +--------- Filename (like codewords)
 |         +------------------- Directory (like compartment)
 +----------------------------- Root (like main section)

Separators:
  /  = Directory separator (like compartment separator)
  -  = Word separator in filename (like codeword separator)
  // = Protocol separator (like main section separator)
```

Or like a URL:

```
https://example.com/path/to/resource
^^^^^^                ^^^^    ^^^^^^^^
|                     |       |
|                     |       +-------- Resource (like codewords)
|                     +---------------- Path segments (like compartments)
+-------------------------------------- Protocol (like main sections)

Separators:
  /  = Path separator (like compartment separator)
  -  = Word separator in resource (like codeword separator)
  // = Protocol separator (like main section separator)
```

## Quick Reference Card

```
┌────────────────────────────────────────────────────┐
│  CLASSIFICATION STRING SEPARATOR QUICK REFERENCE   │
├────────────────────────────────────────────────────┤
│                                                    │
│  //  = Separates MAIN SECTIONS                    │
│       (Classification, SAP, SCI, Distribution)     │
│                                                    │
│  /   = Separates COMPARTMENTS within SCI          │
│       (SI, TK, HCS)                                │
│                                                    │
│  -   = Separates CODEWORDS within compartment     │
│       (GAMMA, DELTA, etc.)                         │
│                                                    │
├────────────────────────────────────────────────────┤
│  EXAMPLES:                                         │
│                                                    │
│  ✅ SECRET//SI-GAMMA//NOFORN                      │
│  ✅ SECRET//SI-GAMMA/TK//NOFORN                   │
│  ✅ SECRET//SI-ALPHA-BRAVO/TK/HCS//NOFORN         │
│                                                    │
│  ❌ SECRET//SI/GAMMA//NOFORN                      │
│  ❌ SECRET//SI/GAMMA/TK//NOFORN                   │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

**UNCLASSIFIED** - Classification markings are for code purposes only.
