# Ontario Cancer Trends Project

## Overview

This project investigates patterns in cancer incidence and mortality across Ontario’s Public Health Units (PHUs) and examines how these patterns relate to social determinants of health (SDOH). By integrating multiple public health datasets and applying machine learning models, the project aims to help Ontario’s health ministries better understand which regions face the greatest burden and which social factors most strongly influence outcomes.

**Business Question:**  

*How can Ontario health departments better allocate limited public health resources to PHUs with the greatest cancer burden, based on SDOH-adjusted risk?*

**Intended Audience:**  

* Ontario government health officials


* Policy makers and funding strategists


* Public health analysts and epidemiologists


---

## Project Structure 


```
OntarioCancerTrends/
│
├── data/
│   ├── raw/                           # Original Excel files (or downloaded using src/download_data.py)
│   │   ├── Cancer_Incidence_Snapshot_Data_2010_2014.xlsx
│   │   ├── Cancer_Mortality_Snapshot_Data_2003_2015.xlsx
│   │   ├── SDOH_Snapshot_Data.xlsx
│   │   └── index-on-marg.xlsx
│   │
│   └── processed/                     # Cleaned datasets used for modelling
│       ├── PHO_Cancer_Incidence_2010_2014.csv
│       ├── PHO_Cancer_Mortality_2003_2015.csv
│       └── SDOH_Clean_Wide.csv
│
├── src/                               # Scripts for reproducibility for repo hygiene
│   ├── download_data.py               # Downloads raw PHO data if too large to store
│   ├── clean_sdoh.py                  # Pivots & cleans SDOH data
│   └── merge_datasets.py              # Harmonizes PHUs and merges datasets for analysis
│
├── models/
│   └── Cancer_SDOH_Model.ipynb        # Main modelling notebook
│
├── images/                            # Model outputs, SHAP values, figures
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
├── notebooks/                         # EDA and experimentation notebooks
│
├── requirements.txt                   # Environment for reproducibility
│
└── README.md

```
---
## Data Sources

1. Cancer Incidence Snapshot (2010–2014):

   `data/processed/PHO_Cancer_Incidence_2010_2014.csv`
    
  * Age standardized incidence rates
     
  * Cancer counts by PHU

   


2. Cancer Mortality Snapshot (2003–2015):
   
    `data/processed/PHO_Cancer_Mortality_2003_2015.csv`  
  
  * Age standardized mortality rates
  
  * Mortality counts by PHU


3. Social Determinants of Health Snapshot:

   `data/raw/SDOH_Snapshot_Data.xlsx` pivoted to wide format and stored in `data/processed/SDOH_Clean_Wide.csv`.  

 * 21 sociodemographic indicators (income, education, housing, labour force stats, etc.)


* PHUs available: 54


* Years: 2016, 2021.


---

## Data Cleaning and Harmonization

**PHU Standardization:**

* Two legacy PHUs (Huron County + Perth District) merged into Huron Perth Public Health.

* All datasets aligned using a unified ```Geography_clean``` key.

**SDOH Cleaning:**

* Original Excel was pivoted from long → wide


* All indicators converted to numeric


* Missing values imputed using median strategy


* Output stored as ```SDOH_Clean_Wide.csv```.

---
## Exploratory Data Analysis (EDA)

**Key EDA steps included:**

* Distribution analysis of age standardized incidence & mortality


* Correlation heatmaps between outcomes and all 21 SDOH indicators


* Trend analysis for high and low performing PHUs


* Clustering of PHUs by demographic similarity

**Notable EDA Findings:**

* PHUs with higher low income rates and higher unemployment consistently showed elevated cancer mortality.


* Incidence was strongly correlated with age based population indicators (e.g. % seniors).


* Northern Ontario PHUs exhibited systematically higher mortality than urban counterparts.


