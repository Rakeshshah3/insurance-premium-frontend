import streamlit as st
import requests

# Backend API URL
API_URL = "https://insurancepremiumpredictor-production.up.railway.app/predict"

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Insurance Premium Category Predictor")
st.markdown("Enter your details below to predict your insurance premium category.")

# ------------------- Input Fields -------------------
age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)

smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Mumbai")

occupation = st.selectbox(
    "Occupation",
    [
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job",
    ],
)

# ------------------- Prediction -------------------
if st.button("🔮 Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation,
    }

    try:
        with st.spinner("🔍 Predicting insurance premium category..."):
            response = requests.post(API_URL, json=input_data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            prediction = result["response"]

            category = prediction["predicted_category"]
            confidence = prediction["confidence"]
            probabilities = prediction["class_probabilities"]

            # -------- Main Result --------
            st.success(f"🎯 **Predicted Insurance Premium Category: {category}**")

            st.metric(
                label="Model Confidence (Predicted Category)",
                value=f"{confidence * 100:.1f}%"
            )

            st.markdown("---")

            # -------- Probability Breakdown --------
            st.subheader("📊 Confidence Percentage by Category")

            for cls, prob in probabilities.items():
                col1, col2 = st.columns([2, 5])
                with col1:
                    st.write(f"**{cls}**")
                with col2:
                    st.progress(prob)
                    st.caption(f"{prob * 100:.1f}%")

            st.info(
                f"ℹ️ The model is most confident that the premium category is **{category}**."
            )

        else:
            st.error(f"❌ API Error: {response.status_code}")
            st.write(response.text)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the backend API. Please try again later.")
    except Exception as e:
        st.error("❌ An unexpected error occurred.")
        st.write(e)