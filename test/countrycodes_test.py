import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

from classification_encoder import CountryDatabase

def test_country_codes_initialization():
    cc = CountryDatabase()
    assert cc.countries2 != {}
    assert cc.countries3 != {}
    assert cc.nato != set()
    assert cc.fvey != set()
    assert cc.nineEyes != set()
    assert cc.fourteenEyes != set()

def test_country_codes_lookup():
    cc = CountryDatabase()
    assert len(cc.nato) > 0
    assert "USA" in cc.nato
    assert "GBR" in cc.nato
    assert "FRA" in cc.nato
    assert "DEU" in cc.nato
    assert "RUS" not in cc.nato
    assert "CHN" not in cc.nato

def test_country_parser():
    cc = CountryDatabase()
    CL = cc.parseAndValidateRelto("REL TO USA")
    assert "USA" in CL

def test_alpha2lookup():
    cc = CountryDatabase()
    assert cc.getAlpha3ForAlpha2("US") == "USA"
    assert cc.getAlpha3ForAlpha2("GB") == "GBR"
    assert cc.getAlpha3ForAlpha2("XX") == None

def test_country_parser2():
    cc = CountryDatabase()
    CL = cc.parseAndValidateRelto("REL TO US")
    print ("%s" % CL)
    assert "USA" in CL