![alt text](https://github.com/solankidhvani/OntarioCancerTrends/blob/main/images/Mortality_SDOH2016%20Correlation.png)

![alt text](https://github.com/solankidhvani/OntarioCancerTrends/blob/main/images/Cancer_Incidence_SDOH2016_Correlation.png)


---
## Summary of Key Findings


The exploratory analysis revealed consistent and meaningful patterns that directly inform the modelling stage:

* Higher cancer mortality is strongly linked to economic vulnerability (low income, unemployment, lone parent households) and to demographic access barriers (recent immigrants, visible minority rate, language barriers).
  
* Cancer incidence patterns are primarily shaped by age structure, PHUs with higher proportions of seniors have systematically higher incidence.
  
* Northern Ontario PHUs exhibit elevated mortality levels, even after adjusting for SDOH indicators, suggesting structural barriers in access to screening and treatment.
  
* Demographically diverse PHUs (especially large urban centres) show higher predicted risk when language or immigration related barriers are present.

These findings motivate the modelling approach and support the development of equitable, SDOH-adjusted resource allocation strategies for Ontario.


---
## Modelling & Methodology

**Feature Engineering**

* Standardized all numeric SDOH variables


* Created a “Geography_clean” key for merging

* Nearest-year alignment:

    * 2014 incidence ↔ 2016 SDOH

    * 2015 mortality ↔ 2016 SDOH

* Merged datasets by PHU & year



**Models Trained**

* Linear Regression


* Lasso Regression


* XGBoost Regressor


* LightGBM Regressor


**Evaluation Metrics**

* R²


* MAE


* RMSE

---
## Model Performance 

| Model             |   R² (Incidence) |    MAE |   RMSE | R² (Mortality) | MAE | RMSE |
| :---------------- | ----------------: | -----: | ------: | -------------: | ---: | ----: |
| Linear Regression | 0.6928 |  8.8404 | 10.4007 | 0.7566 | 3.3465 | 4.6263 |
| Lasso             | 0.7483 |  7.6032 |  9.4141 | 0.8025 | 2.9225 | 4.1668 |
| XGBoost           | 0.7038 |  8.5660 | 10.2130 | **0.9032 (Best)** | **2.0914** | **2.9179** |
| LightGBM          | 0.3737 | 12.6761 | 14.8501 | 0.3170 | 6.0687 | 7.7492 |


Best Model (Mortality): XGBoost

Best Model (Incidence): Lasso

---
## Model Insights (SHAP + Feature Importance)

**Top Predictors of Mortality (XGBoost)**

Strongest demographic drivers:

* Visible minority rate (dominant predictor)

* Recent immigrant rate

* Immigrant rate

* Language barriers (no English/French)

Moderate:

* % seniors

* Housing burden, LIM/LICO (smaller but present)

Interpretation:
Cancer mortality is most strongly associated with demographic vulnerability, suggesting systemic barriers in access to screening and treatment.

**Top Predictors of Incidence (XGBoost)**

* Rate of seniors (major biological driver)

* Visible minority %

* Immigrant %

* Language barriers

* Employment, education, and income factors follow with modest influence.

Interpretation:
Incidence patterns reflect both aging demographics and population diversity.


**LightGBM: Poverty Focused Patterns**

Unlike XGBoost, LightGBM emphasizes:

* Lone parent household rate (#1 predictor)

* Unemployment rate

* Housing cost burden (>30% income)

* Low income measures (LIM/LICO)

Interpretation:
LightGBM reveals that economic hardship is highly predictive of both incidence and mortality.

---
## Figure by Figure Explanations

**XGBoost Feature Importance (Mortality)**

Shows top 25 predictors; dominated by immigration and visible minority indicators.

Interpretation: Mortality disparities heavily reflect demographic and structural access barriers.

**XGBoost Feature Importance (Incidence)**

Seniors dominate incidence prediction, followed by diversity/immigration variables.

Interpretation: Aging + demographic composition drive incidence levels.

**SHAP Summary Plot (Mortality)**

High immigrant/visible minority values push mortality upward.

Interpretation: Clear evidence of healthcare access inequities.

![alt text](https://github.com/solankidhvani/OntarioCancerTrends/blob/main/images/SHAP_XGBoost_Mortality.png)

**SHAP Summary Plot (Incidence)**

Seniors, immigration, visible minority share strongly influence incidence.

Interpretation: Both structural & demographic factors shape incidence.

![alt text](https://github.com/solankidhvani/OntarioCancerTrends/blob/main/images/SHAP_XGBoost_Incidence.png)

**LightGBM Feature Importance (Mortality)**

Economic hardship variables dominate.

Interpretation: Poverty and deprivation strongly shape mortality outcomes.

**LightGBM Feature Importance (Incidence)**

Same pattern: socioeconomic stressors > demographic composition.

Interpretation: Communities facing deprivation experience higher risk.

---
## Insights & Policy Recommendations

**Key Insights**

* Social vulnerability explains a large share of PHU level mortality variation.

* XGBoost accurately identifies high risk PHUs driven by demographic vulnerability.

* LightGBM uncovers parallel patterns where poverty & deprivation strongly shape outcomes.

* Northern/rural PHUs consistently show elevated burden across models.

**Policy Recommendations**

The modelling results highlight clear, actionable patterns that Ontario health officials can use to guide resource allocation:

**Prioritize High Risk PHUs**

Regions consistently predicted to have higher mortality risk include:

* Northern PHUs: Thunder Bay District, Sudbury & District, Porcupine


* Urban High Diversity PHUs: Toronto, Peel, York


* Rural Vulnerable PHUs: Chatham-Kent, Windsor-Essex

These PHUs should be considered priority sites for additional screening capacity, resource deployment, and equity focused programs.

**Expand Equity Oriented Screening and Navigation Services**

Based on XGBoost results showing demographic predictors dominating mortality:

* Provide multilingual screening materials and community health navigators.
  
* Increase funding for immigrant and visible minority support programs.
  
* Improve culturally appropriate cancer awareness outreach in diverse PHUs.

**Target Socioeconomic Barriers Identified by LightGBM**

Since LightGBM elevated poverty indicators:

* Invest in mobile screening clinics in low income and rural PHUs.


* Support income assistance programs tied to cancer screening reminders.


* Extend after hours screening for working families and lone parent households.


**Deploy Structural Support in Northern Ontario**

* Fund teleoncology and remote consult systems.


* Increase permanent oncology staffing.


* Improve transportation subsidies for rural cancer patients.


**Integrate SDOH into Annual Resource Planning**

Use the provided modelling framework to generate annual SDOH-adjusted risk predictions, helping policymakers:

* Forecast emerging high risk PHUs


* Update funding envelopes


* Prioritize interventions with the largest equity impact.


---
## Reproducibility & Environment Setup

**Install Environment**

```bash
git clone <your-repo-url>
cd OntarioCancerTrends
python -m venv venv
source venv/bin/activate     # For macOS/Linux OS
venv\Scripts\activate        # For Windows OS
pip install -r requirements.txt
```
**Run Notebook**

```bash
jupyter notebook models/Cancer_SDOH_Model.ipynb

```
---

## Sample Usage

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
- Regression or time series modeling with SDOH variables as covariates.
- Cluster PHUs based on context and outcomes.
- Trend plots across PHUs or groups.

---

## Caveats
- SDOH available only for years [2016, 2021], while cancer data cover other years. Choose appropriate alignment or averaging.
- Marginalization data is excluded. If included, ensure matching/normalization.
- Huron and Perth units merged post 2020; modify grouping for historical analyses if needed.

---

## Reflection Videos

Links for each member below:

- Glenn Blake : https://drive.google.com/drive/folders/1IiVzJKRIQJTjDRWzy-D6aG3CtFVSg4sV?usp=drive_link

- Alexandre Tugirumubano : https://drive.google.com/drive/folders/1IiVzJKRIQJTjDRWzy-D6aG3CtFVSg4sV?usp=drive_link

- Dhvani Solanki : https://drive.google.com/drive/folders/1IiVzJKRIQJTjDRWzy-D6aG3CtFVSg4sV?usp=drive_link


---
## Project Conclusion


This project provides a comprehensive, SDOH-adjusted understanding of cancer incidence and mortality across Ontario’s Public Health Units. By integrating demographic, socioeconomic, and structural indicators with machine learning models, we identify the PHUs most likely to experience elevated cancer burden.

These results directly address the business question:

*How can Ontario health departments better allocate limited public health resources to PHUs with the greatest cancer burden, based on SDOH-adjusted risk?*

Our findings highlight clear disparities, particularly in Northern regions and high diversity urban centres driven by demographic vulnerability, socioeconomic hardship, and systemic access barriers. These insights equip Ontario health officials, policy makers, and public health analysts with actionable, evidence based guidance for distributing resources, designing targeted screening interventions, and strengthening health equity across the province.

By combining rigorous data processing, explainable ML techniques, and policy focused interpretation, this project offers a scalable framework for annual resource planning and equity oriented decision making across Ontario’s Public Health System. This work enhances transparency, prioritization, and fairness in provincial cancer prevention efforts.

---
## File Summary
- `data/raw/`: Original data files in Excel format.
- `data/processed/PHO_Cancer_Incidence_2010_2014.csv`: Cleaned incidence data.
- `data/processed/PHO_Cancer_Mortality_2003_2015.csv`: Cleaned mortality data.
- `data/processed/SDOH_Clean_Wide.csv`: Pivoted SDOH snapshot.
- `src/`: Scripts for reproducibility and repo hygiene.
- `models/`: Analysis notebooks for modeling.
- `images/`: Model output visualizations/artifacts.
- `reports/`: Analysis reports (PDF).
- `notebooks/`: Jupyter notebooks for analysis and prototyping.
- `requirements.txt/`: Environment for reproducibility.
- `README.md`: This documentation file.
