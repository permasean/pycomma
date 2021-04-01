"""
This file contains tests for the prepare() function within class Comma.
Each test function represents a test case for the function's behavior 
when class properties it depends on are set to certain values. 
"""
from ..comma import Comma
import pytest
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
test_data_with_header_path = os.path.join(
    current_dir, 
    "test_data_with_header.csv"
)

test_data_without_header_path = os.path.join(
    current_dir,
    "test_data_without_header.csv"
)

def test_prepare_when_prepared_is_true():
    comma = Comma(test_data_with_header_path)
    assert comma._get_prepared() == False
    comma.prepare()
    assert comma._get_prepared() == True
    
    with pytest.raises(Exception) as excinfo:
        comma.prepare()

    assert comma.file_is_closed() == True

def test_prepare_when_includes_header_is_true_and_prepared_is_false():
    comma = Comma(test_data_with_header_path, includes_header=True)
    assert comma._get_includes_header() == True
    assert comma._get_prepared() == False
    comma.prepare()
    assert comma._get_prepared() == True
    assert comma.file_is_closed() == True

def test_prepare_when_includes_header_is_false_and_prepared_is_false():
    comma = Comma(test_data_without_header_path, includes_header=False)
    assert comma._get_includes_header() == False
    assert comma._get_prepared() == False
    comma.set_header([])

    with pytest.raises(Exception) as excinfo:
        comma.prepare()
    
    assert comma._get_prepared() == False
    assert comma.file_is_closed() == True

def test_prepare_when_includes_header_is_false_and_header_is_default_value():
    comma = Comma(test_data_without_header_path, includes_header=False)
    assert comma._get_includes_header() == False
    assert isinstance(comma.get_header(), list)
    assert len(comma.get_header()) == 0
    
    with pytest.raises(Exception) as excinfo:
        comma.prepare()
    
    assert comma.file_is_closed() == True