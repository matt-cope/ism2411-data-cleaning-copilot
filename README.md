# ism2411-data-cleaning-copilot

A small Python project that cleans a messy sales dataset using pandas, built
with help from GitHub Copilot as part of ISM 2411 (Muma College of Business,
University of South Florida).

## What this project does

`src/data_cleaning.py` loads `data/raw/sales_data_raw.csv`, which contains
common real-world data quality issues (inconsistent column names, extra
whitespace, missing values, and invalid negative/zero numbers), and produces
a cleaned file at `data/processed/sales_data_clean.csv`.

Cleaning steps applied:

1. **Standardize column names** — lowercase, underscore-separated, no
   stray whitespace.
2. **Clean text fields** — strip and collapse whitespace in product names
   and categories.
3. **Handle missing values** — drop rows missing a price or quantity,
   since revenue can't be calculated for those rows.
4. **Remove invalid rows** — drop rows with negative price/quantity or a
   $0.00 price, and remove exact duplicate rows.

## How to run it

```bash
pip install pandas
python src/data_cleaning.py
```

This reads `data/raw/sales_data_raw.csv` and writes the cleaned result to
`data/processed/sales_data_clean.csv`, printing a preview of the first few
rows to the terminal.

## Project structure

```
ism2411-data-cleaning-copilot/
├── data/
│   ├── raw/
│   │   └── sales_data_raw.csv
│   └── processed/
│       └── sales_data_clean.csv     # created by the script
├── src/
│   └── data_cleaning.py
├── README.md
└── reflection.md
```

## Tools used

- Python 3, pandas
- GitHub Copilot (used to generate a starting point for two of the four
  functions in `data_cleaning.py`; see `reflection.md` for what was
  generated vs. modified)
