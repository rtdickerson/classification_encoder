import os
import sys

class ClassificationEncoder:

    '''
    This class provides encoding and decoding functionality for classification labels.
    
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
    def __init__(self, customcfg):
        self.sections = {
            'classification' : {
                'unclassified' : {
                    'bits' : 0x10000000,
                    'tag' : 'UNCLASSIFIED'
                },
                'confidential' : {
                    'bits' : 0x20000000,
                    'tag' : "CONFIDENTIAL"
                },
                'secret' : {
                    'bits' : 0x40000000,
                    'tag' : "SECRET"
                },
                'topsecret' : {
                    'bits' : 0x80000000,
                    'tag' : "TOP SECRET"
                }
            },
            'containers' : {
                "sci" : {
                    'bits' : 0x01000000,
                    'tag' : "SCI"
                },
                "sap-a" : {
                    'bits' : 0x02000000,
                    'tag' : "SAP-A"
                },
                "sap-b" : {
                    'bits' : 0x04000000,
                    'tag' : "SAP-B"
                },
                "sap-c" : {
                    'bits' : 0x08000000,
                    'tag' : "SAP-C"
                },
                "gamma" : {
                    'bits' : 0x00100000,    
                    'tag' : "GAMMA"
                },
                "si-groupa" : {
                    'bits' : 0x00200000,
                    'tag' : "SI-GROUPA"
                },
                "si-groupb" : {
                    'bits' : 0x00400000,
                    'tag' : "SI-GROUPB"
                },
                "si-groupc" : {
                    'bits' : 0x00800000,
                    'tag' : "SI-GROUPC"
                },
                "hcs" : {
                    'bits' : 0x00010000,
                    'tag' : "HCS"
                },
                "si" : {
                    'bits' : 0x00040000,
                    'tag' : "SI"
                },
                "tk" : {
                    'bits' : 0x00080000,
                    'tag' : "TK"
                }   
            },
            "extra" : {
                "sbu" : {
                    'bits' : 0x00001000,
                    'tag' : "SBU"
                },
                "cui" : {
                    'bits' : 0x00002000,
                    'tag' : "CUI"
                },
            }
        }
        # Tailor the config with the cusomization
        if customcfg:
            if customcfg.get('sap-a') != None:
                self.sections['containers']['sap-a']['tag'] = customcfg['sap-a']
            if customcfg.get('sap-b') != None:
                self.sections['containers']['sap-b']['tag'] = customcfg['sap-b']
            if customcfg.get('sap-c') != None:
                self.sections['containers']['sap-c']['tag'] = customcfg['sap-c']
            if customcfg.get('si-groupa') != None:
                self.sections['containers']['si-groupa']['tag'] = customcfg['si-groupa']
            if customcfg.get('si-groupb') != None:
                self.sections['containers']['si-groupb']['tag'] = customcfg['si-groupb']
            if customcfg.get('si-groupc') != None:
                self.sections['containers']['si-groupc']['tag'] = customcfg['si-groupc']
            if customcfg.get('relto-a') != None:
                self.sections['relto']['relto-a']['tag'] = customcfg['relto-a']
            if customcfg.get('relto-b') != None:
                self.sections['relto']['relto-b']['tag'] = customcfg['relto-b']
            if customcfg.get('relto-c') != None:
                self.sections['relto']['relto-c']['tag'] = customcfg['relto-c']
            if customcfg.get('relto-d') != None:
                self.sections['relto']['relto-d']['tag'] = customcfg['relto-d']
            if customcfg.get('relto-e') != None:
                self.sections['relto']['relto-e']['tag'] = customcfg['relto-e']


    def encode(self, classification_string):
        return 0x00000000

    def decode(self, classification_mask):
        if not classification_mask is int:
            raise ValueError(f"Classification mask must be an integer.")
        return ""
