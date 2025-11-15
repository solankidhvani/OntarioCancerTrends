# Ontario Cancer Trends Project

## Overview
This project investigates trends in cancer incidence and mortality across Ontario's Public Health Units (PHUs), situating these trends within their socio-economic context. The primary objective is to merge and analyze cancer snapshot data with contextual covariates reflecting social determinants of health (SDOH) to better understand how population characteristics relate to disease patterns.

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

## File/Folder Structure
```
OntarioCancerTrends/
│
├── data/
│   ├── raw/
│   │   ├── Cancer_Incidence_Snapshot_Data_2010_2014.xlsx
│   │   ├── Cancer_Mortality_Snapshot_Data_2003_2015.xlsx
│   │   ├── SDOH_Snapshot_Data.xlsx
│   │   └── index-on-marg.xlsx
│   │
│   └── processed/
│       ├── PHO_Cancer_Incidence_2010_2014.csv
│       ├── PHO_Cancer_Mortality_2003_2015.csv
│       └── SDOH_Clean_Wide.csv
│
├── models/
│   └── Cancer_SDOH_Model.ipynb
│
├── images/
│   ├── LightGBM_Incidence.png
│   ├── LightGBM_Mortality.png
│   ├── SHAP_XGBoost_Incidence.png
│   ├── SHAP_XGBoost_Mortality.png
│   ├── XGBoost_Incidence.png
│   ├── XGBoost_Mortality.png
│   └── figures/
│       └── (saved model files and predictions)
│
├── reports/
│   └── regional_cancer_analysis.pdf
│
├── notebooks/
├── scripts/
│
└── README.md
```

---

## Data Cleaning and Harmonization
- **PHU Names:**  
  The old units “Huron County Health Unit” and “Perth District Health Unit” were merged into “Huron Perth Public Health” to reflect their 2020 amalgamation. Names are harmonized across all files.

- **SDOH Pivot and Cleaning:**  
  The SDOH sheet has been pivoted so each PHU-year occupies one row and each indicator its own column. Numeric values are coerced to float; blank values appear as NaN.

  - Indicators: 21 variables (e.g., % immigrant population, % lone parent households, % of households spending more than 30% of income on shelter, % unemployed, labour force participation rate, etc.)
  - PHUs covered: 54
  - Years available: [2016, 2021]

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
- Marginalization data is excluded. If later included, ensure matching and normalization.
- The merger of Huron and Perth units means pre-2020 they were separate jurisdictions; they are unified here. Modify grouping if analysis by pre-merger is desired.

---

## File Summary
- `data/raw/`: Original data files in Excel format.
- `data/processed/PHO_Cancer_Incidence_2010_2014.csv`: Cleaned incidence data.
- `data/processed/PHO_Cancer_Mortality_2003_2015.csv`: Cleaned mortality data.
- `data/processed/SDOH_Clean_Wide.csv`: Pivoted SDOH snapshot.
- `models/Cancer_SDOH_Model.ipynb`: Main analysis notebook with modeling and visualizations.
- `images/`: Model output visualizations and saved model artifacts.
- `reports/regional_cancer_analysis.pdf`: Analysis report.
- `README.md`: This file.
