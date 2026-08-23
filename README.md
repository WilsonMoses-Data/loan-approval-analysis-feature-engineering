# Loan Approval Prediction: Advanced Data Exploration and Feature Engineering

> **AnalystLab Africa Data Science Internship | Week 3 Project**  
> **Author:** Wilson Moses  
> **Focus:** Advanced exploratory analysis, statistical inference, feature engineering, responsible feature selection, and machine-learning preparation.

## Project Overview

This project investigates historical loan applications to understand the factors associated with loan approval and prepare a reliable dataset for predictive modelling.

Building on the cleaning and preprocessing completed in Week 2, the Week 3 analysis moves beyond basic summaries to examine data quality, applicant characteristics, approval patterns, statistical relationships, engineered financial indicators, and leakage-safe machine-learning preparation.

The result is a complete analytical workflow that transforms a cleaned loan application dataset into documented, interpretable, and model-ready project deliverables.

## Business Problem

Lending institutions must assess loan applications consistently while balancing access to credit, operational efficiency, and financial risk.

The central business question is:

> **Which applicant, household, financial, and credit-related characteristics are associated with historical loan approval decisions, and how can those characteristics be prepared responsibly for predictive modelling?**

The target variable is `loan_status`:

- `Y`: loan application approved.
- `N`: loan application not approved.

For numerical analysis and modelling, the outcome is also represented as `approved`:

- `1`: approved.
- `0`: not approved.

## Project Objectives

1. Validate the quality, consistency, and business plausibility of the cleaned dataset.
2. Investigate distributions, outliers, approval rates, and relationships between applicant characteristics.
3. Test whether observed patterns are statistically significant.
4. Create interpretable features describing household composition, credit status, income, and repayment burden.
5. Select informative modelling features while controlling redundancy and fairness risks.
6. Prepare reproducible training and testing datasets without data leakage.
7. Translate technical findings into practical business recommendations.

## Dataset Summary

| Measure | Result |
| --- | ---: |
| Loan applications analysed | 614 |
| Original cleaned variables | 14 |
| Approved applications | 422 |
| Rejected applications | 192 |
| Overall approval rate | 68.73% |
| Engineered features created | 12 |
| Final analytical dataset columns | 26 |
| Selected source modelling features | 12 |
| Encoded modelling features | 13 |
| Training observations | 491 |
| Testing observations | 123 |

The original cleaned dataset includes:

```text
gender
married
dependents
education
self_employed
applicant_income
coapplicant_income
loan_amount
loan_amount_term
credit_history
property_area
loan_status
total_income
loan_income_ratio
```

## Tools and Technologies

- **Python:** primary programming language.
- **Jupyter Notebook:** interactive analysis and documentation.
- **pandas:** data manipulation, validation, grouping, and dataset exports.
- **NumPy:** numerical operations and feature construction.
- **Matplotlib:** data visualisation.
- **Seaborn:** statistical visualisation and exploratory analysis.
- **SciPy:** hypothesis testing and statistical analysis.
- **scikit-learn:** feature screening, train-test splitting, categorical encoding, and feature scaling.

## Repository Structure

The following structure is recommended when publishing the project to GitHub:

```text
loan-prediction-week3/
├── README.md
├── Advance_Analysis_Loan_Predicition.ipynb
├── data/
│   ├── loan_prediction_cleaned.csv
│   └── loan_prediction_ml_ready.csv
├── week3_outputs/
│   ├── loan_prediction_week3_final_cleaned.csv
│   ├── loan_prediction_week3_ml_ready.csv
│   ├── loan_prediction_week3_train.csv
│   ├── loan_prediction_week3_test.csv
│   └── week3_updated_data_dictionary.csv
└── reports/
    ├── Week3_Business_Insights_Report.pdf
    ├── Week3_Statistical_Analysis_Report.pdf
    └── Week3_Feature_Engineering_Documentation.pdf
```

Editable Word versions of the reports can also be included in the `reports/` directory if required.

## Analytical Workflow

### Part 1: Advanced Data Quality Assessment

The initial assessment verifies that the cleaned dataset is suitable for deeper analysis.

Checks include:

- Dataset dimensions and variable data types.
- Missing values and duplicate records.
- Categorical consistency.
- Negative or invalid numerical values.
- Valid credit-history values.
- Existing engineered-feature calculations.
- Outliers identified using the interquartile range method.
- Target-class distribution and class imbalance.

This stage establishes whether the available records are internally consistent and appropriate for interpretation.

### Part 2: Advanced Exploratory Data Analysis

Exploratory analysis examines how applicant characteristics relate to historical approval outcomes.

The notebook includes:

- Histograms, density plots, and box plots for financial variables.
- Log-transformed income and loan-amount distributions.
- Loan-term distribution analysis.
- Categorical frequency and percentage summaries.
- Approval-rate comparisons across applicant groups.
- Cross-tabulations and row percentages.
- Numerical comparisons between approved and rejected applications.
- Pearson and Spearman correlation analysis.
- Combined analysis of credit history and property area.

