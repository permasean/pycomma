"""
This file contains tests for the prepare() function within class Comma.
Each test function represents a test case for the function's behavior 
when a dependent class property is set to a certain expected value
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

def test_prepare_when_includes_header_is_true_and_prepared_is_true():
    csv_file = open(test_data_with_header_path, mode="r", encoding="utf-8")
    comma = Comma(csv_file, includes_header=True)
    assert comma._get_prepared() == False
    comma.prepare()
    assert comma._get_prepared() == True
    
    with pytest.raises(Exception) as excinfo:
        comma.prepare()

    csv_file.close()

def test_prepare_when_includes_header_is_true_and_prepared_is_false():
    csv_file = open(test_data_with_header_path, mode="r", encoding="utf-8")
    comma = Comma(csv_file, includes_header=True)
    assert comma._get_prepared() == False
    comma.prepare()
    assert comma._get_prepared() == True
    csv_file.close()

def test_prepare_when_includes_header_is_false_and_prepared_is_false():
    csv_file = open(test_data_without_header_path, mode="r", encoding="utf-8")
    comma = Comma(csv_file, includes_header=False)
    assert comma._get_prepared() == False
    comma.set_header([])

    with pytest.raises(Exception) as excinfo:
        comma.prepare()
    
    assert comma._get_prepared() == False
    csv_file.close()

if __name__ == "__main__":
    print("Hello World!")