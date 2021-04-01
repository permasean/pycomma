"""
This file contains tests for the configuration of the header property
within class Comma, given certain values of properties it depends on.
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

def test_header_set_when_includes_header_is_true():
    comma = Comma(test_data_with_header_path)
    with pytest.raises(Exception) as excinfo:
        comma.set_header([])

def test_header_set_when_includes_header_is_false():
    header = []
    comma = Comma(test_data_without_header_path, includes_header=False)
    comma.set_header(header)
    assert comma.get_header() == header

def test_header_set_with_non_list_datatype():
    comma = Comma(test_data_without_header_path, includes_header=False)
    with pytest.raises(Exception) as excinfo:
        comma.set_header("random")

    