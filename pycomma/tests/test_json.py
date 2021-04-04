"""
This file contains tests for the json functions within class Comma.
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

def test_to_json_when_prepared_is_false():
    comma = Comma(test_data_with_header_path)
    assert comma._get_prepared() == False

    with pytest.raises(Exception) as excinfo:
        comma._to_json()

def test_save_as_csv_when_prepared_is_false():
    comma = Comma(test_data_with_header_path)
    assert comma._get_prepared() == False

    with pytest.raises(Exception) as excinfo:
        comma.save_as_csv()