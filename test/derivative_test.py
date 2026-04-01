import sys
import os 

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))


from lib.classification_encoder import ClassificationEncoder, NamedBits, DerivativeClassificationEncoder

def test_derivative_0_nonZero():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("UNCLASSIFIED")
    newmask = DerivativeClassificationEncoder.constructClassificationString(mask, 0)
    assert newmask == mask, "Got %08X" % newmask
    newmask = DerivativeClassificationEncoder.constructClassificationString(0, mask)
    assert newmask == mask, "Got %08X" % newmask

def test_derivative_config1():
    cfg = {
        'sap-a' : "SAP-ALPHA",
        'si-groupa': 'ALPHA',
        'si-groupb': 'BRAVO',
        'si-groupc': 'CHARLIE'
    }
    ce = ClassificationEncoder(cfg)
    mask1 = ce.parseClassificationString("UNCLASSIFIED")
    mask2 = ce.parseClassificationString("CONFIDENTIAL")
    expected = ce.parseClassificationString("CONFIDENTIAL")
    newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
    assert newmask == expected, "Got %08X, expected %08X C" % (newmask, expected)
    mask1 = ce.parseClassificationString("CONFIDENTIAL")
    mask2 = ce.parseClassificationString("SECRET")
    expected = ce.parseClassificationString("SECRET")
    newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
    assert newmask == expected, "Got %08X, expected %08X S" % (newmask, expected)
    mask1 = ce.parseClassificationString("SECRET")
    mask2 = ce.parseClassificationString("TOP SECRET")
    expected = ce.parseClassificationString("TOP SECRET")
    newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
    assert newmask == expected, "Got %08X, expected %08X TS" % (newmask, expected)

def test_derivative_config2():
    cfg = {
        'sap-a' : "SAP-ALPHA",
        'si-groupa': 'ALPHA',
        'si-groupb': 'BRAVO',
        'si-groupc': 'CHARLIE'
    }
    ce = ClassificationEncoder(cfg)
    mask1 = ce.parseClassificationString("SECRET//NOFORN")
    mask2 = ce.parseClassificationString("SECRET//REL TO FVEY")
    expected = ce.parseClassificationString("SECRET//NOFORN")
    newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
    assert newmask == expected, "Got %08X, expected %08X C" % (newmask, expected)

def test_derivative_config3():
    cfg = {
        'sap-a' : "SAP-ALPHA",
        'si-groupa': 'ALPHA',
        'si-groupb': 'BRAVO',
        'si-groupc': 'CHARLIE'
    }
    ce = ClassificationEncoder(cfg)
    mask1 = ce.parseClassificationString("SECRET//SCI//NOFORN")
    mask2 = ce.parseClassificationString("SECRET//REL TO FVEY")
    expected = ce.parseClassificationString("SECRET//SCI//NOFORN")
    newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
    assert newmask == expected, "Got %08X, expected %08X C" % (newmask, expected)

def test_derivative_config4():
    cfg = {
        'sap-a' : "SAP-ALPHA",
        'si-groupa': 'ALPHA',
        'si-groupb': 'BRAVO',
        'si-groupc': 'CHARLIE'
    }
    ce = ClassificationEncoder(cfg)
    mask1 = ce.parseClassificationString("SECRET//SCI//NOFORN")
    mask2 = ce.parseClassificationString("TOP SECRET//REL TO FVEY")
    expected = ce.parseClassificationString("TOP SECRET//SCI//NOFORN")
    newmask = DerivativeClassificationEncoder.constructClassificationString(mask1, mask2)
    assert newmask == expected, "Got %08X, expected %08X C" % (newmask, expected)
