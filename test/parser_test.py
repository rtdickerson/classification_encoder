import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))


from classification_encoder import ClassificationEncoder, NamedBits


def test_classification_encoder_config1():
    ce = ClassificationEncoder(None)
    assert ce.sections['classification']['unclassified']['tag'] == 'UNCLASSIFIED'
    assert ce.sections['classification']['confidential']['enabled'] == True
    assert ce.sections['classification']['confidential']['tag'] == 'CONFIDENTIAL'
    assert ce.sections['classification']['secret']['tag'] == 'SECRET'
    assert ce.sections['classification']['topsecret']['tag'] == 'TOP SECRET'

def test_classification_encoder_config2():
    cfg = {
        'sap-a': 'ALPHA',
        'sap-b': 'BRAVO',
        'sap-c': 'CHARLIE'
    }
    ce = ClassificationEncoder(cfg)

    assert ce.sections['containers']['sci']['tag'] == 'SCI'
    assert ce.sections['containers']['sap-a']['tag'] == 'ALPHA'
    assert ce.sections['containers']['sap-a']['enabled'] == True
    assert ce.sections['containers']['sap-b']['tag'] == 'BRAVO'
    assert ce.sections['containers']['sap-c']['tag'] == 'CHARLIE'

def test_classification_encoder_config3():
    cfg = {
        'si-groupa': 'ALPHA',
        'si-groupb': 'BRAVO',
        'si-groupc': 'CHARLIE'
    }

    ce = ClassificationEncoder(cfg)

    assert ce.sections['containers']['sci']['tag'] == 'SCI'
    assert ce.sections['containers']['si-groupa']['tag'] == 'ALPHA'
    assert ce.sections['containers']['si-groupa']['enabled'] == True
    assert ce.sections['containers']['si-groupb']['tag'] == 'BRAVO'
    assert ce.sections['containers']['si-groupc']['tag'] == 'CHARLIE'

def test_classification_encoder_config4():
    cfg = {
        'relto-a': 'REL TO NZL, GBR, XXX',
        'relto-b': 'REL TO NZL, GBR, USA, FRA, DEU',
        'relto-c': 'REL TO NZL, GBR'
    }

    ce = ClassificationEncoder(cfg)

    assert ce.sections['containers']['sci']['tag'] == 'SCI'
    assert ce.sections['distribution']['relto-a']['tag'] == 'REL TO NZL, GBR, XXX'
    assert ce.sections['distribution']['relto-a']['enabled'] == True
    assert set(ce.sections['distribution']['relto-a']['countries']) == set(["GBR", "NZL"])
    assert ce.sections['distribution']['relto-b']['tag'] == 'REL TO NZL, GBR, USA, FRA, DEU'
    assert ce.sections['distribution']['relto-b']['enabled'] == True
    assert set(ce.sections['distribution']['relto-b']['countries']) == set(["GBR", "NZL", "USA", "FRA", "DEU"])
    assert ce.sections['distribution']['relto-c']['tag'] == 'REL TO NZL, GBR'
    assert ce.sections['distribution']['relto-c']['enabled'] == True
    assert set(ce.sections['distribution']['relto-c']['countries']) == set(["GBR", "NZL"])

def test_relto_generator():
    ce = ClassificationEncoder(None)

    S = ce.makeReltoString(NamedBits.RELTO_NATO)
    assert S == "REL TO NATO"
    S = ce.makeReltoString(NamedBits.RELTO_FVEY)
    assert S == "REL TO AUS, CAN, NZL, GBR, USA"


def test_splitting_classiciation():
    ce = ClassificationEncoder(None)
    parts = ce.splitOnClearanceSeparator("SECRET//SI-GROUPA//REL TO USA, GBR")
    assert len(parts) == 3
    assert parts[0] == "SECRET"
    assert parts[1] == 'SI-GROUPA'
    assert parts[2] == "REL TO USA, GBR"
    parts = ce.splitOnClearanceSeparator("SECRET//SI/GROUPA//REL TO USA, GBR")
    assert len(parts) == 4
    assert parts[0] == "SECRET"
    assert parts[1] == "SI"
    assert parts[2] == 'GROUPA'
    assert parts[3] == "REL TO USA, GBR"

def test_handlerelto():
    cfg = {
        'relto-a': 'REL TO NZL, GBR, ITA',
        'relto-b': 'REL TO NZL, GBR, USA, FRA, DEU',
        'relto-c': 'REL TO NZL, GBR'
    }
    ce = ClassificationEncoder(cfg)
    WKS = "REL TO NATO"
    assert ce.handleRelto(WKS) == NamedBits.RELTO_NATO.value
    WKS = "REL TO FVEY"
    assert ce.handleRelto(WKS) == NamedBits.RELTO_FVEY.value
    WKS = "REL TO AUS, CAN, NZL, GBR, USA"
    assert ce.handleRelto(WKS) == NamedBits.RELTO_FVEY.value
    WKS = "REL TO CAN, AUS,  NZL, USA, GBR"
    assert ce.handleRelto(WKS) == NamedBits.RELTO_FVEY.value
    WKS = "REL TO AUS, CAN, NZL, GBR, USA, DNK, FRA, NLD, NOR"
    assert ce.handleRelto(WKS) == NamedBits.RELTO_NINEEYES.value
    WKS = "REL TO %s" % ", ".join(["AUS", "CAN", "NZL", "GBR", "USA", "DNK", "FRA", "NLD", "NOR", "DEU", "ESP", "ITA", "SWE", "BEL"])
    assert ce.handleRelto(WKS) == NamedBits.RELTO_FOURTEENEYES.value
    WKS = "REL TO NZL, GBR, ITA"
    assert ce.handleRelto(WKS) == NamedBits.RELTO_A.value
    WKS = "REL TO NZL, GBR, USA, FRA, DEU"
    assert ce.handleRelto(WKS) == NamedBits.RELTO_B.value
    WKS = "REL TO NZL, GBR"
    assert ce.handleRelto(WKS) == NamedBits.RELTO_C.value
 
