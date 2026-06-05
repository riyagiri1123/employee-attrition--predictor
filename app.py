import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

st.title("Employee Attrition Predictor")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open('model.pkl', 'rb'))

# ---------------- LOAD DATA ----------------
data = pd.read_csv("project data.csv")

# ---------------- PREPROCESSING (SAME AS TRAINING) ----------------
data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1})
data['OverTime'] = data['OverTime'].map({'No': 0, 'Yes': 1})

encoding_cols = ['BusinessTravel', 'Department', 'EducationField', 'JobRole', 'MaritalStatus']
label_encoders = {}

for column in encoding_cols:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])

# Features
X = data.drop(['Attrition', 'Over18'], axis=1)

# ---------------- UI ----------------
st.subheader("Enter Employee Details")

age = st.number_input("Age", min_value=18, max_value=60)
monthly_income = st.number_input("Monthly Income")
years_company = st.number_input("Years At Company")
job_level = st.number_input("Job Level")

gender = st.selectbox("Gender", ["Male", "Female"])
overtime = st.selectbox("OverTime", ["No", "Yes"])
JobSatisfaction	=st.number_input("JobSatisfaction")

# ---------------- PREDICTION ----------------
if st.button("Predict"):
    try:
        # Create full input with default values
        input_data = X.iloc[0].copy()

        # Replace important fields
        input_data['Age'] = age
        input_data['MonthlyIncome'] = monthly_income
        input_data['YearsAtCompany'] = years_company
        input_data['JobLevel'] = job_level
        input_data['JobSatisfaction	']= JobSatisfaction	

        input_data['Gender'] = 0 if gender == "Male" else 1
        input_data['OverTime'] = 0 if overtime == "No" else 1

        # Convert to DataFrame
        final_input = pd.DataFrame([input_data])

        # Prediction
        result = model.predict(final_input)

        if result[0] == 1:
            st.error("⚠️ Employee is likely to leave")
        else:
            st.success("✅ Employee will stay")

    except Exception as e:
        st.error(f"Error: {e}")