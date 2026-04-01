##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##

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

'''

import os
import importlib
from pathlib import Path

from .bitmask import NamedBits
from .bitmask import BitmaskManager
from .countrydatabase import CountryDatabase
from .classification_encoder import ClassificationEncoder
from .mask_compare import MaskComparatorClass
from .derivative import DerivativeClassificationEncoder

# List to store all exported names
__all__ = ["NamedBits", "BitmaskManager", "CountryDatabase", "ClassificationEncoder","MaskComparatorClass","DerivativeClassificationEncoder"]

    
##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##
