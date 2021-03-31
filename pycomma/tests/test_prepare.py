from ..comma import Comma
import pytest
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
test_data_path = os.path.join(current_dir, "test_data.csv")

def test_prepare_includes_header_false():
    print(__file__)
    csv_file = open(test_data_path, mode="r", encoding="utf-8")
    comma = Comma(csv_file)
    print(comma.get_data())

if __name__ == "__main__":
    test_prepare_includes_header_false()