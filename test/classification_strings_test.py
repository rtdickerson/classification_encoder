import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))


from lib.classification_encoder import ClassificationEncoder, NamedBits

def test_parseUNCLASS():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("UNCLASSIFIED")
    assert mask == 0x10000000, "Got %08X" % mask

def test_parseCUI():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("UNCLASSIFIED//CUI")
    assert mask == 0x10002000, "Got %08X" % mask
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("CUI")
    assert mask == 0x10002000, "Got %08X" % mask

def test_parseSECRET_REL_TO_FVEY():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("SECRET//REL TO FVEY")
    assert mask == 0x40000020, "Got %08X" % mask

def test_parseSECRET_REL_TO_FVEY2():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("SECRET//REL TO AUS, CAN, NZL, GBR, USA")
    assert mask == 0x40000020, "Got %08X" % mask    

def test_parseSECRET_REL_TO_NATO():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("SECRET//REL TO NATO")
    assert mask == 0x40000040, "Got %08X" % mask

def test_parseSECRET_REL_TO_NINE():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("SECRET//REL TO AUS, CAN, NZL, GBR, USA, DNK, FRA, NLD, NOR")
    assert mask == 0x40000001, "Got %08X" % mask

def test_parseSECRET_REL_TO_FOURTEEN():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("SECRET//REL TO AUS, CAN, NZL, GBR, USA, DNK, FRA, NLD, NOR, BEL, DEU, ITA, ESP, SWE")
    assert mask == 0x40000002, "Got %08X" % mask

def test_parseSECRET_NOFORN():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("SECRET//NOFORN")
    assert mask == 0x40000080, "Got %08X" % mask

def test_parseTOPSECRET_REL_TO_FVEY():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("TOP SECRET//REL TO FVEY")
    assert mask == 0x80000020, "Got %08X" % mask

def test_parseTOPSECRET_NOFORN():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("TOP SECRET//NOFORN")
    assert mask == 0x80000080, "Got %08X" % mask

def test_parseTOPSECRET_SCI_NOFORN():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("TOP SECRET//SCI//NOFORN")
    assert mask == 0x81000080, "Got %08X" % mask

def test_parseTOPSECRET_GAMMA_NOFORN():
    ce = ClassificationEncoder(None)
    mask = ce.parseClassificationString("TOP SECRET//SI/GAMMA//NOFORN")
    assert mask == 0x81140080, "Got %08X" % mask

def test_parseTOPSECRET_SI_NOFORN():
    cfg = {
        'si-groupa': 'ALPHA',
    }

    ce = ClassificationEncoder(cfg)
    mask = ce.parseClassificationString("TOP SECRET//SI/ALPHA//NOFORN")
    assert mask == 0x81240080, "Got %08X" % mask


def test_parseTOPSECRET_SAP_NOFORN():
    cfg = {
        'sap-a': 'ALPHA',
    }

    ce = ClassificationEncoder(cfg)
    mask = ce.parseClassificationString("TOP SECRET//SAR-ALPHA//NOFORN")
    assert mask == 0x82000080, "Got %08X" % mask