### Part 3: Statistical Analysis

Six hypothesis tests evaluate whether observed relationships are supported by statistical evidence.

| Analysis | Statistical method | Result | Interpretation |
| --- | --- | --- | --- |
| Credit history vs. loan approval | Chi-square test | `p < 0.001`; Cramer's V = `0.536` | Strong evidence of an association. |
| Property area vs. loan approval | Chi-square test | `p = 0.002`; Cramer's V = `0.142` | Statistically significant but comparatively weak association. |
| Total income by approval outcome | Mann-Whitney U test | `p = 0.713` | No statistically significant independent difference. |
| Loan amount by approval outcome | Mann-Whitney U test | `p = 0.398` | No statistically significant independent difference. |
| Total income across property areas | Kruskal-Wallis test | `p = 0.140` | No statistically significant difference across the three areas. |
| Total income vs. requested loan amount | Spearman correlation | `rho = 0.688`; `p < 0.001` | Strong positive relationship. |

Financial variables were right-skewed, so nonparametric methods were used where appropriate. Statistical significance was assessed at `alpha = 0.05`.

### Part 4: Feature Engineering

Twelve new features were created to improve interpretability and represent applicant circumstances more meaningfully.

| Engineered feature | Description |
| --- | --- |
| `dependents_numeric` | Converts the dependents category into a numerical representation. |
| `family_size` | Estimates household size using applicant, marital status, and dependents. |
| `family_size_group` | Groups estimated household sizes into interpretable categories. |
| `income_band` | Segments total household income into descriptive ranges. |
| `has_coapplicant_income` | Indicates whether a coapplicant contributes income. |
| `coapplicant_income_share` | Measures the proportion of household income contributed by a coapplicant. |
| `term_years` | Converts the loan repayment period from months to years. |
| `estimated_monthly_principal` | Estimates monthly principal repayment using loan amount and term. |
| `payment_income_ratio` | Approximates repayment burden relative to household income. |
| `credit_risk_category` | Converts credit-history status into a business-readable category. |
| `log_total_income` | Reduces the impact of right-skewed household income. |
| `log_loan_amount` | Reduces the impact of right-skewed requested loan amounts. |

The affordability-related calculations were defined as:

```python
estimated_monthly_principal = (loan_amount * 1000) / loan_amount_term

payment_income_ratio = estimated_monthly_principal / total_income
```

> **Important:** The repayment measure is a proxy, not a complete affordability assessment. Interest rates, existing debt, insurance, and verified monthly expenses are not available in the dataset.

### Part 5: Feature Selection

Feature selection considered statistical evidence, mutual information, interpretability, redundancy, and responsible use.

The final selected source features were:

```python
final_selected_features = [
    "married",
    "dependents_numeric",
    "education",
    "self_employed",
    "property_area",
    "credit_history",
    "log_total_income",
    "log_loan_amount",
    "term_years",
    "has_coapplicant_income",
    "coapplicant_income_share",
    "payment_income_ratio",
]
```

Several variables were retained for reporting but excluded from final modelling because they duplicated information already represented elsewhere. For example:

- `family_size` duplicates information derived from marital status and dependents.
- `credit_risk_category` duplicates `credit_history`.
- `income_band` simplifies income for reporting but discards useful numerical detail.
- `estimated_monthly_principal` is partly represented by the repayment-burden proxy.

`gender` was intentionally excluded from predictive inputs because it can function as a protected characteristic. It remains relevant for fairness monitoring and subgroup evaluation.

### Part 6: Machine-Learning Data Preparation

The final preprocessing workflow was designed to avoid information leakage.

1. Separate the selected predictors from the binary target.
2. Create a stratified 80/20 train-test split using `random_state=42`.
3. Fit preprocessing transformations using the training data only.
4. Apply the fitted transformations to the held-out testing data.
5. Export the final analytical, machine-learning-ready, training, and testing datasets.

The preprocessing pipeline applies:

- `OneHotEncoder(drop="first", handle_unknown="ignore")` to nominal categorical variables.
- `StandardScaler()` to selected continuous variables.
- Passthrough processing to binary and ordinal features.

```python
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                drop="first",
                handle_unknown="ignore",
                sparse_output=False,
            ),
            nominal_features,
        ),
        ("continuous", StandardScaler(), continuous_model_features),
        ("binary_ordinal", "passthrough", passthrough_features),
    ]
)

X_train_transformed = preprocessor.fit_transform(X_train)
X_test_transformed = preprocessor.transform(X_test)
```

The exported machine-learning datasets contain 13 transformed predictors, the binary `approved` target, and a `dataset_split` metadata column.

> **Modelling note:** `dataset_split` identifies whether an observation belongs to the training or testing partition. It is metadata and must not be included as a model input.

### Part 7: Business Insights and Recommendations

The final stage translates the analytical findings into practical recommendations for lending and future model development.

