import requests

try:
    params = {
        "education": 1,
        "cibil_score": 650,
        "income_annum": 500000,
        "loan_amount": 1000000,
        "no_of_dependents": 2,
        "residential_assets_value": 2000000,
        "commercial_assets_value": 500000,
        "luxury_assets_value": 300000,
        "bank_asset_value": 400000
    }

    response = requests.get("http://127.0.0.1:8000/get_loan_status", params=params)
    print("Status code:", response.status_code)
    print("Response:", response.text)

except requests.exceptions.ConnectionError:
    print("ERROR: Server is not running!")

except Exception as e:
    print("ERROR:", e)