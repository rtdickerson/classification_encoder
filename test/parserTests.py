import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))


from classification_encoder import ClassificationEncoder

def test_classification_encoder_config1():
    ce = ClassificationEncoder(None)
    assert ce.sections['classification']['unclassified']['tag'] == 'UNCLASSIFIED'
    assert ce.sections['classification']['confidential']['tag'] == 'CONFIDENTIAL'
    assert ce.sections['classification']['secret']['tag'] == 'SECRET'
    assert ce.sections['classification']['topsecret']['tag'] == 'TOP SECRET'

def test_classification_encoder_config2():
    cfg = {
        'sap-a': 'SAP-ALPHA',
        'sap-b': 'SAP-BRAVO',
        'sap-c': 'SAP-CHARLIE'
    }
    ce = ClassificationEncoder(None)

    assert ce.sections['containers']['sci']['tag'] == 'SCI'
    assert ce.sections['containers']['sap-a']['tag'] == 'SAP-ALPHA'
    assert ce.sections['containers']['sap-b']['tag'] == 'SAP-BRAVE'
    assert ce.sections['containers']['sap-c']['tag'] == 'SAP-CCHARLIE'