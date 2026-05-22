import streamlit as st
import pandas as pd
import joblib

# ---------------- LOAD FILES ----------------
model = joblib.load("churn_model.pkl")
scaler = joblib.load("scaler.pkl")
columns = joblib.load("columns.pkl")  # Training column order

st.set_page_config(page_title="Bank Churn Predictor", layout="centered")
st.title("🏦 Bank Customer Churn Prediction")
st.write("Enter customer details to predict churn risk.")

# ---------------- USER INPUT ----------------
CreditScore = st.number_input("Credit Score", 300, 900, 600)
Age = st.number_input("Age", 18, 100, 40)
Tenure = st.number_input("Tenure (Years with Bank)", 0, 20, 3)
Balance = st.number_input("Account Balance", 0.0, 300000.0, 50000.0)
NumOfProducts = st.number_input("Number of Bank Products", 1, 4, 1)
HasCrCard = st.selectbox("Has Credit Card?", [1, 0])
IsActiveMember = st.selectbox("Is Active Member?", [1, 0])
EstimatedSalary = st.number_input("Estimated Salary", 0.0, 300000.0, 60000.0)
Complain = st.selectbox("Customer Complained?", [0, 1])
Satisfaction_Score = st.slider("Satisfaction Score", 1, 5, 3)
Point_Earned = st.number_input("Reward Points Earned", 0, 1000, 300)

Geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
Gender = st.selectbox("Gender", ["Male", "Female"])
Card_Type = st.selectbox("Card Type", ["GOLD", "PLATINUM", "SILVER"])

# ---------------- PREDICTION ----------------
if st.button("🔍 Predict Churn Risk"):

    # Create empty dataframe with EXACT training columns
    input_data = pd.DataFrame(0, index=[0], columns=columns)

    # Fill numeric values
    input_data["CreditScore"] = CreditScore
    input_data["Age"] = Age
    input_data["Tenure"] = Tenure
    input_data["Balance"] = Balance
    input_data["NumOfProducts"] = NumOfProducts
    input_data["HasCrCard"] = HasCrCard
    input_data["IsActiveMember"] = IsActiveMember
    input_data["EstimatedSalary"] = EstimatedSalary
    input_data["Complain"] = Complain
    input_data["Satisfaction_Score"] = Satisfaction_Score
    input_data["Point_Earned"] = Point_Earned

    # One-hot encoding (only if column exists in model)
    if "Geography_Germany" in columns:
        input_data["Geography_Germany"] = 1 if Geography == "Germany" else 0
    if "Geography_Spain" in columns:
        input_data["Geography_Spain"] = 1 if Geography == "Spain" else 0

    if "Gender_Male" in columns:
        input_data["Gender_Male"] = 1 if Gender == "Male" else 0

    if "Card_Type_GOLD" in columns:
        input_data["Card_Type_GOLD"] = 1 if Card_Type == "GOLD" else 0
    if "Card_Type_PLATINUM" in columns:
        input_data["Card_Type_PLATINUM"] = 1 if Card_Type == "PLATINUM" else 0
    if "Card_Type_SILVER" in columns:
        input_data["Card_Type_SILVER"] = 1 if Card_Type == "SILVER" else 0

    # Ensure correct column order
    input_data = input_data[columns]

    # Scale input
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    # Output
    st.subheader("Prediction Result")

    if prediction == 1:
        st.error(f"⚠️ Customer is likely to CHURN\n\nProbability: {probability:.2%}")
    else:
        st.success(f"✅ Customer is likely to STAY\n\nProbability of churn: {probability:.2%}")

    st.progress(float(probability))
