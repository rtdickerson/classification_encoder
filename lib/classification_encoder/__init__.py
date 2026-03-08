import os
import sys
from enum import Enum
from json import loads as json_loads
import re

'''
This project provides encoding and decoding functionality for classification labels.

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
|||||||||||||||||||||||+-------- 0x00000100 - Reserved
||||||||||||||||||||||+--------- 0x00000200 - Reserved
|||||||||||||||||||||+---------- 0x00000400 - Reserved
||||||||||||||||||||+----------- 0x00000800 - Reserved
|||||||||||||||||||+------------ 0x00001000 - SBU
||||||||||||||||||+------------- 0x00002000 - CUI
|||||||||||||||||+-------------- 0x00004000 - FOUO
||||||||||||||||+--------------- 0x00008000 - PROTECTED
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

'''

'''
The CountryDatabase class provides a simple interface to access country codes and 
related information. It loads country data from a JSON file and provides lists of 
countries, NATO members, Five Eyes members, Nine Eyes members, and Fourteen Eyes members.
'''
class CountryDatabase:
    rawdata = {}

    def getAlpha3ForAlpha2(self, alpha2):
        for entry in self.rawdata:
            if entry['alpha2'].upper() == alpha2:
                return entry['alpha3'].upper()
        return None

    def __init__(self):
        self.countries3 = []
        self.countries2 = []
        self.rawdata = {}
        ccodesfile = os.path.join(os.path.dirname(__file__), "world.json")
        with open(ccodesfile, "r", encoding="utf-8", errors="ignore") as f:
            self.rawdata = json_loads(f.read())
        for entry in self.rawdata:
            self.countries3.append(entry['alpha3'].upper())
            self.countries2.append(entry['alpha2'].upper())
        self.nato = [
            'ALB', 'BEL', 'BGR', 'CAN', 'HRV', 'CZE', 'DNK', 'EST', 'FIN', 
            'FRA', 'DEU', 'GRC', 'HUN', 'ISL', 'ITA', 'LVA', 'LTU', 
            'LUX', 'MNE', 'NLD', 'MKD', 'NOR', 'POL', 'PRT', 'ROU', 'SVK', 
            'SVN', 'ESP', 'SWE', 'CHE', 'TUR', "GBR", "USA"]
        self.fvey = ["AUS", "CAN", "NZL", "GBR", "USA"]
        self.nineEyes = ["AUS", "CAN", "NZL", "GBR", "USA", "DNK", "FRA", "NLD", "NOR"]
        self.fourteenEyes = ["AUS", "CAN", "NZL", "GBR", "USA", "DNK", "FRA", "NLD", 
                                "NOR", "BEL", "DEU", "ITA", "ESP", "SWE"]   

    # Take a REL TO ... line and return the country codes as a list.  If the code is 
    # invalid discard it.  If they use alpha-2 then normalize it to alpha-3 which
    # is what they should be using these days.
    def parseAndValidateRelto(self, reltoStr):
        if reltoStr.startswith("REL TO"):
            reltoStr = reltoStr[len("REL TO"):]
        CCODES = []
        for CX in reltoStr.split(","):
            CX = CX.strip()
            if len(CX) == 2:
                # if we find it, normalize it to alpha3 which is what they're supposed
                # to be using.
                if CX in self.countries2:
                    CX2 = self.getAlpha3ForAlpha2(CX)
                    if CX2 != None:
                        CCODES.append(CX2)
            elif len(CX) == 3:
                if CX in self.countries3:
                    CCODES.append(CX)
        return CCODES

    def isNATO(self, countryList):
        return set(self.nato) == set(countryList)

    def isFVEY(self, countryList):
        return set(self.fvey) == set(countryList)

    def isNineEyes(self, countryList):
        return set(self.nineEyes) == set(countryList)

    def isFourteenEyes(self, countryList):
        return set(self.fourteenEyes) == set(countryList)


