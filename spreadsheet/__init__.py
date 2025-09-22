from __future__ import annotations
import re
from typing import Dict, Tuple


class Spreadsheet:
    """
    26 columns (A..Z), N rows (1-indexed). Each cell holds int in [0, 1e5].
    Unset cells read as 0.
    """

    COLS = 26
    MAX_CELL_VALUE = 10**5

    def __init__(self, rows: int):
        if rows <= 0:
            raise ValueError("rows must be positive")
        self.rows = rows
        # store only non-zero cells (sparse)
        self._grid: Dict[Tuple[int, int], int] = {}

    # ---------- core cell helpers ----------

    def _parse_cell(self, cell: str) -> Tuple[int, int]:
        """
        Returns (row, col) as 1-indexed.
        Accepts exactly 'A1'..'Z<rows>' (uppercase A-Z).
        """
        if not isinstance(cell, str):
            raise TypeError("cell must be a string like 'A1'")
        m = re.fullmatch(r"([A-Z])([1-9]\d*)", cell.strip())
        if not m:
            raise ValueError(f"invalid cell reference: {cell!r}")
        col_letter, row_s = m.groups()
        row = int(row_s)
        col = ord(col_letter) - ord("A") + 1
        if not (1 <= col <= self.COLS):
            raise ValueError("column out of range")
        if not (1 <= row <= self.rows):
            raise ValueError("row out of range")
        return row, col

    def _get_cell_value(self, cell: str) -> int:
        r, c = self._parse_cell(cell)
        return self._grid.get((r, c), 0)

    # ---------- public API ----------

    def setCell(self, cell: str, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("value must be int")
        if not (0 <= value <= self.MAX_CELL_VALUE):
            raise ValueError("value out of allowed range [0, 1e5]")
        r, c = self._parse_cell(cell)
        if value == 0:
            self._grid.pop((r, c), None)
        else:
            self._grid[(r, c)] = value

    def resetCell(self, cell: str) -> None:
        r, c = self._parse_cell(cell)
        self._grid.pop((r, c), None)

    def getValue(self, formula: str) -> int:
        """
        Evaluate formulas of the form '=X+Y' where X,Y are either:
          - cell refs like 'A1' (uppercase A-Z, 1-indexed row)
          - non-negative integers in [0, 1e5]
        Returns X + Y as an int. Unset cells count as 0.
        """
        if not isinstance(formula, str):
            raise TypeError("formula must be a string")
        s = formula.strip()
        if not s.startswith("="):
            raise ValueError("formula must start with '='")
        body = s[1:]
        parts = body.split("+")
        if len(parts) != 2:
            raise ValueError("only binary + supported (exactly one '+')")
        a_tok, b_tok = (p.strip() for p in parts)
        a = self._value_of_token(a_tok)
        b = self._value_of_token(b_tok)
        return a + b

    # ---------- parsing tokens ----------

    def _value_of_token(self, token: str) -> int:
        if token.isdigit():
            v = int(token)
            if v > self.MAX_CELL_VALUE:
                raise ValueError("literal exceeds 1e5")
            return v
        # otherwise treat as cell reference
        return self._get_cell_value(token)
