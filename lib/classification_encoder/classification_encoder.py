##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##

import os
import sys
from enum import Enum
from json import loads as json_loads
from typing import Optional, Dict, List

from .bitmask import NamedBits
from .bitmask import BitmaskManager
from .countrydatabase import CountryDatabase

'''
The ClassificationEncoder class provides methods for encoding and decoding classification 
labels.

SCI Compartment Format:
- SI, TK, HCS are compartments under SCI
- Codewords within a compartment are separated by "-" (dash)
- Different compartments are separated by "/" (slash)
- Examples:
  - SECRET//SI-GAMMA//TK//NOFORN
  - SECRET//SI-JOE//TK-ABLE//HCS-P//NOFORN
  - TOP SECRET//SI-ALPHA-BRAVO/TK//NOFORN
'''
class ClassificationEncoder:

    def getClassificationSection(self, sectionname: NamedBits) -> Optional[str]:
        """Get the section name for a given NamedBits value."""
        for section in self.sections.keys():
            for chunk in self.sections[section].keys():
                if self.sections[section][chunk]['bits'] == sectionname.value:
                    return chunk
        return None
    
    def _enableClassificationItem(self, sectionname: NamedBits) -> None:
        """Enable a classification item by its NamedBits value."""
        for section in self.sections.keys():
            for chunk in self.sections[section].keys():
                if self.sections[section][chunk]['bits'] == sectionname.value:
                    self.sections[section][chunk]['enabled'] = True
                    return

    def _updateClassificationItem(self, sectionname: NamedBits, tag: str) -> None:
        """Update the tag for a classification item."""
        for section in self.sections.keys():
            for chunk in self.sections[section].keys():
                if self.sections[section][chunk]['bits'] == sectionname.value:
                    self.sections[section][chunk]['tag'] = tag
                    return

    def _parseCountries(self, sectionname: NamedBits, reltoString: str) -> List[str]:
        """Parse and validate country codes from a RELTO string."""
        return self.countries.parseAndValidateRelto(reltoString)
                
    def __init__(self, customcfg: Optional[Dict] = None):
        """
        Initialize the ClassificationEncoder.
        
        Args:
            customcfg: Optional dictionary with custom configuration for SAP programs,
                      SI groups, and RELTO lists.
                      
        Example:
            cfg = {
                'sap-a': 'PROGRAM-ALPHA',
                'si-groupa': 'CODEWORD-ONE',
                'relto-a': 'REL TO USA, GBR, CAN'
            }
            ce = ClassificationEncoder(cfg)
        """
        self.bits = BitmaskManager()
        self.countries = CountryDatabase()
        
        # The sections dictionary defines the structure of the classification system, 
        # including the bits, tags, and enabled status for each classification and container.
        self.sections = {
            'classification': {
                'unclassified': {
                    'bits': NamedBits.UNCLASSIFIED.value,
                    'tag': 'UNCLASSIFIED',
                    'enabled': True
                },
                'confidential': {
                    'bits': NamedBits.CONFIDENTIAL.value,
                    'tag': "CONFIDENTIAL",
                    'enabled': True
                },
                'secret': {
                    'bits': NamedBits.SECRET.value,
                    'tag': "SECRET",
                    'enabled': True
                },
                'topsecret': {
                    'bits': NamedBits.TOPSECRET.value,
                    'tag': "TOP SECRET",
                    'enabled': True
                }
            },
            'containers': {
                "sci": {
                    'bits': NamedBits.SCI.value,
                    'tag': "SCI",
                    "enabled": True
                },
                "sap-a": {
                    'bits': NamedBits.SAP_A.value,
                    'tag': "SAP-A",
                    "enabled": True
                },
                "sap-b": {
                    'bits': NamedBits.SAP_B.value,
                    'tag': "SAP-B",
                    "enabled": False
                },
                "sap-c": {
                    'bits': NamedBits.SAP_C.value,
                    'tag': "SAP-C",
                    "enabled": False
                },
                "gamma": {
                    'bits': NamedBits.GAMMA.value,
                    'tag': "GAMMA",
                    "enabled": True
                },
                "si-groupa": {
                    'bits': NamedBits.SI_GROUPA.value,
                    'tag': "SI-GROUPA",
                    "enabled": False
                },
                "si-groupb": {
                    'bits': NamedBits.SI_GROUPB.value,
                    'tag': "SI-GROUPB",
                    "enabled": False
                },
                "si-groupc": {
                    'bits': NamedBits.SI_GROUPC.value,
                    'tag': "SI-GROUPC",
                    "enabled": False
                },
                "hcs": {
                    'bits': NamedBits.HCS.value,
                    'tag': "HCS",
                    "enabled": True
                },
                "si": {
                    'bits': NamedBits.SI.value,
                    'tag': "SI",
                    "enabled": True
                },
                "tk": {
                    'bits': NamedBits.TK.value,
                    'tag': "TK",
                    "enabled": True
                }   
            },
            "extra": {
                "sbu": {
                    'bits': NamedBits.SBU.value,
                    'tag': "SBU",
                    "enabled": True
                },
                "cui": {
                    'bits': NamedBits.CUI.value,
                    'tag': "CUI",
                    "enabled": True
                },
            },
            'distribution': {
                'relido': {
                    'bits': NamedBits.RELIDO,
                    'tag': 'RELIDO',
                    'tokens': [],
                    'enabled': True,
                    'countries': []
                },
                'relto-a': {
                    'bits': NamedBits.RELTO_A.value,
                    'tag': "REL TO A",
                    "tokens": [],
                    'enabled': False,
                    'countries': []
                },
                'relto-b': {
                    'bits': NamedBits.RELTO_B.value,
                    'tag': "REL TO B",
                    "tokens": [],
                    'enabled': False,
                    'countries': []
                },
                'relto-c': {
                    'bits': NamedBits.RELTO_C.value,
                    'tag': "REL TO C",
                    "tokens": [],
                    'enabled': False,
                    'countries': []
                },
                'relto-9eyes': {
                    'bits': NamedBits.RELTO_NINEEYES.value,
                    'tag': "REL TO 9EYES",
                    'enabled': False,
                    'countries': self.countries.nineEyes
                },
                'relto-14eyes': {
                    'bits': NamedBits.RELTO_FOURTEENEYES.value,
                    'tag': "REL TO 14EYES",
                    'enabled': False,
                    'countries': self.countries.fourteenEyes
                },
                'relto-fvey': {
                    'bits': NamedBits.RELTO_FVEY.value,
                    'tag': "REL TO FVEY",
                    "tokens": ["REL TO FVEY"],
                    'enabled': True,
                    'countries': self.countries.fvey
                },
                'relto-nato': {
                    'bits': NamedBits.RELTO_NATO.value,
                    'tag': "REL TO NATO",
                    "tokens": ["REL TO NATO"],
                    'enabled': True,
                    'countries': self.countries.nato
                },
                'noforn': {
                    'bits': NamedBits.NOFORN.value,
                    'tag': "NOFORN",
                    "tokens": ["NOFORN"],
                    'enabled': True,
                    'countries': []
                }
            }
        }
        
        # Apply custom configuration
        if customcfg:
            if customcfg.get('sap-a') is not None:
                self._updateClassificationItem(NamedBits.SAP_A, customcfg['sap-a'])
                self._enableClassificationItem(NamedBits.SAP_A)
            if customcfg.get('sap-b') is not None:
                self._updateClassificationItem(NamedBits.SAP_B, customcfg['sap-b'])
                self._enableClassificationItem(NamedBits.SAP_B)
            if customcfg.get('sap-c') is not None:
                self._updateClassificationItem(NamedBits.SAP_C, customcfg['sap-c'])
                self._enableClassificationItem(NamedBits.SAP_C)
            if customcfg.get('si-groupa') is not None:
                self._updateClassificationItem(NamedBits.SI_GROUPA, customcfg['si-groupa'])
                self._enableClassificationItem(NamedBits.SI_GROUPA)
            if customcfg.get('si-groupb') is not None:
                self._updateClassificationItem(NamedBits.SI_GROUPB, customcfg['si-groupb'])
                self._enableClassificationItem(NamedBits.SI_GROUPB)
            if customcfg.get('si-groupc') is not None:
                self._updateClassificationItem(NamedBits.SI_GROUPC, customcfg['si-groupc'])
                self._enableClassificationItem(NamedBits.SI_GROUPC)
            if customcfg.get('relto-a') is not None:
                self._updateClassificationItem(NamedBits.RELTO_A, customcfg['relto-a'])
                CL = self._parseCountries(NamedBits.RELTO_A, customcfg['relto-a'])
                if len(CL) > 0:
                    self._enableClassificationItem(NamedBits.RELTO_A)
                    self.sections['distribution']['relto-a']['countries'] = CL
            if customcfg.get('relto-b') is not None:
                self._updateClassificationItem(NamedBits.RELTO_B, customcfg['relto-b'])
                CL = self._parseCountries(NamedBits.RELTO_B, customcfg['relto-b'])
                if len(CL) > 0:
                    self._enableClassificationItem(NamedBits.RELTO_B)
                    self.sections['distribution']['relto-b']['countries'] = CL
            if customcfg.get('relto-c') is not None:
                self._updateClassificationItem(NamedBits.RELTO_C, customcfg['relto-c'])
                CL = self._parseCountries(NamedBits.RELTO_C, customcfg['relto-c'])
                if len(CL) > 0:
                    self._enableClassificationItem(NamedBits.RELTO_C)
                    self.sections['distribution']['relto-c']['countries'] = CL

    def setBitElement(self, bit: NamedBits) -> None:
        """Set a specific bit in the bitmask."""
        self.bits.set_bit(bit.value)

    def encode(self, classification_string: str) -> int:
        """
        Encode a classification string to a 32-bit integer.
        
        This is an alias for parseClassificationString for API consistency.
        
        Args:
            classification_string: Classification marking string
            
        Returns:
            32-bit integer bitmask
        """
        return self.parseClassificationString(classification_string)

    def decode(self, classification_mask: int) -> str:
        """
        Decode a classification bitmask to a string.
        
        This is an alias for constructClassificationString for API consistency.
        
        Args:
            classification_mask: 32-bit integer bitmask
            
        Returns:
            Classification marking string
            
        Raises:
            ValueError: If classification_mask is not an integer
        """
        if not isinstance(classification_mask, int):
            raise ValueError(f"Classification mask must be an integer, got {type(classification_mask)}")
        
        # Create a temporary BitmaskManager with the provided mask
        old_mask = self.bits.bitmask
        self.bits.bitmask = classification_mask
        result = self.constructClassificationString(classification_mask)
        self.bits.bitmask = old_mask
        return result

    def splitOnClearanceSeparator(self, classification_string: str) -> List[str]:
        """Split classification string on '//' separator."""
        return classification_string.split("//")

    def handleRelto(self, reltoString: str) -> int:
        """
        Parse a RELTO string and return the appropriate bit value.
        
        Args:
            reltoString: String like "REL TO FVEY" or "REL TO USA, GBR, CAN"
            
        Returns:
            Bit value for the matching RELTO group, or 0 if no match
        """
        if reltoString == "REL TO NATO":
            return NamedBits.RELTO_NATO.value
        elif reltoString == "REL TO FVEY":
            return NamedBits.RELTO_FVEY.value
            
        CLIST = self.countries.parseAndValidateRelto(reltoString)
        if self.countries.isNATO(CLIST):
            return NamedBits.RELTO_NATO.value
        elif self.countries.isFVEY(CLIST):
            return NamedBits.RELTO_FVEY.value
        elif self.countries.isNineEyes(CLIST):
            return NamedBits.RELTO_NINEEYES.value
        elif self.countries.isFourteenEyes(CLIST):
            return NamedBits.RELTO_FOURTEENEYES.value
        elif self.sections['distribution']['relto-a']['enabled'] and \
            set(CLIST) == set(self.sections['distribution']['relto-a']['countries']):
            return NamedBits.RELTO_A.value
        elif self.sections['distribution']['relto-b']['enabled'] and \
            set(CLIST) == set(self.sections['distribution']['relto-b']['countries']):
            return NamedBits.RELTO_B.value
        elif self.sections['distribution']['relto-c']['enabled'] and \
            set(CLIST) == set(self.sections['distribution']['relto-c']['countries']):
            return NamedBits.RELTO_C.value
        else:
            return 0x00000000
        
    def _createCommaSeparatedRelto(self, countryList: List[str]) -> str:
        """Create a comma-separated RELTO string from a country list."""
        return f"REL TO {', '.join(countryList)}"
    
    def makeReltoString(self, reltoBit: NamedBits) -> str:
        """
        Generate a RELTO string from a NamedBits value.
        
        Args:
            reltoBit: NamedBits enum value for a RELTO group
            
        Returns:
            Formatted RELTO string
        """
        if reltoBit == NamedBits.NOFORN:
            return "NOFORN"
        if reltoBit == NamedBits.RELTO_NATO:
            return "REL TO NATO"
        elif reltoBit == NamedBits.RELTO_FVEY:
            return self._createCommaSeparatedRelto(self.countries.fvey)
        elif reltoBit == NamedBits.RELTO_NINEEYES:
            return self._createCommaSeparatedRelto(self.countries.nineEyes)
        elif reltoBit == NamedBits.RELTO_FOURTEENEYES:
            return self._createCommaSeparatedRelto(self.countries.fourteenEyes)
        elif reltoBit == NamedBits.RELTO_A:
            return self._createCommaSeparatedRelto(self.sections['distribution']['relto-a']['countries'])
        elif reltoBit == NamedBits.RELTO_B:
            return self._createCommaSeparatedRelto(self.sections['distribution']['relto-b']['countries'])
        elif reltoBit == NamedBits.RELTO_C:
            return self._createCommaSeparatedRelto(self.sections['distribution']['relto-c']['countries'])
        else:
            return ""
        
    def _parseSI(self, part: str) -> None:
        """
        Parse SI (Special Intelligence) compartments.
        
        Format: SI-CODEWORD1-CODEWORD2
        Codewords are separated by "-" (dash)
        
        Examples:
            SI (just SI, no codewords)
            SI-GAMMA
            SI-ALPHA-BRAVO
        """
        if part == "SI":
            self.bits.set_bit(NamedBits.SCI.value)
            self.bits.set_bit(NamedBits.SI.value)
            return
        if not part.startswith("SI-"):  # Must start with "SI-" for codewords
            return
        if part == "SI-G": # Shorthand for SI-GAMMA
            self.bits.set_bit(NamedBits.SCI.value)
            self.bits.set_bit(NamedBits.SI.value)
            self.bits.set_bit(NamedBits.GAMMA.value)
            return

            
        # We know it's at least SI, even if we don't recognize the codewords
        self.bits.set_bit(NamedBits.SCI.value)
        self.bits.set_bit(NamedBits.SI.value)
        
        # Parse codewords separated by "-"
        # Example: "SI-GAMMA-ALPHA" -> ["SI", "GAMMA", "ALPHA"]
        parts = part.split("-")
        for sp in parts[1:]:  # Skip the first "SI" part
            wks = sp.strip()
            if self.sections['containers']['si-groupa']['enabled']:
                if self.sections['containers']['si-groupa']['tag'] == wks:
                    self.bits.set_bit(NamedBits.SI_GROUPA.value)
            if self.sections['containers']['si-groupb']['enabled']:
                if self.sections['containers']['si-groupb']['tag'] == wks:
                    self.bits.set_bit(NamedBits.SI_GROUPB.value)
            if self.sections['containers']['si-groupc']['enabled']:
                if self.sections['containers']['si-groupc']['tag'] == wks:
                    self.bits.set_bit(NamedBits.SI_GROUPC.value)
            if wks == "GAMMA":
                self.bits.set_bit(NamedBits.GAMMA.value)

    def _parseTK(self, part: str) -> None:
        """
        Parse TK (TALENT KEYHOLE) compartments.
        
        Format: TK or TK-CODEWORD1-CODEWORD2
        Codewords are separated by "-" (dash)
        
        Examples:
            TK
            TALENT KEYHOLE
            TK-ABLE
        """
        if part == "TK" or part == "TALENT KEYHOLE":
            self.bits.set_bit(NamedBits.SCI.value)
            self.bits.set_bit(NamedBits.TK.value)
            return
        if part.startswith("TK-"):
            # TK with codewords (we don't track individual TK codewords yet)
            self.bits.set_bit(NamedBits.SCI.value)
            self.bits.set_bit(NamedBits.TK.value)

    def _parseSAP(self, part: str) -> None:
        """Parse SAP (Special Access Program) designations."""
        wks = part[4:]  # Get text after "SAR-"
        
        # Check all enabled SAP programs
        if self.sections['containers']['sap-a']['enabled']:
            if self.sections['containers']['sap-a']['tag'] == wks:
                self.bits.set_bit(NamedBits.SAP_A.value)
        if self.sections['containers']['sap-b']['enabled']:
            if self.sections['containers']['sap-b']['tag'] == wks:
                self.bits.set_bit(NamedBits.SAP_B.value)
        if self.sections['containers']['sap-c']['enabled']:
            if self.sections['containers']['sap-c']['tag'] == wks:
                self.bits.set_bit(NamedBits.SAP_C.value)

    def _parseHCS(self, part: str) -> None:
        """
        Parse HCS (HUMINT Control System) compartments.
        
        Format: HCS or HCS-CODEWORD1-CODEWORD2
        Codewords are separated by "-" (dash)
        
        Examples:
            HCS
            HCS-P
        """
        if part == "HCS":
            self.bits.set_bit(NamedBits.SCI.value)
            self.bits.set_bit(NamedBits.HCS.value)
            return
        elif part == "HCS-P":
            self.bits.set_bit(NamedBits.SCI.value)
            self.bits.set_bit(NamedBits.HCS.value)
            self.bits.set_bit(NamedBits.HCS_P.value)
        elif part == "HCS-O":
            self.bits.set_bit(NamedBits.SCI.value)
            self.bits.set_bit(NamedBits.HCS.value)
            self.bits.set_bit(NamedBits.HCS_O.value)
        if part.startswith("HCS-"):
            # HCS with codewords (we don't track individual HCS codewords yet)
            self.bits.set_bit(NamedBits.SCI.value)
            self.bits.set_bit(NamedBits.HCS.value)

    def _parseSCICompartments(self, part: str) -> None:
        """
        Parse SCI compartments which may contain multiple compartments separated by "/".
        
        Format: COMPARTMENT1/COMPARTMENT2/COMPARTMENT3
        Where each compartment can be:
            - SI-CODEWORD1-CODEWORD2
            - TK-CODEWORD1-CODEWORD2
            - HCS-CODEWORD1-CODEWORD2
        
        Examples:
            SI-GAMMA/TK
            SI-JOE/TK-ABLE/HCS-P
            SI/TK/HCS
        """
        # Split on "/" to get individual compartments
        compartments = part.split("/")
        
        for compartment in compartments:
            compartment = compartment.strip()
            if not compartment:
                continue
                
            if compartment.startswith("SI"):
                self._parseSI(compartment)
            elif compartment.startswith("TK") or compartment == "TALENT KEYHOLE":
                self._parseTK(compartment)
            elif compartment.startswith("HCS"):
                self._parseHCS(compartment)

    def parseClassificationString(self, classification_string: str) -> int:
        """
        Parse a classification string and return its bitmask representation.
        
        SCI Compartment Format:
            - Codewords within a compartment: separated by "-" (dash)
            - Different compartments: separated by "/" (slash)
            
        Examples:
            SECRET//SI-GAMMA//TK//NOFORN
            SECRET//SI-JOE/TK-ABLE//NOFORN
            TOP SECRET//SI-ALPHA-BRAVO/TK/HCS-P//NOFORN
        
        Args:
            classification_string: A classification marking like "SECRET//NOFORN"
            
        Returns:
            32-bit integer bitmask representing the classification
            
        Raises:
            ValueError: If classification_string is empty or too long
            
        Example:
            >>> ce = ClassificationEncoder(None)
            >>> mask = ce.parseClassificationString("SECRET//NOFORN")
            >>> hex(mask)
            '0x40000080'
        """
        if not classification_string:
            raise ValueError("Classification string cannot be empty")
        if len(classification_string) > 500:
            raise ValueError("Classification string too long (max 500 characters)")
            
        classification_string = classification_string.upper()
        
        # Reset bitmask for fresh parsing
        self.bits.bitmask = 0x00000000
        
        parts = self.splitOnClearanceSeparator(classification_string)
        for part in parts:
            part = part.strip()
            if part == "UNCLASSIFIED":
                self.bits.set_bit(NamedBits.UNCLASSIFIED.value)
            elif part == "CONFIDENTIAL":
                self.bits.set_bit(NamedBits.CONFIDENTIAL.value)
            elif part == "SECRET":
                self.bits.set_bit(NamedBits.SECRET.value)
            elif part == "TOP SECRET":
                self.bits.set_bit(NamedBits.TOPSECRET.value)
            elif part.startswith("SAR-"):
                self._parseSAP(part)
            elif part == "SCI":
                self.bits.set_bit(NamedBits.SCI.value)
            elif part.startswith("SI") or part.startswith("TK") or part.startswith("HCS") or part == "TALENT KEYHOLE":
                # This might be a single compartment or multiple compartments separated by "/"
                self._parseSCICompartments(part)
            elif part == "NOFORN":
                self.bits.set_bit(NamedBits.NOFORN.value)
            elif part.startswith("REL TO"):
                reltoBit = self.handleRelto(part)
                if reltoBit != 0x00000000:
                    self.bits.set_bit(reltoBit)
            elif part == "CUI":
                self.bits.set_bit(NamedBits.UNCLASSIFIED.value)
                self.bits.set_bit(NamedBits.CUI.value)
            elif part == "SBU":
                self.bits.set_bit(NamedBits.UNCLASSIFIED.value)
                self.bits.set_bit(NamedBits.SBU.value)
        return self.bits.bitmask
    
    def constructClassificationString(self, classification_mask: int) -> str:
        """
        Construct a classification string from a bitmask.
        
        SCI compartments are formatted with:
            - Codewords within a compartment separated by "-" (dash)
            - Different compartments separated by "/" (slash)
        
        Args:
            classification_mask: 32-bit integer bitmask
            
        Returns:
            Formatted classification string
            
        Example:
            >>> ce = ClassificationEncoder(None)
            >>> ce.constructClassificationString(0x40000080)
            'SECRET//NOFORN'
        """
        result = ""
        
        # Handle CUI explicitly
        if self.bits.is_bit_set(NamedBits.UNCLASSIFIED.value) and \
            self.bits.is_bit_set(NamedBits.CUI.value):
                result = "CUI"
                return result
        if self.bits.is_bit_set(NamedBits.UNCLASSIFIED.value) and \
            self.bits.is_bit_set(NamedBits.SBU.value):
                result = "UNCLASSIFIED//SBU"
                return result
                
        # Handle the classifications first
        for bit in [NamedBits.UNCLASSIFIED, NamedBits.CONFIDENTIAL, NamedBits.SECRET,
            NamedBits.TOPSECRET]:
            if self.bits.is_bit_set(bit.value):
                if bit == NamedBits.TOPSECRET:
                    result = "TOP SECRET"
                else:
                    result = bit.name
                break
        
        # Add the SAP programs first if defined
        if self.bits.is_bit_set(NamedBits.SAP_A.value):
            result += f"//SAR-{self.sections['containers']['sap-a']['tag']}"
        if self.bits.is_bit_set(NamedBits.SAP_B.value):
            result += f"//SAR-{self.sections['containers']['sap-b']['tag']}"
        if self.bits.is_bit_set(NamedBits.SAP_C.value):
            result += f"//SAR-{self.sections['containers']['sap-c']['tag']}"

        # Handle SCI compartments
        if self.bits.is_bit_set(NamedBits.SCI.value):
            if not self.bits.anySCISet():
                result += "//SCI"
            else:
                # Build compartments separated by "/"
                compartments = []
                
                # Handle SI compartment with codewords
                if self.bits.is_bit_set(NamedBits.SI.value):
                    si_parts = ["SI"]
                    if self.bits.is_bit_set(NamedBits.SI_GROUPA.value):
                        si_parts.append(self.sections['containers']['si-groupa']['tag'])
                    if self.bits.is_bit_set(NamedBits.SI_GROUPB.value):
                        si_parts.append(self.sections['containers']['si-groupb']['tag'])
                    if self.bits.is_bit_set(NamedBits.SI_GROUPC.value):
                        si_parts.append(self.sections['containers']['si-groupc']['tag'])
                    if self.bits.is_bit_set(NamedBits.GAMMA.value):
                        si_parts.append("GAMMA")
                    compartments.append("-".join(si_parts))
                
                # Handle TK compartment
                if self.bits.is_bit_set(NamedBits.TK.value):
                    compartments.append("TK")
                
                # Handle HCS compartment
                if self.bits.is_bit_set(NamedBits.HCS.value):
                    if self.bits.is_bit_set(NamedBits.HCS_O):
                        compartments.append("HCS-O")
                    elif self.bits.is_bit_set(NamedBits.HCS_P):
                        compartments.append("HCS-P")
                    else:
                        compartments.append("HCS")
                
                if compartments:
                    result += "//" + "/".join(compartments)

        # Handle distribution markings
        if self.bits.is_bit_set(NamedBits.RELIDO.value):
            result += "//RELIDO"
        if self.bits.is_bit_set(NamedBits.NOFORN.value):
            result += f"//{self.makeReltoString(NamedBits.NOFORN)}"
        elif self.bits.is_bit_set(NamedBits.RELTO_FVEY.value):
            result += f"//{self.makeReltoString(NamedBits.RELTO_FVEY)}"
        elif self.bits.is_bit_set(NamedBits.RELTO_NATO.value):
            result += f"//{self.makeReltoString(NamedBits.RELTO_NATO)}"
        elif self.bits.is_bit_set(NamedBits.RELTO_NINEEYES.value):
            result += f"//{self.makeReltoString(NamedBits.RELTO_NINEEYES)}"
        elif self.bits.is_bit_set(NamedBits.RELTO_FOURTEENEYES.value):
            result += f"//{self.makeReltoString(NamedBits.RELTO_FOURTEENEYES)}"
        elif self.bits.is_bit_set(NamedBits.RELTO_A.value):
            result += f"//{self.makeReltoString(NamedBits.RELTO_A)}"
        elif self.bits.is_bit_set(NamedBits.RELTO_B.value):
            result += f"//{self.makeReltoString(NamedBits.RELTO_B)}"
        elif self.bits.is_bit_set(NamedBits.RELTO_C.value):
            result += f"//{self.makeReltoString(NamedBits.RELTO_C)}"
        
        return result


    def checkAccess(self, accessMask: int) -> bool:
        """
        Check if the current bitmask allows access based on an access mask.
        
        Args:
            accessMask: Required access level bitmask
            
        Returns:
            True if access is granted, False otherwise
        """
        if accessMask & self.bits.bitmask == self.bits.bitmask:
            return True
        return False

##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##