'''
The NamedBits enum defines named constants for each bit in the classification bitmask.
'''
class NamedBits(Enum):
    RELTO_NINEEYES = 0x00000001
    RELTO_FOURTEENEYES = 0x00000002
    RELTO_C = 0x00000004
    RELTO_B = 0x00000008
    RELTO_A = 0x00000010
    RELTO_FVEY = 0x00000020
    RELTO_NATO = 0x00000040
    NOFORN = 0x00000080
    SBU = 0x00001000
    CUI = 0x00002000
    FOUO = 0x00004000
    PROTECTED = 0x00008000
    HCS = 0x00010000
    SI = 0x00040000
    TK = 0x00080000
    GAMMA = 0x00100000
    SI_GROUPA = 0x00200000
    SI_GROUPB = 0x00400000
    SI_GROUPC = 0x00800000
    SCI = 0x01000000
    SAP_A = 0x02000000
    SAP_B = 0x04000000
    SAP_C = 0x08000000 
    UNCLASSIFIED = 0x10000000 
    CONFIDENTIAL = 0x20000000 
    SECRET = 0x40000000 
    TOP_SECRET = 0x80000000

'''
The BitmaskManager class provides methods for managing a classification bitmask.
'''
class BitmaskManager:
    def __init__(self):
        self.bitmask = 0x00000000

    def set_bit(self, bit):
        self.bitmask |= bit

    def clear_bit(self, bit):
        self.bitmask &= ~bit

    def is_bit_set(self, bit):
        return (self.bitmask & bit) != 0
    
    def setNamedBit(self, namedbit):
        if not isinstance(namedbit, NamedBits):
            raise ValueError(f"Expected a NamedBits enum value, got {type(namedbit)}")
        self.set_bit(namedbit.value)

    def clearNamedBit(self, namedbit):
        if not isinstance(namedbit, NamedBits):
            raise ValueError(f"Expected a NamedBits enum value, got {type(namedbit)}")
        self.clear_bit(namedbit.value)
    
    def getFirstNibble(self):
        return (self.bitmask >> 28) & 0xF
    
    def getSecondNibble(self):
        return (self.bitmask >> 24) & 0xF   
    
    def getThirdNibble(self):
        return (self.bitmask >> 20) & 0xF
    
    def getFouthNibble(self):
        return (self.bitmask >> 16) & 0xF

    def getFifthNibble(self):
        return (self.bitmask >> 12) & 0xF
    
    def getSixthNibble(self):
        return (self.bitmask >> 8) & 0xF    
    
    def getSeventhNibble(self):
        return (self.bitmask >> 4) & 0xF
    
    def getEighthNibble(self):
        return self.bitmask & 0xF
    
    def getFirstByte(self):
        return (self.bitmask >> 24) & 0xFF
    
    def getSecondByte(self):
        return (self.bitmask >> 16) & 0xFF
    
    def getThirdByte(self): 
        return (self.bitmask >> 8) & 0xFF
    
    def getForthByte(self):
        return self.bitmask & 0xFF

