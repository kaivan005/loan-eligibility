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
        score=score
    )
