# Oil Well Production Forecasting

                                                                         **STILL WORKING ON IT**

This project explores forecasting oil production from real-world well production data using both traditional reservoir engineering techniques and modern machine learning methods.

The dataset used is the Volve Field production dataset, containing production volumes, pressure measurements, temperature readings, choke settings, and other operational data collected from multiple offshore wells.

---

## Project Goals

The objective is to compare:

1. **Arps Decline Curve Analysis (DCA)** — a traditional reservoir engineering forecasting method.
2. **XGBoost Time-Series Forecasting** — a machine learning approach using lagged production and engineered features.

The final result will compare forecast accuracy, explain model behavior, and evaluate where each approach succeeds or fails.

---

## Dataset

Key production variables include:

* Oil Production Volume (`BORE_OIL_VOL`)
* Gas Production Volume (`BORE_GAS_VOL`)
* Water Production Volume (`BORE_WAT_VOL`)
* Downhole Pressure
* Wellhead Pressure
* Choke Size
* On-Stream Hours
* Production Flow Type

After cleaning:

* ~8,000 production records
* 6 producing wells
* Production period: 2007–2016

---

## Current Progress

###  Phase 1 — Data Loading & Cleaning (IMPLEMENTED)

Implemented:

* Excel ingestion pipeline
* Column validation
* Datetime parsing
* Production-only filtering
* Shut-in day removal
* Feature engineering:

  * Gas-Oil Ratio (GOR)
  * Water Cut (WCT)
  * Drawdown Pressure
  * Days on Production
  * Normalized Oil Rate
* Missing value audit
* Parquet export pipeline

---

## In Progress

###  Phase 2 — Exploratory Data Analysis

Planned analyses:

* Production decline curves
* Well-by-well performance comparison
* GOR trends
* Water cut evolution
* Correlation analysis
* Missing value investigation

---

## Upcoming

### ⏳ Phase 3 — Forecasting Models

#### Arps Decline Curve Analysis

* Exponential decline
* Hyperbolic decline
* Forecast generation
* Parameter estimation

#### XGBoost Time-Series Forecasting

* Lag features
* Rolling averages
* Cumulative production features
* Walk-forward validation

---

## Future Work

* SHAP explainability analysis
* Model error comparison
* Confidence intervals
* Interactive dashboard
* Final production forecast visualization

---

## Project Structure

```text
well-production-forecast/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_arps_baseline.ipynb
│   ├── 03_xgboost_model.ipynb
│   └── 04_error_shap.ipynb
│
├── src/
│   ├── data_loader.py
│   ├── arps.py
│   └── features.py
│
├── outputs/
│   ├── figures/
│   └── models/
│
└── README.md
```

---

## Tech Stack

* Python
* Pandas
* NumPy
* Matplotlib
* Scikit-Learn
* XGBoost
* SHAP

---

## Status

Current Stage: **Data Engineering & EDA**

This repository is actively being developed. Additional notebooks, forecasting models, visualizations, and performance evaluations will be added as the project progresses.
