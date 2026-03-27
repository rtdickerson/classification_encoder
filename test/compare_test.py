import os
import sys


#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

from lib.classification_encoder import ClassificationEncoder, NamedBits
from lib.classification_encoder import MaskComparatorClass


def test_compare1():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("SECRET//REL TO FVEY")
    comp = MaskComparatorClass.compareTwo(val, val)
    assert comp == MaskComparatorClass.COMPARE_EQUAL, f"compate same 0x{val:x}" 

def test_compare2():
    ce = ClassificationEncoder(None)
    val1 = ce.parseClassificationString("SECRET//REL TO FVEY")
    val2 = ce.parseClassificationString("SECRET//NOFORN")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_SECOND

def test_compare3():
    ce = ClassificationEncoder(None)
    val1 = ce.parseClassificationString("UNCLASSIFIED//REL TO FVEY")
    val2 = ce.parseClassificationString("SECRET//NOFORN")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_SECOND

def test_compare_C_U():
    ce = ClassificationEncoder(None)
    val1 = ce.parseClassificationString("CONFIDENTIAL")
    val2 = ce.parseClassificationString("UNCLASSIFIED")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_FIRST

def test_compare_U_C():
    ce = ClassificationEncoder(None)
    val1 = ce.parseClassificationString("UNCLASSIFIED")
    val2 = ce.parseClassificationString("CONFIDENTIAL")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_SECOND

def test_compare_C_S():
    ce = ClassificationEncoder(None)
    val1 = ce.parseClassificationString("CONFIDENTIAL")
    val2 = ce.parseClassificationString("SECRET")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_SECOND

def test_compare_S_TS():
    ce = ClassificationEncoder(None)
    val1 = ce.parseClassificationString("SECRET")
    val2 = ce.parseClassificationString("TOP SECRET")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_SECOND

def test_compare_TS_TS1():
    cfg = {
        'sap-a': 'ALPHA',
    }
    ce = ClassificationEncoder(cfg)
    val1 = ce.parseClassificationString("TOP SECRET//NOFORN")
    val2 = ce.parseClassificationString("TOP SECRET//SAR-ALPHA//REL TO FVEY")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_SECOND

def test_compare_TS_TS2():
    cfg = {
        'sap-a': 'ALPHA',
    }
    ce = ClassificationEncoder(cfg)
    val1 = ce.parseClassificationString("TOP SECRET//SCI//NOFORN")
    val2 = ce.parseClassificationString("TOP SECRET//NOFORN")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_FIRST

def test_compare_TS_TS3():
    cfg = {
        'sap-a': 'ALPHA',
    }
    ce = ClassificationEncoder(cfg)
    val1 = ce.parseClassificationString("TOP SECRET//SI//NOFORN")
    val2 = ce.parseClassificationString("TOP SECRET//NOFORN")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_FIRST

def test_compare_TS_TS4():
    cfg = {
        'sap-a': 'ALPHA',
    }
    ce = ClassificationEncoder(cfg)
    val1 = ce.parseClassificationString("TOP SECRET//SI//NOFORN")
    val2 = ce.parseClassificationString("TOP SECRET//SI//NOFORN")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_EQUAL

def test_compare_TS_TS5():
    ce = ClassificationEncoder(None)
    val1 = ce.parseClassificationString("TOP SECRET//SI//NOFORN")
    val2 = ce.parseClassificationString("TOP SECRET//SI/HCS-O//NOFORN")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_SECOND

def test_compare_TS_TS6():
    ce = ClassificationEncoder(None)
    val1 = ce.parseClassificationString("TOP SECRET//SI-G//NOFORN")
    val2 = ce.parseClassificationString("TOP SECRET//SI//NOFORN")
    comp = MaskComparatorClass.compareTwo(val1, val2)
    assert comp == MaskComparatorClass.COMPARE_FIRST

def test_compare_TS_TS_S():
    ce = ClassificationEncoder(None)
    val1 = ce.parseClassificationString("TOP SECRET//SI-G//NOFORN")
    val2 = ce.parseClassificationString("TOP SECRET//SI//NOFORN")
    val3 = ce.parseClassificationString("SECRET//SI//NOFORN")
    comp = MaskComparatorClass.compareThree(val1, val2, val3)
    assert comp == MaskComparatorClass.COMPARE_FIRST

def test_compare_TS_S_TS():
    ce = ClassificationEncoder(None)
    val1 = ce.parseClassificationString("TOP SECRET//SI//NOFORN")
    val2 = ce.parseClassificationString("SECRET//SI//NOFORN")
    val3 = ce.parseClassificationString("TOP SECRET//SI-G//NOFORN")
    comp = MaskComparatorClass.compareThree(val1, val2, val3)
    assert comp == MaskComparatorClass.COMPARE_THIRD

def test_compare_S_TS_TS():
    ce = ClassificationEncoder(None)
    val1 = ce.parseClassificationString("SECRET//SI//NOFORN")
    val2 = ce.parseClassificationString("TOP SECRET//SI-G//NOFORN")
    val3 = ce.parseClassificationString("TOP SECRET//SI//NOFORN")
    comp = MaskComparatorClass.compareThree(val1, val2, val3)
    assert comp == MaskComparatorClass.COMPARE_SECOND
