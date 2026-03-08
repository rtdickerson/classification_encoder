import os
import sys
from enum import Enum
from json import loads as json_loads

'''
This project provides encoding and decoding functionality for classification labels.

|              ||              |
|      ||      ||      ||      |
+--++--++--++--++--++--++--++--+
    3         2         1    
10987654321098765432109876543210
|||||||||||||||||||||||||||||||+ 0x00000001 - RELTO_E
||||||||||||||||||||||||||||||+- 0x00000002 - RELTO_D
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

class CountryDatabase:
    def __init__(self):
        self.countries = []
        self.rawdata = None
        with open("./country_codes.json", "r") as f:
            self.rawdata = json_loads(f.read())
        for entry in self.rawdata:
            self.countries.append(entry['alpha-3'])
        self.nato = [
            'ALB', 'BEL', 'BGR', 'CAN', 'HRV', 'CZE', 'DNK', 'EST', 'FIN', 
            'FRA', 'DEU', 'GRC', 'HUN', 'ISL', 'ITA', 'LVA', 'LTU', 
            'LUX', 'MNE', 'NLD', 'MKD', 'NOR', 'POL', 'PRT', 'ROU', 'SVK', 
            'SVN', 'ESP', 'SWE', 'CHE', 'TUR', "GBR", "USA"]
        self.fvey = ["USA", "GBR", "CAN", "AUS", "NZL"]    


class NamedBits(Enum):
    RELTO_E = 0x00000001
    RELTO_D = 0x00000002
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

class ClassificationEncoder:

    def __init__(self, customcfg):
        self.bits = BitmaskManager()
        self.sections = {
            'classification' : {
                'unclassified' : {
                    'bits' : NamedBits.UNCLASSIFIED.value,
                    'tag' : 'UNCLASSIFIED'
                },
                'confidential' : {
                    'bits' : NamedBits.CONFIDENTIAL.value,
                    'tag' : "CONFIDENTIAL"
                },
                'secret' : {
                    'bits' : NamedBits.SECRET.value,
                    'tag' : "SECRET"
                },
                'topsecret' : {
                    'bits' : NamedBits.TOP_SECRET.value,
                    'tag' : "TOP SECRET"
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
                'relto-d' : {
                    'bits' : NamedBits.RELTO_D.value,
                    'tag' : "REL TO D",
                    'enabled' : False,
                    'countries' : []
                },
                'relto-e' : {
                    'bits' : NamedBits.RELTO_E.value,
                    'tag' : "REL TO E",
                    'enabled' : False,
                    'countries' : []
                },
                'relto-fvey' : {
                    'bits' : NamedBits.RELTO_FVEY.value,
                    'tag' : "REL TO FVEY",
                    "tokens" : ["REL TO FVEY"],
                    'enabled' : True,
                    'countries' : ["USA", "UK", "CAN", "AUS", "NZL"]
                },
                'relto-nato' : {
                    'bits' : NamedBits.RELTO_NATO.value,
                    'tag' : "REL TO NATO",
                    "tokens" : ["REL TO NATO"],
                    'enabled' : True,
                    'countries' : ["USA", "UK", "CAN", "AUS", "NZL"]
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
                self.sections['containers']['sap-a']['tag'] = customcfg['sap-a']
                self.sections['containers']['sap-a']['enabled'] = True
            if customcfg.get('sap-b') != None:
                self.sections['containers']['sap-b']['tag'] = customcfg['sap-b']
                self.sections['containers']['sap-b']['enabled'] = True
            if customcfg.get('sap-c') != None:
                self.sections['containers']['sap-c']['tag'] = customcfg['sap-c']
                self.sections['containers']['sap-c']['enabled'] = True
            if customcfg.get('si-groupa') != None:
                self.sections['containers']['si-groupa']['tag'] = customcfg['si-groupa']
                self.sections['containers']['si-groupa']['enabled'] = True
            if customcfg.get('si-groupb') != None:
                self.sections['containers']['si-groupb']['tag'] = customcfg['si-groupb']
                self.sections['containers']['si-groupb']['enabled'] = True
            if customcfg.get('si-groupc') != None:
                self.sections['containers']['si-groupc']['tag'] = customcfg['si-groupc']
                self.sections['containers']['si-groupc']['enabled'] = True
            if customcfg.get('relto-a') != None:
                self.sections['relto']['relto-a']['tag'] = customcfg['relto-a']
                self.sections['relto']['relto-a']['enabled'] = True
            if customcfg.get('relto-b') != None:
                self.sections['relto']['relto-b']['tag'] = customcfg['relto-b']
                self.sections['relto']['relto-b']['enabled'] = True
            if customcfg.get('relto-c') != None:
                self.sections['relto']['relto-c']['tag'] = customcfg['relto-c']
                self.sections['relto']['relto-c']['enabled'] = True
            if customcfg.get('relto-d') != None:
                self.sections['relto']['relto-d']['tag'] = customcfg['relto-d']
            if customcfg.get('relto-e') != None:
                self.sections['relto']['relto-e']['tag'] = customcfg['relto-e']
                self.sections['relto']['relto-e']['enabled'] = True

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
        self.parserTokens.append({
            'strings': ["SAP-A"],
            "bit" : NamedBits.SAP_A.value,
            'section': 'containers',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["SAP-B"],
            "bit" : NamedBits.SAP_B.value,
            'section': 'containers',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["SAP-C"],
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
        self.parserTokens.append({
            'strings': ["SI-GROUPA"],
            "bit" : NamedBits.SI_GROUPA.value,
            'section': 'containers',
            "setAlso" : [NamedBits.SCI.value, NamedBits.SI.value]
        })
        self.parserTokens.append({
            'strings': ["SI-GROUPB"],
            "bit" : NamedBits.SI_GROUPB.value,
            'section': 'containers',
            "setAlso" : [NamedBits.SCI.value, NamedBits.SI.value]
        })
        self.parserTokens.append({
            'strings': ["SI-GROUPC"],
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
            'strings': ["REL TO A"],
            "bit" : NamedBits.RELTO_A.value,
            'section': 'distribution',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["REL TO B"],
            "bit" : NamedBits.RELTO_B.value,
            'section': 'distribution',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["REL TO C"],
            "bit" : NamedBits.RELTO_C.value,
            'section': 'distribution',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["REL TO D"],
            "bit" : NamedBits.RELTO_D.value,
            'section': 'distribution',
            "setAlso" : []
        })
        self.parserTokens.append({
            'strings': ["REL TO E"],
            "bit" : NamedBits.RELTO_E.value,
            'section': 'distribution',
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