Key recommendations include:

- Prioritise the completeness and reliability of credit-history information.
- Evaluate affordability through combined income, loan amount, and repayment-duration indicators.
- Investigate geographic approval differences before incorporating them into operational decisions.
- Monitor demographic fairness without using protected characteristics as direct predictive inputs.
- Validate future models against held-out data and multiple performance metrics.

## Key Findings

### Credit History Was the Strongest Observed Approval Factor

| Credit-history group | Applications | Approved | Approval rate |
| --- | ---: | ---: | ---: |
| Positive credit history | 525 | 415 | 79.05% |
| No positive credit history | 89 | 7 | 7.87% |

The difference was statistically significant and showed a substantially stronger effect than the other tested categorical variables.

### Approval Rates Also Varied by Property Area

| Property area | Applications | Approved | Approval rate |
| --- | ---: | ---: | ---: |
| Semiurban | 233 | 179 | 76.82% |
| Urban | 202 | 133 | 65.84% |
| Rural | 179 | 110 | 61.45% |

Although this association was statistically significant, its effect size was smaller than the effect associated with credit history.

### Financial Variables Were More Useful in Combination

Total income and loan amount did not independently distinguish approved from rejected applications in the statistical comparisons. However, income and requested loan amount were strongly related, supporting the creation of combined affordability and repayment-burden features.

## Exported Project Deliverables

| Deliverable | Description | Dimensions |
| --- | --- | --- |
| `loan_prediction_week3_final_cleaned.csv` | Human-readable analytical dataset containing original and engineered features. | `614 x 26` |
| `loan_prediction_week3_ml_ready.csv` | Combined encoded and transformed modelling dataset. | `614 x 15` |
| `loan_prediction_week3_train.csv` | Predetermined training partition. | `491 x 15` |
| `loan_prediction_week3_test.csv` | Predetermined testing partition. | `123 x 15` |
| `week3_updated_data_dictionary.csv` | Definitions, data types, and roles for analytical and modelling variables. | `41 x 5` |
| `Week3_Business_Insights_Report.pdf` | Stakeholder-facing business findings and recommendations. | 5 pages |
| `Week3_Statistical_Analysis_Report.pdf` | Detailed hypothesis tests and interpretation. | 6 pages |
| `Week3_Feature_Engineering_Documentation.pdf` | Feature definitions, selection decisions, and preprocessing workflow. | 5 pages |

## How to Run the Project

### 1. Clone or Download the Repository

```bash
git clone <your-repository-url>
cd <your-repository-directory>
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

```bash
# Windows
.venv\Scripts\activate

# macOS or Linux
source .venv/bin/activate
```

### 3. Install the Required Packages

```bash
pip install jupyter numpy pandas matplotlib seaborn scipy scikit-learn
```

### 4. Place the Input Dataset in an Accessible Location

The notebook automatically searches for `loan_prediction_cleaned.csv` in the following locations:

```text
loan_prediction_cleaned.csv
data/loan_prediction_cleaned.csv
../data/loan_prediction_cleaned.csv
upload/loan_prediction_cleaned.csv
```

### 5. Launch Jupyter Notebook

```bash
jupyter notebook
```

Open `Advance_Analysis_Loan_Predicition.ipynb` and run the cells sequentially from top to bottom.

The notebook writes its generated datasets and data dictionary to the `week3_outputs/` directory.

## Limitations and Responsible Interpretation

- The dataset contains 614 applications, so estimates for small applicant groups may be unstable.
- The target captures historical approval decisions, not actual repayment behaviour or default outcomes.
- Historical decisions may reflect institutional bias or inconsistent lending practices.
- Interest rates, existing debt, living expenses, and verified instalment amounts are unavailable.
- Previously imputed values may reduce the natural variability of some features.
- Statistical association does not establish causation.
- Geographic or demographic patterns should be assessed carefully before influencing real lending decisions.

## Next Steps

The next phase of the project will focus on supervised machine-learning model development and evaluation, including:

- Establishing a baseline classifier.
- Comparing logistic regression, decision-tree, and random-forest models.
- Applying stratified cross-validation.
- Evaluating accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrices.
- Reviewing fairness across applicant subgroups.
- Assessing model calibration and classification-threshold trade-offs.

## Skills Demonstrated

- Advanced exploratory data analysis.
- Data-quality validation and outlier assessment.
- Statistical hypothesis testing and effect-size interpretation.
- Feature engineering and affordability-proxy design.
- Feature selection and redundancy assessment.
- Mutual-information analysis.
- Responsible machine learning and fairness awareness.
- Leakage-safe preprocessing and train-test splitting.
- Data visualisation and analytical storytelling.
- Technical reporting and business communication.

## Author

**Wilson Moses**  
Data Science Intern, AnalystLab Africa  
Data Science to AI Engineering Journey

---

*This project forms part of my ongoing journey to develop practical capability in data science, machine learning, and AI engineering through hands-on analytical projects.*
