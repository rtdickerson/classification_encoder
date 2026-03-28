import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))


from classification_encoder import ClassificationEncoder, NamedBits

def test_build_classification_SEC_NOFORN ():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("SECRET//NOFORN")
    cstr = ce.constructClassificationString(val)
    assert cstr == "SECRET//NOFORN"

def test_build_classification_CUI ():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("CUI")
    cstr = ce.constructClassificationString(val)
    assert cstr == "CUI"

def test_build_classification_UNCLASS ():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("UNCLASSIFIED")
    cstr = ce.constructClassificationString(val)
    assert cstr == "UNCLASSIFIED"

def test_build_classification_UNCLASS_SBU ():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("UNCLASSIFIED//SBU")
    cstr = ce.constructClassificationString(val)
    assert cstr == "UNCLASSIFIED//SBU"


def test_build_classification_CONFID ():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("CONFIDENTIAL")
    cstr = ce.constructClassificationString(val)
    assert cstr == "CONFIDENTIAL"

def test_build_classification_SECRET ():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("SECRET")
    cstr = ce.constructClassificationString(val)
    assert cstr == "SECRET"

def test_build_classification_TOPSECRET():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("TOP SECRET")
    cstr = ce.constructClassificationString(val)
    assert cstr == "TOP SECRET"

def test_build_classification_SECRET_FVEY():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("SECRET//REL TO FVEY")
    cstr = ce.constructClassificationString(val)
    assert cstr == "SECRET//REL TO AUS, CAN, NZL, GBR, USA"

def test_build_classification_SECRET_FVEY2():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("SECRET//REL TO AUS, CAN, NZL, GBR, USA")
    cstr = ce.constructClassificationString(val)
    assert cstr == "SECRET//REL TO AUS, CAN, NZL, GBR, USA"

def test_build_classification_SECRET_SIG():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("SECRET//SI-GAMMA/TK//NOFORN")
    cstr = ce.constructClassificationString(val)
    assert cstr == "SECRET//SI-GAMMA/TK//NOFORN"

def test_build_classification_SECRET_SIG2():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("SECRET//SI-GAMMA/TK//NOFORN")
    cstr = ce.constructClassificationString(val)
    assert cstr == "SECRET//SI-GAMMA/TK//NOFORN"

def test_build_classification_SECRET_SIA():
    cfg = {
        'sap-a' : "SAP-ALPHA",
        'si-groupa': 'ALPHA',
        'si-groupb': 'BRAVO',
        'si-groupc': 'CHARLIE'
    }
    ce = ClassificationEncoder(cfg)
    val = ce.parseClassificationString("SECRET//SI-ALPHA/TK//NOFORN")
    cstr = ce.constructClassificationString(val)
    assert cstr == "SECRET//SI-ALPHA/TK//NOFORN"

def test_build_classification_SECRET_SAPA():
    cfg = {
        'sap-a' : "ALPHA",
        'si-groupa': 'ALPHA',
        'si-groupb': 'BRAVO',
        'si-groupc': 'CHARLIE'
    }
    ce = ClassificationEncoder(cfg)
    val = ce.parseClassificationString("SECRET//SAR-ALPHA//SI/TK//NOFORN")
    cstr = ce.constructClassificationString(val)
    assert cstr == "SECRET//SAR-ALPHA//SI/TK//NOFORN"

def test_build_classification_SECRET_HCS_P_HCS_O():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("SECRET//HCS-P/HCS-O//NOFORN")
    cstr = ce.constructClassificationString(mask)
    assert cstr == "SECRET//HCS-O/HCS-P//NOFORN"
