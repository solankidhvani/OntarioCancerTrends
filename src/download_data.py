"""
download_data.py
-----------------
Optional helper script for downloading or validating raw data files.
If PHO datasets require manual download, this script simply checks
whether the expected files exist.
"""

import os

RAW_DIR = "data/raw"

EXPECTED_FILES = [
    "PHO_Cancer_Incidence_2010_2014.xlsx",
    "PHO_Cancer_Mortality_2003_2015.xlsx",
    "SDOH_Indicators.xlsx"
]

def ensure_raw_folder():
    if not os.path.exists(RAW_DIR):
        os.makedirs(RAW_DIR)
        print(f"Created folder: {RAW_DIR}")

def check_files():
    print("\nChecking raw dataset availability...\n")
    missing = []
    for f in EXPECTED_FILES:
        path = os.path.join(RAW_DIR, f)
        if not os.path.exists(path):
            missing.append(f)
            print(f"❌ Missing: {path}")
        else:
            print(f"✔ Found: {path}")

    if missing:
        print("\n⚠ Some files are missing. Please manually download them into:")
        print(f"   {RAW_DIR}")
    else:
        print("\nAll raw files are available! ✔")

if __name__ == "__main__":
    ensure_raw_folder()
    check_files()
