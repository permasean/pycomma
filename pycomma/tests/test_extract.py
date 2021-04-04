"""
This file contains tests for the extraction functions within class Comma
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

def test_extract_header_from_file():
    comma = Comma(test_data_with_header_path)
    comma._manual_load_csv_for_testing()

    header = comma._extract_header_from_file()
    assert len(header) > 0

    comma._manual_close_file_for_testing()
    assert comma.file_is_closed() == True

def test_extract_data_from_file():
    comma = Comma(test_data_without_header_path)
    comma._manual_load_csv_for_testing()

    data = comma._extract_data_from_file()
    assert len(data) > 0
    
    comma._manual_close_file_for_testing()
    assert comma.file_is_closed() == True

    
    