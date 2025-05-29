"""Data loading utilities for market names, distance matrix and price table."""
from __future__ import annotations

import os
from typing import Dict, List, Tuple

import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
MARKET_NAMES_TXT: str = os.path.join(BASE_DIR, "market_names.txt")
DISTANCES_XLSX: str = os.path.join(BASE_DIR, "uzaklik.xlsx")
PRICES_XLSX: str = os.path.join(BASE_DIR, "marketler ve fiyatlar 27.05.2025.xlsx")

# ---------------------------------------------------------------------------
# Loader helpers
# ---------------------------------------------------------------------------

def load_market_names(path: str = MARKET_NAMES_TXT) -> List[str]:
    """Load market names from a .txt file (one per line)."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Market names file not found: {path}")
    with open(path, "r", encoding="utf-8") as fp:
        # Read all non-empty lines, strip whitespace, and filter out any remaining empty strings
        markets = [line.strip() for line in fp if line.strip()]
    return markets


def load_distance_matrix(path: str = DISTANCES_XLSX) -> List[List[float]]:
    """Load NxN distance matrix from an Excel file.

    The Excel sheet should contain only numeric distance values.
    Any non-numeric entries are coerced to 0.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Distance file not found: {path}")

    # Read the Excel file without assuming any headers
    df = pd.read_excel(path, header=None)
    
    # Convert all values to numeric, non-numeric become NaN
    df = df.apply(pd.to_numeric, errors='coerce')
    
    # Fill NaN values with 0 and convert to float
    df = df.fillna(0).astype(float)
    
    # Convert to list of lists
    return df.values.tolist()


def load_product_prices(
    market_names: List[str], path: str = PRICES_XLSX
) -> Dict[str, List[float]]:
    """Load product prices per market.

    The first column must contain market names. Remaining columns are products.
    Prices are aligned to *market_names* order. Missing values are treated as 0.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Price file not found: {path}")

    df = pd.read_excel(path)
    df.columns = [str(c).lower().strip() for c in df.columns]
    market_col = df.columns[0]

    df[market_col] = df[market_col].str.strip().str.lower()
    df = df.set_index(market_col)

    # Eliminate duplicate market rows by taking the mean of duplicates
    if df.index.duplicated().any():
        print("[Uyarı] Fiyat dosyasında yinelenen market satırları tespit edildi; ortalama değerler kullanılacak.")
        df = df.groupby(df.index).mean()

    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

    aligned = df.reindex([m.lower() for m in market_names], fill_value=0)
    return {col: aligned[col].astype(float).tolist() for col in aligned.columns}


def load_all() -> Tuple[List[str], List[List[float]], Dict[str, List[float]]]:
    """Convenience loader returning all datasets."""
    markets = load_market_names()
    distances = load_distance_matrix()
    if len(distances) != len(markets):
        raise ValueError("Mismatch between market count and distance matrix size.")
    products = load_product_prices(markets)
    if not products:
        raise ValueError("No product data loaded. Check price file.")
    return markets, distances, products
