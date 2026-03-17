import joblib
import pandas as pd
from types import SimpleNamespace
from pathlib import Path

# Load model once (not on every request)
MODEL_PATH = Path(__file__).parent / "logistic_regression_model.pkl"
model = joblib.load(MODEL_PATH)


def call_ml_model(form_data: dict):
    """
    Takes form_data from Streamlit page
    Returns: object with .eligible and .score
    """

    # Create base dictionary with all required features = 0
    input_dict = dict.fromkeys(model.feature_names_in_, 0)

    # ----------------------
    # NUMERIC FEATURES
    # ----------------------

    # IMPORTANT:
    # Your model was trained with LoanAmount in thousands.
    # So divide by 1000.
    input_dict["ApplicantIncome"] = form_data["applicantIncome"]
    input_dict["CoapplicantIncome"] = form_data["coapplicantIncome"]
    input_dict["LoanAmount"] = form_data["loanAmount"] / 1000
    input_dict["Loan_Amount_Term"] = form_data["loanAmountTerm"]
    input_dict["Credit_History"] = 1 if form_data["creditHistory"] == "Yes" else 0

    # ----------------------
    # CATEGORICAL ENCODING
    # ----------------------

    # Gender
    if form_data["gender"] == "Male":
        input_dict["Gender_Male"] = 1

    # Married
    if form_data["married"] == "Yes":
        input_dict["Married_Yes"] = 1

    # Dependents
    dep = str(form_data["dependents"])
    if dep == "1":
        input_dict["Dependents_1"] = 1
    elif dep == "2":
        input_dict["Dependents_2"] = 1
    elif dep == "3":
        input_dict["Dependents_3+"] = 1

    # Education
    if form_data["education"] == "Below Graduate":
        input_dict["Education_Not Graduate"] = 1

    # Self Employed
    if form_data["self_employed"] == "Yes":
        input_dict["Self_Employed_Yes"] = 1

    # Property Area
    if form_data["propertyArea"] == "Semiurban":
        input_dict["Property_Area_Semiurban"] = 1
    elif form_data["propertyArea"] == "Urban":
        input_dict["Property_Area_Urban"] = 1
    # Rural = both 0

    # ----------------------
    # CONVERT TO DATAFRAME
    # ----------------------

    input_df = pd.DataFrame([input_dict])

    # ----------------------
    # PREDICTION
    # ----------------------

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    # Convert probability to score /100
    score = int(probability * 100)

    return SimpleNamespace(
        eligible=bool(prediction),
        score=score,
    )


def get_rejection_reasons(form_data: dict) -> list[str]:
    """Return human-readable rejection reasons derived from the form inputs."""
    reasons = []

    credit_history = form_data.get("creditHistory", "No")
    if credit_history == "No":
        reasons.append(
            "No credit history — lenders require a proven repayment track record."
        )

    applicant_income = float(form_data.get("applicantIncome", 0) or 0)
    coapplicant_income = float(form_data.get("coapplicantIncome", 0) or 0)
    total_income = applicant_income + coapplicant_income
    loan_amount = float(form_data.get("loanAmount", 0) or 0)

    if total_income > 0:
        loan_to_income = loan_amount / total_income
        if loan_to_income > 5:
            reasons.append(
                f"Loan-to-income ratio is too high ({loan_to_income:.1f}x) — "
                "recommended under 5× annual income."
            )
    else:
        reasons.append("No income information provided — income is required for assessment.")

    if total_income < 120_000:
        reasons.append(
            "Total annual income is below the minimum threshold for the requested loan amount."
        )

    if form_data.get("education") == "Below Graduate" and total_income < 200_000:
        reasons.append(
            "Below-graduate education combined with lower income reduces approval likelihood."
        )

    try:
        term = int(form_data.get("loanAmountTerm", 360) or 360)
        if term < 60:
            reasons.append(
                "Short loan term increases monthly obligations beyond acceptable limits."
            )
    except (ValueError, TypeError):
        pass

    if not reasons:
        reasons.append(
            "Overall financial profile does not meet the minimum eligibility criteria at this time."
        )

    return reasons
