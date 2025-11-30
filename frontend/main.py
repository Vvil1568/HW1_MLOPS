import streamlit as st
import requests
import json
import pandas as pd

API_URL = "http://backend-service:8000/api/v1"

st.set_page_config(page_title="MLOps Dashboard", layout="wide")
st.title("🎛️ MLOps Homework Dashboard")

# Tabs
tab1, tab2, tab3 = st.tabs(["📂 Datasets (DVC)", "🧠 Training (ClearML)", "🔮 Inference"])

# --- Tab 1: Datasets ---
with tab1:
    st.header("Manage Datasets")

    # List
    if st.button("Refresh Datasets"):
        try:
            res = requests.get(f"{API_URL}/datasets/list")
            if res.status_code == 200:
                datasets = res.json().get("datasets", [])
                st.session_state['datasets'] = datasets
                st.success("List updated")
        except Exception as e:
            st.error(f"Connection error: {e}")

    st.write("Available Datasets:", st.session_state.get('datasets', []))

    # Upload
    uploaded_file = st.file_uploader("Upload CSV/JSON", type=['csv', 'json'])
    if uploaded_file and st.button("Upload to DVC"):
        files = {'file': uploaded_file}
        res = requests.post(f"{API_URL}/datasets/upload", files=files)
        if res.status_code == 200:
            st.success(f"Uploaded: {res.json()}")
        else:
            st.error("Upload failed")

# --- Tab 2: Training ---
with tab2:
    st.header("Train Model")

    # Fetch Model Classes
    res_models = requests.get(f"{API_URL}/models/list")
    model_options = []
    if res_models.status_code == 200:
        model_options = res_models.json().get("models", [])

    selected_model = st.selectbox("Select Model Class", model_options)

    # Select Dataset
    dataset_options = st.session_state.get('datasets', [])
    selected_dataset = st.selectbox("Select Dataset", dataset_options)

    # Hyperparams
    default_params = '{"n_estimators": 100, "max_depth": 5}' if selected_model == "RandomForest" else '{"C": 1.0}'
    hyperparams_str = st.text_area("Hyperparameters (JSON)", value=default_params)

    if st.button("Start Training"):
        try:
            params = json.loads(hyperparams_str)
            payload = {
                "model_type": selected_model,
                "dataset_name": selected_dataset,
                "hyperparameters": params
            }
            res = requests.post(f"{API_URL}/train", json=payload)
            if res.status_code == 200:
                st.success(f"Training started! Task ID: {res.json().get('task_id')}")
            else:
                st.error(f"Error: {res.text}")
        except json.JSONDecodeError:
            st.error("Invalid JSON")

# --- Tab 3: Inference ---
with tab3:
    st.header("Predict")
    model_id = st.text_input("ClearML Model Task ID")
    features_input = st.text_area("Features (comma separated, e.g. 1.0, 2.5, 3.1)")

    if st.button("Get Prediction"):
        try:
            features = [float(x.strip()) for x in features_input.split(",")]
            payload = {
                "model_id": model_id,
                "features": [features]  # Batch of 1
            }
            res = requests.post(f"{API_URL}/predict", json=payload)
            if res.status_code == 200:
                st.balloons()
                st.metric("Result", str(res.json().get("predictions")[0]))
            else:
                st.error(res.text)
        except Exception as e:
            st.error(f"Error: {e}")