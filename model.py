import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from fastapi import FastAPI

app = FastAPI()

df = pd.read_csv('loan_approval_dataset.csv')
df.columns = df.columns.str.strip()

le = LabelEncoder()
df['education'] = le.fit_transform(df['education'])
df['self_employed'] = le.fit_transform(df['self_employed'])
df['loan_status'] = le.fit_transform(df['loan_status'])

FEATURES = [
    'education', 'cibil_score', 'income_annum', 'loan_amount',
    'no_of_dependents', 'residential_assets_value',
    'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value'
]

X = df[FEATURES]
y = df['loan_status']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

model = RandomForestClassifier(random_state=1, n_estimators=100, max_depth=5)
model.fit(X_train_scaled, y_train)


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
    return {"Predicted_Loan_Status": label}

''' to measure accuracy of the model

y_pred = np.round(y_pred)
print("Predicted values:", y_pred)


accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred)) '''