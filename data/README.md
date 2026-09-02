# Data documentation

## Source input

`raw/loan_prediction_cleaned.csv` contains the 614-row cleaned dataset produced during the preceding loan-data-preparation phase. It is treated as the unchanged upstream input for this repository. It contains 14 analytical columns, zero missing values and zero exact duplicate rows.

The original learning dataset is the [Loan Prediction Problem Dataset on Kaggle](https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset). The dataset remains subject to its original source terms.

## Processed outputs

| File | Purpose |
|---|---|
| `loan_prediction_week3_final_cleaned.csv` | Human-readable dataset containing the original cleaned variables and 12 engineered features |
| `loan_prediction_week3_ml_ready.csv` | Combined encoded and transformed dataset with its predetermined train/test split recorded |
| `loan_prediction_week3_train.csv` | Training partition containing 491 applications |
| `loan_prediction_week3_test.csv` | Held-out testing partition containing 123 applications |
| `week3_updated_data_dictionary.csv` | Definitions, roles and data types for the analytical and model-ready fields |

The `dataset_split` field is metadata and must not be used as a model predictor. The target is `approved`, where `1` represents a historically approved application and `0` represents a historically rejected application.

## Responsible use

These files support an educational portfolio project. Historical approval is not the same as creditworthiness, repayment performance or default risk. The data must not be used to approve, reject or rank real applicants.

