# main.py
import pickle
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# Loads in milliseconds
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

FEATURES = [
    'education', 'cibil_score', 'income_annum', 'loan_amount',
    'no_of_dependents', 'residential_assets_value',
    'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value'
]

@app.get("/get_loan_status")
def get_loan_status(
    education: int,
    cibil_score: int,
    income_annum: int,
    loan_amount: int,
    no_of_dependents: int,
    residential_assets_value: int,
    commercial_assets_value: int,
    luxury_assets_value: int,
    bank_asset_value: int
):
    input_df = pd.DataFrame([[
        education, cibil_score, income_annum, loan_amount,
        no_of_dependents, residential_assets_value,
        commercial_assets_value, luxury_assets_value, bank_asset_value
    ]], columns=FEATURES)

    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)

    label = "Approved" if prediction[0] == 1 else "Rejected"
    return {"Predicted Loan Status": label}