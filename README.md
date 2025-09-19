# Spreadsheet Kata

Run tests with:
```bash
pytest
```

## Usage
```py
from spreadsheet import Spreadsheet
ss = Spreadsheet(rows=10)
ss.setCell("A1", 5)
ss.setCell("B2", 7)
print(ss.getValue("=A1+B2"))  # 12
```
