import os
import sys


#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

from lib.classification_encoder import ClassificationEncoder, NamedBits

def test_compare1():
    ce = ClassificationEncoder(None)
    val = ce.parseClassificationString("SECRET//REL TO FVEY")
    print ("val 0x%08x" % val)
    assert ce.compareTwo(val, val) == ce.COMPARE_EQUAL 

def test_compare2():
    ce = ClassificationEncoder(None)
    assert ce.compareTwo(0x10000020, 0x10000080) == ce.COMPARE_SECOND

def test_compare3():
    ce = ClassificationEncoder(None)
    assert ce.compareTwo(0x10000020, 0x40000020) == ce.COMPARE_SECOND

def test_compare4():
    ce = ClassificationEncoder(None)
    assert ce.compareTwo(0x40000020, 0x10000020) == ce.COMPARE_FIRST