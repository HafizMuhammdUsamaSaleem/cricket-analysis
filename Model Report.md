# Report Cricket Match Prediction
## 1. Introduction

The goal of this project was to build a machine learning model that predicts the outcome of a T20 cricket chase given the current match situation.
The prediction system was further wrapped in a FastAPI service, extended with LLM-based explanations.

**The challenge involves binary classification:**

1 == The chasing team wins.

0 == The chasing team loses.

## 2. Dataset & Preprocessing

The dataset contained ball-by-ball records of T20 chases with the following columns:

total_runs – Runs scored so far by the chasing team.

wickets – Number of wickets fallen.

target – Runs required to win.

balls_left – Balls remaining in the innings.

won – Target variable (1 = win, 0 = loss).

**Preprocessing Steps**

Null Values: Rows with missing or NaN values were dropped, as they were deemed garbage entries with no meaningful recovery.

Logical Validation:

Removed rows with impossible values (e.g., negative balls, wickets > 10, runs > target).

Kept only realistic cricket scenarios.

Type Conversion: Converted all numeric features into integers (except run rate, which was float).

This ensured a clean dataset suitable for analysis and modeling.

## 3. Exploratory Data Analysis (EDA)
- Key Insights

Matches were relatively balanced between wins and losses, showing no major class imbalance.

Wickets vs. Outcome: Teams losing fewer wickets had higher win probabilities.

Pressure Zones: Situations with low balls left and high runs needed showed much lower chances of winning.

Target Size: Higher targets correlated with fewer wins.

- Visualizations

Target Distribution: Showed a good balance between wins and losses.

Scatter: Runs Needed vs Balls Left (colored by outcome): Clearly showed winning vs losing “pressure zones.”

Heatmap of Win Probability: Grouped runs_needed and balls_left into bins to visualize strategy zones.

Correlation Heatmap: Identified strong negative correlation between wickets lost and winning probability.

## 4. Feature Engineering

Although the dataset was simple, we introduced cricket-relevant features for better interpretability:

runs_needed = target - total_runs.

required_run_rate = runs_needed / balls_left (float, 2 decimals).

wickets_ratio = wickets / 10 (normalized).

These features didn’t drastically improve accuracy but provided cricket-specific insights and made explanations easier to interpret.

## 5. Model Development
Algorithms Tested

1. Logistic Regression

Simple, interpretable linear baseline.

Achieved ~75% accuracy.

Useful for benchmarking.

2. Random Forest Classifier

Captures nonlinear relationships.

Achieved ~95% accuracy.

Chosen for deployment due to strong balance of accuracy, interpretability, and robustness.

Why Not XGBoost or Complex Ensembles?

Given the dataset simplicity (few structured features), deeper ensembles risked overfitting without meaningful performance gain.

## 6. Evaluation
1. Metrics

Accuracy: Primary metric (classification).

Confusion Matrix: Checked balance of predictions.

Cross-Validation: Performed to ensure results were consistent.

2. Results

Logistic Regression: ~75% accuracy.

Random Forest: ~95% accuracy.

The Random Forest model provided a clear boost in predictive power and was selected as the production model (random_forest_v1.pkl).

## 7. API Deployment

The trained model was deployed via FastAPI, with three endpoints:

POST /predict: Accepts a CSV, filters rows (balls_left < 60, target > 120) runs predictions returns CSV + metadata.

POST /explain/{prediction_id}: Uses Gemini LLM to provide human-readable cricket explanations (Win/Loss reasoning).

GET /health: Returns service + model version.

The API includes:

- Input validation.

- Null handling (dropped rows logged).

- Error messages for malformed CSVs.

- Logging for monitoring/debugging.

## 8. Limitations

Identical starting states issue:

Example: Two matches start with 0 wickets, 120 balls left, target 160.

Some end in wins, others in losses.

This isn’t ambiguity but reflects real-world cricket variability (team quality, player form, pressure).

Feature engineering impact: While interpretability improved, accuracy gains were minimal due to dataset constraints.

## 9. Future Improvements

Incorporate contextual features:pitch type, batting team strength, winning ratio chasing vs defending.

## 10. Conclusion

This project successfully built an end-to-end machine learning pipeline for T20 chase prediction, supported by:

Rigorous EDA and feature engineering.

Model comparison (Logistic Regression vs Random Forest).

A production-ready API with prediction and LLM-based explanation endpoints.

The Random Forest model (95% accuracy) was chosen for deployment. While feature engineering offered limited accuracy gain, it enriched interpretability and aligns well with cricket logic.
