import pandas as pd
import numpy as np
import sklearn as sk
import matplotlib.pyplot as plt
from sklearn.calibration import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('loan_approval_dataset.csv')

le = LabelEncoder()

df['no_of_dependents'] = le.fit_transform(df['no_of_dependents'])
df['self_employed'] = le.fit_transform(df['self_employed'])
df['education'] = le.fit_transform(df['education'])
df['cibil_score'] = le.fit_transform(df['cibil_score'])
df['income_annum'] = le.fit_transform(df['income_annum'])
df['loan_amount'] = le.fit_transform(df['loan_amount'])
df['residential_assets_value'] = le.fit_transform(df['residential_assets_value'])
df['commercial_assets_value'] = le.fit_transform(df['commercial_assets_value'])
df['luxury_assets_value'] = le.fit_transform(df['luxury_assets_value'])
df['bank_asset_value'] = le.fit_transform(df['bank_asset_value'])

df['loan_status'] = le.fit_transform(df['loan_status'])

X = df[['education', 'cibil_score', 'income_annum', 'loan_amount', 'no_of_dependents', 'residential_assets_value', 'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value']]
y = df['loan_status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# model = LogisticRegression(random_state=1)
# model = DecisionTreeClassifier(random_state=1)

model = RandomForestClassifier(random_state=1,n_estimators=100,max_depth=5)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)


# y_pred = np.round(y_pred)
print("Predicted values:", y_pred)


accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))