'''
The ClassificationEncoder class provides methods for encoding and decoding classification 
labels.
'''
class ClassificationEncoder:

    sections = {}

    def getClassificationSection(self, sectionname:NamedBits):
        for section in self.sections.keys():
            for chunk in self.sections[section].keys():
                if self.sections[section][chunk]['bits'] == sectionname.value:
                    return chunk
        return None
    
    def _enableClassificationItem(self, sectionname:NamedBits):
        for section in self.sections.keys():
            for chunk in self.sections[section].keys():
                if self.sections[section][chunk]['bits'] == sectionname.value:
                    self.sections[section][chunk]['enabled'] = True
                    return

    def _updateClassificationItem(self, sectionname:NamedBits, tag:str):
        for section in self.sections.keys():
            for chunk in self.sections[section].keys():
                if self.sections[section][chunk]['bits'] == sectionname.value:
                    self.sections[section][chunk]['tag'] = tag
                    return

    def _parseCountries(self, sectionname:NamedBits, reltoString):
        return self.countries.parseAndValidateRelto(reltoString)
                
    def __init__(self, customcfg):
        self.bits = BitmaskManager()
        self.countries = CountryDatabase()
        # The sections dictionary defines the structure of the classification system, 
        # including the bits, tags, and enabled status for each classification and container.
        self.sections = {
            'classification' : {
                'unclassified' : {
                    'bits' : NamedBits.UNCLASSIFIED.value,
                    'tag' : 'UNCLASSIFIED',
                    'enabled' : True
                },
                'confidential' : {
                    'bits' : NamedBits.CONFIDENTIAL.value,
                    'tag' : "CONFIDENTIAL",
                    'enabled' : True
                },
                'secret' : {
                    'bits' : NamedBits.SECRET.value,
                    'tag' : "SECRET",
                    'enabled' : True
                },
                'topsecret' : {
                    'bits' : NamedBits.TOP_SECRET.value,
                    'tag' : "TOP SECRET",
                    'enabled' : True
                }
            },
            'containers' : {
                "sci" : {
                    'bits' : NamedBits.SCI.value,
                    'tag' : "SCI",
                    "enabled" : True
                },
                "sap-a" : {
                    'bits' : NamedBits.SAP_A.value,
                    'tag' : "SAP-A",
                    "enabled" : True
                },
                "sap-b" : {
                    'bits' : NamedBits.SAP_B.value,
                    'tag' : "SAP-B",
                    "enabled" : False
                },
                "sap-c" : {
                    'bits' : NamedBits.SAP_C.value,
                    'tag' : "SAP-C",
                    "enabled" : False
                },
                "gamma" : {
                    'bits' : NamedBits.GAMMA.value,
                    'tag' : "GAMMA",
                    "enabled" : True
                },
                "si-groupa" : {
                    'bits' : NamedBits.SI_GROUPA.value,
                    'tag' : "SI-GROUPA",
                    "enabled" : False
                },
                "si-groupb" : {
                    'bits' : NamedBits.SI_GROUPB.value,
                    'tag' : "SI-GROUPB",
                    "enabled" : False
                },
                "si-groupc" : {
                    'bits' : NamedBits.SI_GROUPC.value,
                    'tag' : "SI-GROUPC",
                    "enabled" : False
                },
                "hcs" : {
                    'bits' : NamedBits.HCS.value,
                    'tag' : "HCS",
                    "enabled" : True
                },
                "si" : {
                    'bits' : NamedBits.SI.value,
                    'tag' : "SI",
                    "enabled" : True
                },
                "tk" : {
                    'bits' : NamedBits.TK.value,
                    'tag' : "TK",
                    "enabled" : True
                }   
            },
            "extra" : {
                "sbu" : {
                    'bits' : NamedBits.SBU.value,
                    'tag' : "SBU",
                    "enabled" : True
                },
                "cui" : {
                    'bits' : NamedBits.CUI.value,
                    'tag' : "CUI",
                    "enabled" : True
                },
            },
            'distribution' : {
                'relto-a' : {
                    'bits' : NamedBits.RELTO_A.value,
                    'tag' : "REL TO A",
                    "tokens" : [],
                    'enabled' : False,
                    'countries' : []
                },
                'relto-b' : {
                    'bits' : NamedBits.RELTO_B.value,
                    'tag' : "REL TO B",
                    "tokens" : [],
                    'enabled' : False,
                    'countries' : []
                },
                'relto-c' : {
                    'bits' : NamedBits.RELTO_C.value,
                    'tag' : "REL TO C",
                    "tokens" : [],
                    'enabled' : False,
                    'countries' : []
                },
                'relto-9eyes' : {
                    'bits' : NamedBits.RELTO_NINEEYES.value,
                    'tag' : "REL TO 9EYES",
                    'enabled' : False,
                    'countries' : self.countries.nineEyes
                },
                'relto-14eyes' : {
                    'bits' : NamedBits.RELTO_FOURTEENEYES.value,
                    'tag' : "REL TO 14EYES",
                    'enabled' : False,
                    'countries' : self.countries.fourteenEyes
                },
                'relto-fvey' : {
                    'bits' : NamedBits.RELTO_FVEY.value,
                    'tag' : "REL TO FVEY",
                    "tokens" : ["REL TO FVEY"],
                    'enabled' : True,
                    'countries' : self.countries.fvey
                },
                'relto-nato' : {
                    'bits' : NamedBits.RELTO_NATO.value,
                    'tag' : "REL TO NATO",
                    "tokens" : ["REL TO NATO"],
                    'enabled' : True,
                    'countries' : self.countries.nato
                },
                'noforn' : {
                    'bits' : NamedBits.NOFORN.value,
                    'tag' : "NOFORN",
                    "tokens" : ["NOFORN"],
                    'enabled' : True,
                    'countries' : []
                }
            }
        }
        self.parserTokens = []
        # Tailor the config with the cusomization
        if customcfg:
            if customcfg.get('sap-a') != None:
                self._updateClassificationItem(NamedBits.SAP_A, customcfg['sap-a'])
                self._enableClassificationItem(NamedBits.SAP_A)
            if customcfg.get('sap-b') != None:
                self._updateClassificationItem(NamedBits.SAP_B, customcfg['sap-b'])
                self._enableClassificationItem(NamedBits.SAP_B)
                self.sections['containers']['sap-b']['tag'] = customcfg['sap-b']
                self.sections['containers']['sap-b']['enabled'] = True
            if customcfg.get('sap-c') != None:
                self._updateClassificationItem(NamedBits.SAP_C, customcfg['sap-c'])
                self._enableClassificationItem(NamedBits.SAP_C)
            if customcfg.get('si-groupa') != None:
                self._updateClassificationItem(NamedBits.SI_GROUPA, customcfg['si-groupa'])
                self._enableClassificationItem(NamedBits.SI_GROUPA)
            if customcfg.get('si-groupb') != None:
                self._updateClassificationItem(NamedBits.SI_GROUPB, customcfg['si-groupb'])
                self._enableClassificationItem(NamedBits.SI_GROUPB)
            if customcfg.get('si-groupc') != None:
                self._updateClassificationItem(NamedBits.SI_GROUPC, customcfg['si-groupc'])
                self._enableClassificationItem(NamedBits.SI_GROUPC)
            if customcfg.get('relto-a') != None:
                self._updateClassificationItem(NamedBits.RELTO_A, customcfg['relto-a'])
                CL = self._parseCountries(NamedBits.RELTO_A, customcfg['relto-a'])
                if len(CL) > 0:
                    self._enableClassificationItem(NamedBits.RELTO_A)
                    self.sections['distribution']['relto-a']['countries'] = CL
            if customcfg.get('relto-b') != None:
                self._updateClassificationItem(NamedBits.RELTO_B, customcfg['relto-b'])
                CL = self._parseCountries(NamedBits.RELTO_B, customcfg['relto-b'])
                if len(CL) > 0:
                    self._enableClassificationItem(NamedBits.RELTO_B)
                    self.sections['distribution']['relto-b']['countries'] = CL
            if customcfg.get('relto-c') != None:
                self._updateClassificationItem(NamedBits.RELTO_C, customcfg['relto-c'])
                CL = self._parseCountries(NamedBits.RELTO_C, customcfg['relto-c'])
                if len(CL) > 0:
                    self._enableClassificationItem(NamedBits.RELTO_C)
                    self.sections['distribution']['relto-c']['countries'] = CL

    def setBitElement(self, bit : NamedBits):
        self.bits.set_bit(bit.value)

    ##
    # This function builds the list of parser tokens based on the sections and their 
    # enabled status.
    def buildParserTokens(self):
        self.parserTokens = []
        self.parserTokens.append({
            'strings': ["UNCLASSIFIED"],
            "bit" : NamedBits.UNCLASSIFIED.value,
            'section': 'classification',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["CONFIDENTIAL"],
            "bit" : NamedBits.CONFIDENTIAL.value,
            'section': 'classification',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["SECRET"],
            "bit" : NamedBits.SECRET.value,
            'section': 'classification',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["TOP SECRET"],
            "bit" : NamedBits.TOP_SECRET.value,
            'section': 'classification',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["SCI"],
            "bit" : NamedBits.SCI.value,
            'section': 'containers',
            "setAlso" : []
        })
        if self.sections['containers']['sap-a']['enabled']:
            self.parserTokens.append({
                'strings': ["SAP-%s" % self.sections['containers']['sap-a']['tag']],
                "bit" : NamedBits.SAP_A.value,
                'section': 'containers',
                "setAlso" : []
            })
        if self.sections['containers']['sap-b']['enabled']:
            self.parserTokens.append({
                    'strings': ["SAP-%s" % self.sections['containers']['sap-b']['tag']],
                    "bit" : NamedBits.SAP_B.value,
                    'section': 'containers',
                    "setAlso" : []
                })
        if self.sections['containers']['sap-c']['enabled']:
            self.parserTokens.append({
                    'strings': ["SAP-%s" % self.sections['containers']['sap-c']['tag']],
                    "bit" : NamedBits.SAP_C.value,
                    'section': 'containers',
                    "setAlso" : []
                })
        self.parserTokens.append({
            'strings': ["GAMMA"],
            "bit" : NamedBits.GAMMA.value,
            'section': 'containers',
            "setAlso" : [NamedBits.SCI.value, NamedBits.SI.value]
        })
        if self.sections['containers']['si-groupa']['enabled']:
            STR = self.sections['containers']['si-groupa']['tag']
            # Can be SI-{str} or //SI/{str} to allow either, but if the
            # configuration uses SI-... explicitly then only do one.
            if STR.startswith("SI-"):
                self.parserTokens.append({
                    'strings': [STR],
                    "bit" : NamedBits.SI_GROUPA.value,
                    'section': 'containers',
                    "setAlso" : [NamedBits.SCI.value, NamedBits.SI.value]
                })
            else:
                self.parserTokens.append({
                    'strings': ["SI-%s" % STR, STR],
                    "bit" : NamedBits.SI_GROUPA.value,
                    'section': 'containers',
                    "setAlso" : [NamedBits.SCI.value, NamedBits.SI.value]
                })
        if self.sections['containers']['si-groupb']['enabled']:
            STR = self.sections['containers']['si-groupb']['tag']
            # Can be SI-{str} or //SI/{str} to allow either, but if the
            # configuration uses SI-... explicitly then only do one.
            if STR.startswith("SI-"):
                self.parserTokens.append({
                    'strings': [STR],
                    "bit" : NamedBits.SI_GROUPB.value,
                    'section': 'containers',
                    "setAlso" : [NamedBits.SCI.value, NamedBits.SI.value]
                })
            else:
                self.parserTokens.append({
                    'strings': ["SI-%s" % STR, STR],
                    "bit" : NamedBits.SI_GROUPB.value,
                    'section': 'containers',
                    "setAlso" : [NamedBits.SCI.value, NamedBits.SI.value]
                })
        if self.sections['containers']['si-groupc']['enabled']:
            STR = self.sections['containers']['si-groupc']['tag']
            # Can be SI-{str} or //SI/{str} to allow either, but if the
            # configuration uses SI-... explicitly then only do one.
            if STR.startswith("SI-"):
                self.parserTokens.append({
                    'strings': [STR],
                    "bit" : NamedBits.SI_GROUPC.value,
                    'section': 'containers',
                    "setAlso" : [NamedBits.SCI.value, NamedBits.SI.value]
                })
            else:            
                self.parserTokens.append({
                    'strings': ["SI-%s" % STR, STR],
                    "bit" : NamedBits.SI_GROUPC.value,
                    'section': 'containers',
                    "setAlso" : [NamedBits.SCI.value, NamedBits.SI.value]
                })
        self.parserTokens.append({
            'strings': ["HCS"],
            "bit" : NamedBits.HCS.value,
            'section': 'containers',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["SI"],
            "bit" : NamedBits.SI.value,
            'section': 'containers',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["TK"],
            "bit" : NamedBits.TK.value,
            'section': 'containers',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["SBU"],
            "bit" : NamedBits.SBU.value,
            'section': 'extra',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["CUI"],
            "bit" : NamedBits.CUI.value,
            'section': 'extra',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["REL TO FVEY"],
            "bit" : NamedBits.RELTO_FVEY.value,
            'section': 'distribution',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["REL TO NATO"],
            "bit" : NamedBits.RELTO_NATO.value,
            'section': 'distribution',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["NOFORN"],
            "bit" : NamedBits.NOFORN.value,
            'section': 'distribution',
            "setAlso" : []
        })


    def encode(self, classification_string):
        return 0x00000000

    def decode(self, classification_mask):
        if not classification_mask is int:
            raise ValueError(f"Classification mask must be an integer.")
        return ""

    def splitOnClearanceSeparator(self, classification_string):
        return re.split(r'/+', classification_string)

    def handleRelto(self, reltoString):
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
        
    def _createCommaSeparatedRelto(self, countryList):
        return "REL TO %s" % ", ".join(countryList)
    
    def makeReltoString(self, reltoBit : NamedBits):
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