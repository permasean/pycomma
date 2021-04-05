"""
This file contains tests for the config-related functions within class Comma.
"""
from ..comma import Comma
import pytest
import os

def test_set_config_non_str_input_type_for_config():
    comma = Comma("anything.csv")

    with pytest.raises(ValueError) as excinfo:
        comma.set_config(0, False)

def test_set_config_input_value_config_does_not_exist():
    comma = Comma("anything.csv")

    with pytest.raises(ValueError) as excinfo:
        comma.set_config("this_config_does_not_exist", "test")

def test_set_config_success_messages_non_bool_value_type():
    comma = Comma("anything.csv")

    with pytest.raises(ValueError) as excinfo:
        comma.set_config("success_messages", 0)

def test_set_config_success_messages_valid_input_type():
    comma = Comma("anything.csv")
    comma.set_config("success_messages", False)
    assert comma.get_config("success_messages")["value"] == False

def test_set_config_max_row_display_non_int_value_type():
    comma = Comma("anything.csv")
    
    with pytest.raises(ValueError) as excinfo:
        comma.set_config("max_row_display", 0.0)

def test_set_config_max_row_display_int_value_type():
    comma = Comma("anything.csv")
    comma.set_config("max_row_display", 42)
    assert comma.get_config("max_row_display")["value"] == 42

def test_get_config_does_not_exist():
    comma = Comma("anything.csv")
    
    with pytest.raises(ValueError) as excinfo:
        comma.get_config("this_config_does_not_exist")
    
def test_get_config_output_format():
    comma = Comma("anything.csv")
    comma.set_config("max_row_display", 5)

    output = comma.get_config("max_row_display")
    assert isinstance(output, dict)
    assert "config" in output
    assert "value" in output
    assert output["config"] == "max_row_display"
    assert output["value"] == 5