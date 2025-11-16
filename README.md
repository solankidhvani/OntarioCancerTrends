# Ontario Cancer Trends Project

## Overview
This project investigates trends in cancer incidence and mortality across Ontario's Public Health Units (PHUs), situating these trends within their socio-economic context. The primary objective is [...]  

**Business Question:**  
*How can health departments better allocate their limited funds to best support cancer mortality rates?*

**Intended Audience:**  
Government health officials and policy analysts seeking data-driven insights to inform resource allocation and policy decisions.

---

## Data Sources
- **Cancer Incidence Snapshot (2010–2014):**  
  `data/processed/PHO_Cancer_Incidence_2010_2014.csv`  
  Contains counts and age-standardized rates for all cancer types across PHUs.

- **Cancer Mortality Snapshot (2003–2015):**  
  `data/processed/PHO_Cancer_Mortality_2003_2015.csv`  
  Contains counts and age-standardized rates for all cancer types across PHUs.

- **SDOH Data:**  
  Original Excel (`data/raw/SDOH_Snapshot_Data.xlsx`) pivoted to wide format and stored in `data/processed/SDOH_Clean_Wide.csv`.  
  Contains socio-economic indicator percentages for PHUs.

---

## File/Folder Structure & Directory Descriptions

```
OntarioCancerTrends/
│
├── data/
│   ├── raw/                # Original raw Excel data files as received from PHO and Statistics Canada
│   └── processed/          # Cleaned and pre-processed data files (CSV) ready for analysis/modeling
│
├── models/                 # Jupyter notebooks for analytic and statistical modeling (e.g., regression, ML)
│
├── images/                 # Figures and image files output by the models or notebooks (plots, SHAP values, etc.)
│   └── figures/            # Additional subfolder for storing model-generated outputs and prediction files
│
├── reports/                # Final analysis reports, typically in PDF format
│
├── notebooks/              # Jupyter notebooks for exploratory analysis, visualizations, reporting, and prototyping
│
└── README.md               # This documentation file
```

### Directory Details

- **data/raw/**:  
  Contains all unaltered, original input files including cancer incidence/mortality snapshots and SDOH indicator Excel sheets.  
  Example: Cancer_Incidence_Snapshot_Data_2010_2014.xlsx

- **data/processed/**:  
  Contains cleaned CSV-formatted datasets derived from the raw Excel files. All harmonization, pivoting, renaming, and NA processing is reflected here.  
  Example: PHO_Cancer_Incidence_2010_2014.csv

- **models/**:  
  Contains main modeling and analysis notebooks—typically, these notebooks house the workflow for feature engineering, model building (e.g., LightGBM/XGBoost), and in-depth exploratory data anal[...]  

- **images/**:  
  Contains static image outputs and visualization assets generated during data analysis and modeling.  
  Includes subfolder **images/figures/** for more granular model outputs (e.g., prediction results).

- **reports/**:  
  Contains summarized project deliverables and findings as formal reports for stakeholders (usually in PDF).

- **notebooks/**:  
  Jupyter notebooks supporting exploratory data analysis, intermediate experiments, data visualization, and results presentation. Notebooks here may be in-development, contain draft analyses, or s[...]  

- **scripts/**:  
  (If present and populated) Utility or helper scripts for repeatable data processing, batch running, or transformations outside notebooks.

- **README.md**:  
  You're reading it! This document provides project context, usage, and supporting details.

---

## Data Cleaning and Harmonization
- **PHU Names:**  
  The old units “Huron County Health Unit” and “Perth District Health Unit” are merged into “Huron Perth Public Health” for 2020+; all names are harmonized.

- **SDOH Pivot and Cleaning:**  
  SDOH sheet is pivoted so each PHU-year is a row, indicators are columns. Numeric conversion, blank-as-NaN, etc.

  - Indicators: 21 socio-demographic/economic variables
  - PHUs covered: 54
  - Years: [2016, 2021]

---

## Usage Instructions
To load the data in Python:
```python
import pandas as pd
inc = pd.read_csv("data/processed/PHO_Cancer_Incidence_2010_2014.csv")
mort = pd.read_csv("data/processed/PHO_Cancer_Mortality_2003_2015.csv")
sdoh = pd.read_csv("data/processed/SDOH_Clean_Wide.csv")
```
Create a clean key for merging:
```python
for df in (inc, mort, sdoh):
    df["Geography_clean"] = df["Geography"].str.strip().str.lower()
```
Perform a merge:
```python
merged = inc.merge(sdoh, on=["Geography_clean", "Year"], how="left")
```
Adjust `how` param as needed (e.g., left, inner, outer). Handle NaNs explicitly.

---

## Analysis Ideas
- Correlate incidence/mortality with SDOH indicators.
- Regression or time-series modeling with SDOH variables as covariates.
- Cluster PHUs based on context and outcomes.
- Trend plots across PHUs or groups.

---

## Caveats
- SDOH available only for years [2016, 2021], while cancer data cover other years. Choose appropriate alignment or averaging.
- Marginalization data is excluded. If included, ensure matching/normalization.
- Huron and Perth units merged post-2020; modify grouping for historical analyses if needed.

---

## Team Member Video Reflections
- Team Member Video Reflections: https://drive.google.com/drive/folders/1IiVzJKRIQJTjDRWzy-D6aG3CtFVSg4sV?usp=drive_link

---

## File Summary
- `data/raw/`: Original data files in Excel format.
- `data/processed/PHO_Cancer_Incidence_2010_2014.csv`: Cleaned incidence data.
- `data/processed/PHO_Cancer_Mortality_2003_2015.csv`: Cleaned mortality data.
- `data/processed/SDOH_Clean_Wide.csv`: Pivoted SDOH snapshot.
- `models/`: Analysis notebooks for modeling.
- `images/`: Model output visualizations/artifacts.
- `reports/`: Analysis reports (PDF).
- `notebooks/`: Jupyter notebooks for analysis and prototyping.
- `README.md`: This documentation file.
