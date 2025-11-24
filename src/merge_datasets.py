"""
merge_datasets.py
-----------------
Merges the SDOH, cancer incidence, and cancer mortality datasets.
Handles PHU name standardization and year alignment.
"""

import pandas as pd

INC_PATH = "data/processed/PHO_Cancer_Incidence_2010_2014.csv"
MORT_PATH = "data/processed/PHO_Cancer_Mortality_2003_2015.csv"
SDOH_PATH = "data/processed/SDOH_Clean_Wide.csv"

OUT_PATH = "data/processed/Merged_Cancer_SDOH.csv"

# PHU name fixes based on 2020 restructuring
PHU_RENAMES = {
    "Huron County Health Unit": "Huron Perth Public Health",
    "Perth District Health Unit": "Huron Perth Public Health"
}

def normalize_geography(df):
    df["Geography"] = df["Geography"].replace(PHU_RENAMES)
    df["Geography_clean"] = df["Geography"].str.lower().str.strip()
    return df

def load_data():
    inc = pd.read_csv(INC_PATH)
    mort = pd.read_csv(MORT_PATH)
    sdoh = pd.read_csv(SDOH_PATH)
    return inc, mort, sdoh

def merge_datasets():
    inc, mort, sdoh = load_data()

    inc = normalize_geography(inc)
    mort = normalize_geography(mort)

    print("Merging datasets...")

    # Year alignment: incidence 2010–2014 → closest SDOH year (2016)
    inc["SDOH_Year"] = 2016
    mort["SDOH_Year"] = 2016

    merged_inc = inc.merge(
        sdoh,
        left_on=["Geography_clean", "SDOH_Year"],
        right_on=["Geography_clean", "Year"],
        how="left"
    )

    merged_mort = mort.merge(
        sdoh,
        left_on=["Geography_clean", "SDOH_Year"],
        right_on=["Geography_clean", "Year"],
        how="left"
    )

    final = pd.concat([merged_inc, merged_mort], ignore_index=True)

    print("Merged dataset created ✔")
    return final

def save_merged(df, path=OUT_PATH):
    df.to_csv(path, index=False)
    print(f"Saved merged dataset → {path}")

if __name__ == "__main__":
    df = merge_datasets()
    save_merged(df)
