"""
This file contains tests for the history-related functions within class Comma.
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

def test_undo_when_console_mode_is_false():
    comma = Comma(test_data_with_header_path, console_mode=False)
    assert comma._get_console_mode() == False

    with pytest.raises(Exception) as excinfo:
        comma.undo()
    