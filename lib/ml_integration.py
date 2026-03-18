import joblib
import pandas as pd
from types import SimpleNamespace
from pathlib import Path
import pickle

data = pickle.load(open(Path(__file__).parent / "pipeline.pkl", "rb"))

model = data["model"]
scaler = data["scaler"]
feature_names = data["features"]


def _normalize_prediction_to_bool(prediction) -> bool:
    """Safely map model predictions to an eligibility boolean."""
    if isinstance(prediction, (bool, int, float)):
        return int(prediction) == 1

    text = str(prediction).strip().upper()
    if text in {"1", "Y", "YES", "TRUE", "ELIGIBLE", "APPROVED"}:
        return True
    if text in {"0", "N", "NO", "FALSE", "NOT_ELIGIBLE", "REJECTED", "DENIED"}:
        return False
    return False


def _dependents_to_numeric(dep) -> int:
    """Convert dependents input to model-compatible numeric bucket."""
    try:
        value = int(str(dep).strip())
    except (ValueError, TypeError):
        value = 0

    if value <= 0:
        return 0
    if value == 1:
        return 1
    if value == 2:
        return 2
    return 3


def _eligible_class_index(model_obj) -> int:
    """Return the probability index that represents the eligible class."""
    classes = getattr(model_obj, "classes_", None)
    if classes is None:
        return 1

    positive_labels = {"1", "Y", "YES", "TRUE", "ELIGIBLE", "APPROVED"}
    for idx, cls in enumerate(classes):
        if str(cls).strip().upper() in positive_labels:
            return idx

    return 1 if len(classes) > 1 else 0



def call_ml_model(form_data: dict):
    from types import SimpleNamespace
    import pandas as pd
    import numpy as np

    # ----------------------
    # CREATE BASE INPUT
    # ----------------------
    input_dict = dict.fromkeys(feature_names, 0)
    # ----------------------
    # RAW VALUES
    # ----------------------
    applicant_income = form_data["applicantIncome"]
    coapplicant_income = form_data["coapplicantIncome"]
    loan_amount = form_data["loanAmount"]

    # ----------------------
    # FEATURE ENGINEERING (NEW 🔥)
    # ----------------------
    total_income = applicant_income + coapplicant_income

    # Convert LoanAmount to actual (NOT /1000 anymore)
    loan_amount = loan_amount

    # Log transform
    total_income_log = np.log(total_income + 1)
    loan_amount_log = np.log(loan_amount + 1)

    # Ratio
    loan_income_ratio = loan_amount_log / total_income_log if total_income_log != 0 else 0

    # ----------------------
    # NUMERIC FEATURES
    # ----------------------
    input_dict["TotalIncome"] = total_income_log
    input_dict["LoanAmount"] = loan_amount_log
    input_dict["LoanIncomeRatio"] = loan_income_ratio
    input_dict["Loan_Amount_Term"] = form_data["loanAmountTerm"]
    input_dict["Credit_History"] = 1 if form_data["creditHistory"] == "Yes" else 0

    # ----------------------
    # CATEGORICAL (KEEP SAME)
    # ----------------------
    input_dict["Gender"] = 1 if form_data["gender"] == "Male" else 0
    input_dict["Married"] = 1 if form_data["married"] == "Yes" else 0

    # Dependents
    dep = form_data["dependents"]
    input_dict["Dependents"] = _dependents_to_numeric(dep)

    # Education
    input_dict["Education"] = 0 if form_data["education"] == "Graduate" else 1

    # Self Employed
    input_dict["Self_Employed"] = 1 if form_data["self_employed"] == "Yes" else 0

    # Property Area
    area = form_data["propertyArea"]
    if area == "Rural":
        input_dict["Property_Area"] = 0
    elif area == "Semiurban":
        input_dict["Property_Area"] = 1
    else:
        input_dict["Property_Area"] = 2

    

    # ----------------------
    # DATAFRAME
    # ----------------------
    input_df = pd.DataFrame([input_dict])

    # ----------------------
    # 🔥 APPLY SCALER (NEW)
    # ----------------------
    input_scaled = scaler.transform(input_df)

    # ----------------------
    # PREDICTION
    # ----------------------
    prediction = model.predict(input_scaled)[0]
    eligible_idx = _eligible_class_index(model)
    probability = model.predict_proba(input_scaled)[0][eligible_idx]

    score = int(probability * 100)
    eligible = _normalize_prediction_to_bool(prediction)

    return SimpleNamespace(
        eligible=eligible,
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
