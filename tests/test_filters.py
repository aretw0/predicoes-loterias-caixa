import pytest
from loterias.filters import PredictionFilter

def test_filter_parsing():
    f = PredictionFilter("sum:10-20,odd:2-3,even:4")
    assert f.filters['sum'] == (10, 20)
    assert f.filters['odd'] == (2, 3)
    assert f.filters['even'] == (4, 4)

def test_sum_validation():
    f = PredictionFilter("sum:10-20")
    assert f.validate([5, 5]) is True # 10
    assert f.validate([10, 10]) is True # 20
    assert f.validate([1, 2]) is False # 3 (too low)
    assert f.validate([10, 15]) is False # 25 (too high)

def test_odd_validation():
    f = PredictionFilter("odd:2") # Exactly 2 odds
    assert f.validate([1, 3, 2, 4]) is True # 1, 3 are odd (2 total)
    assert f.validate([1, 2, 4, 6]) is False # 1 is odd (1 total)
    assert f.validate([1, 3, 5, 2]) is False # 3 total

def test_even_validation():
    f = PredictionFilter("even:1-2") 
    assert f.validate([2, 1, 3]) is True # 1 even
    assert f.validate([2, 4, 1]) is True # 2 even
    assert f.validate([1, 3, 5]) is False # 0 even

def test_combined_filters():
    # Sum between 6 and 10, Exactly 1 odd
    f = PredictionFilter("sum:6-10,odd:1")
    
    assert f.validate([2, 4, 1]) is True # Sum 7, 1 odd -> OK
    assert f.validate([2, 4, 2]) is False # Sum 8, 0 odds -> Fail
    assert f.validate([5, 7]) is False # Sum 12, 2 odds -> Fail
