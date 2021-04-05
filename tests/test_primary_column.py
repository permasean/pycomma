"""
This file contains tests for the primary_column functions within class Comma.
"""
from ..pycomma.comma import Comma
import pytest
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
test_data_with_header_path = os.path.join(
    current_dir, 
    "test_data_with_header.csv"
)

def test_assign_primary_without_ignore_duplicates():
    comma = Comma(test_data_with_header_path)
    comma.prepare()
    comma.assign_primary("id", ignore_duplicate=False)
    assert comma.get_primary() == "id"

def test_assign_primary_with_ignore_duplicates():
    comma = Comma(test_data_with_header_path)
    comma.prepare()
    comma.assign_primary("work_type", ignore_duplicate=True)
    assert comma.get_primary() == "work_type"

def test_get_primary_column_name():
    comma = Comma(test_data_with_header_path)
    comma.prepare()
    comma.assign_primary("id")
    assert comma.get_primary() == "id"