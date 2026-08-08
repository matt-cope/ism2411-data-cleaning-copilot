"""
data_cleaning.py

Purpose:
This script cleans the raw sales dataset (data/raw/sales_data_raw.csv) and
writes a cleaned version to data/processed/sales_data_clean.csv.

The raw file has several real-world data quality problems:
    - Column headers with inconsistent casing and extra spaces
      (e.g. " CATEGORY ", "  date_sold")
    - Product names / categories with leading/trailing whitespace and
      inconsistent capitalization (e.g. "USB Cable" vs "usb cable ")
    - Missing price and quantity values
    - Invalid values: negative prices, negative quantities, and a $0.00 price
    - A couple of exact duplicate rows

Two of the functions below (clean_column_names and handle_missing_values)
started as GitHub Copilot suggestions generated from the docstring/comment
above each function signature. I reviewed each suggestion and modified the
logic, variable names, and edge cases to match this specific dataset -- see
reflection.md for details on what Copilot produced vs. what I changed.
"""

import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load the raw sales CSV into a DataFrame.

    Why: centralizing the read_csv call in one function makes it easy to
    swap file paths or add read options (encoding, dtype, etc.) later
    without touching the rest of the pipeline.
    """
    df = pd.read_csv(file_path, skipinitialspace=True)
    return df


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Copilot-assisted function.

    What: Standardize column names to lowercase, underscore-separated
    names with no leading/trailing whitespace
    (e.g. " CATEGORY " -> "category", "  date_sold" -> "date_sold").

    Why: the raw headers have inconsistent spacing and casing, which makes
    referencing columns by name (df["category"]) unreliable and error-prone.
    """
    # Copilot's first suggestion only did df.columns.str.strip().str.lower().
    # I extended it to also replace internal spaces with underscores, since
    # a couple of headers in this file have multiple words / stray spaces
    # (e.g. "qty ,   date_sold").
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Copilot-assisted function.

    What: Clean up text fields (strip whitespace, collapse extra internal
    spaces) and drop rows that are missing a price or quantity, since we
    can't calculate revenue for those rows.

    Why: product/category text has stray whitespace that would otherwise
    cause "Electronics" and " electronics " to be treated as different
    groups. Missing price/qty rows are incomplete transactions -- rather
    than guessing a fill value (which could distort totals), we drop them
    and note that decision here and in reflection.md.
    """
    df = df.copy()

    # Copilot originally suggested df.fillna(0) for every column, which
    # would have silently turned missing prices/quantities into 0 and
    # corrupted the data. I changed this to explicitly strip text columns
    # and drop rows missing price or qty instead, since those are the two
    # numeric fields required for any downstream sales analysis.
    for col in ["prodname", "category"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )

    df = df.dropna(subset=["price", "qty"])

    return df


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    What: Remove rows with clearly invalid values -- negative quantity,
    negative price, or a price of exactly $0.00 -- and drop exact
    duplicate rows.

    Why: negative prices/quantities are data entry errors (a sale can't
    have negative revenue or negative units sold), and a $0.00 price is
    not a real transaction. Exact duplicate rows likely mean the same
    sale was logged twice.
    """
    df = df.copy()

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce")

    df = df[(df["price"] > 0) & (df["qty"] > 0)]
    df = df.drop_duplicates()

    return df


if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())
