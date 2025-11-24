"""
clean_sdoh.py
-------------
Cleans the Social Determinants of Health (SDOH) dataset by:
1. Pivoting long → wide
2. Converting numeric columns
3. Imputing missing values
4. Saving the clean output as CSV
"""

import pandas as pd
import numpy as np

RAW_PATH = "data/raw/SDOH_Indicators.xlsx"
OUT_PATH = "data/processed/SDOH_Clean_Wide.csv"

def load_sdoh(path=RAW_PATH):
    print(f"Loading SDOH data from: {path}")
    return pd.read_excel(path)

def clean_sdoh(df):
    print("Cleaning SDOH...")

    # Pivot long → wide
    df_wide = df.pivot_table(
        index=["Geography", "Year"],
        columns="Indicator",
        values="Value"
    ).reset_index()

    # Make all numeric columns numeric
    for col in df_wide.columns:
        if col not in ["Geography", "Year"]:
            df_wide[col] = pd.to_numeric(df_wide[col], errors="coerce")

    # Impute missing with median
    df_wide = df_wide.fillna(df_wide.median(numeric_only=True))

    # Standardize column
    df_wide["Geography_clean"] = df_wide["Geography"].str.lower().str.strip()

    print("SDOH cleaned successfully ✔")
    return df_wide

def save_sdoh(df, out_path=OUT_PATH):
    df.to_csv(out_path, index=False)
    print(f"Saved cleaned SDOH to: {out_path}")

if __name__ == "__main__":
    df = load_sdoh()
    df_clean = clean_sdoh(df)
    save_sdoh(df_clean)
