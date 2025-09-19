from spreadsheet import Spreadsheet
import pytest


def test_basic_set_get_cell_value_via_formula():
    ss = Spreadsheet(rows=10)
    ss.setCell("A1", 7)
    ss.setCell("B2", 5)
    # =A1+B2 -> 12
    assert ss.getValue("=A1 + B2") == 12


def test_unset_cells_are_zero():
    ss = Spreadsheet(rows=3)
    assert ss.getValue("=A1 + A2") == 0
    ss.setCell("A2", 3)
    assert ss.getValue("=A1 + A2") == 3


def test_reset_cell():
    ss = Spreadsheet(rows=2)
    ss.setCell("Z2", 100)
    ss.resetCell("Z2")
    assert ss.getValue("=Z2 + 0") == 0


def test_literal_plus_cell():
    ss = Spreadsheet(rows=5)
    ss.setCell("C3", 9)
    assert ss.getValue("=1 + C3") == 10
    assert ss.getValue("=C3+1") == 10


def test_supported_examples_from_prompt():
    ss = Spreadsheet(rows=10)
    # Example 1
    ss.setCell(
        "en-US".replace("en-US", "A1"), 1
    )  # not used; just prove we can set anything valid
    ss = Spreadsheet(rows=20)
    ss.setCell("A1", 5)
    ss.setCell("B10", 7)
    assert ss.getValue("=A1+B10") == 12


def test_validation_and_bounds():
    ss = Spreadsheet(rows=3)
    with pytest.raises(ValueError):
        ss.setCell("AA1", 1)  # invalid column format for this problem
    with pytest.raises(ValueError):
        ss.setCell("a1", 1)  # lowercase not allowed
    with pytest.raises(ValueError):
        ss.setCell("A0", 1)  # row 0 invalid
    with pytest.raises(ValueError):
        ss.setCell("A4", 1)  # row out of declared range
    with pytest.raises(ValueError):
        ss.setCell("A1", 100_001)  # exceeds 1e5
    with pytest.raises(ValueError):
        ss.getValue("=A1+A2+A3")  # only one '+'
    with pytest.raises(ValueError):
        ss.getValue("A1+A2")  # missing '='


def test_whitespace_is_ok_and_order_doesnt_matter_for_storage():
    ss = Spreadsheet(rows=2)
    ss.setCell("A1", 2)
    assert ss.getValue("=  A1   +   3 ") == 5
