import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Advanced BMI Calculator",
    page_icon="🏋️",
    layout="wide"
)

# Main header
st.title("🏋️ Advanced BMI Calculator by ZeeJay🙅‍♂️")
st.markdown("Track your Body Mass Index and get personalized health recommendations")

# Initialize session state
state = st.session_state
if 'history' not in state:
    state.history = []

# Unit conversion
units = st.radio("Select units:", ("Metric", "Imperial"), horizontal=True)

if units == "Metric":
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=52.0, step=0.5)
    height = st.number_input("Height (m)", min_value=1.0, max_value=3.0, value=1.54, step=0.01)
else:
    col1, col2 = st.columns(2)
    with col1:
        weight_lb = st.number_input("Weight (lbs)", min_value=66.0, max_value=440.0, value=114.64, step=1.0)
    with col2:
        height_ft = st.number_input("Height (feet)", min_value=3.0, max_value=9.0, value=5.0, step=0.1)
        height_in = st.number_input("Height (inches)", min_value=0.0, max_value=11.0, value=0.5, step=0.1)
    
    weight = weight_lb * 0.453592
    height = (height_ft * 0.3048) + (height_in * 0.0254)

# Calculate BMI
bmi = weight / (height ** 2)
bmi_rounded = round(bmi, 1)

# Determine category
categories = [
    (13, "Severe Underweight", "danger"),
    (18.5, "Underweight", "warning"),
    (25, "Normal", "success"),
    (30, "Overweight", "warning"),
    (43, "Obesity", "danger"),
    (float('inf'), "Severe Obesity", "danger")
]

for threshold, label, _ in categories:
    if bmi_rounded <= threshold:
        level = label
        color = _
        break

# Plotly gauge
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = bmi_rounded,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "BMI", 'font': {'size': 24}},
    gauge = {
        'axis': {'range': [13, 43], 'tickwidth': 2, 'tickcolor': "black"},
        'bar': {'color': "black"},
        'bgcolor': "white",
        'steps': [
            {'range': [13, 18.5], 'color': "#ff4444"},
            {'range': [18.5, 25], 'color': "#88c241"},
            {'range': [25, 30], 'color': "#ffd700"},
            {'range': [30, 43], 'color': "#ff6b6b"}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 43}}))

fig.update_layout(paper_bgcolor="white", font={'color': "black", 'family': "Arial"})

# Layout
st.subheader(f"Your BMI: {bmi_rounded} - {level}")
col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.markdown(f"""
    <div style="border-radius: 10px; padding: 20px; background-color: #f0f2f6; height: 300px;">
        <h4 style="color: #2c3e50;">Health Implications</h4>
        <ul style="list-style-type: none; padding-left: 0;">
            <li> {'⚠️ Consult a healthcare provider immediately' if 'Severe' in level else ''}</li>
            <li> {'🔹 Normal: Healthy weight range' if level == 'Normal' else ''}</li>
            <li> {'⚠️ Overweight: Increased health risks' if level == 'Overweight' else ''}</li>
            <li> {'🚨 Obesity: Higher risk of chronic diseases' if level == 'Obesity' else ''}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# History tracking
if st.button("Save to history 📥"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "Date": timestamp,
        "Weight (kg)": round(weight, 1),
        "Height (m)": round(height, 2),
        "BMI": bmi_rounded,
        "Category": level
    }
    state.history.append(entry)

if state.history:
    st.subheader("Tracking History")
    history_df = pd.DataFrame(state.history)
    st.dataframe(history_df.style.apply(lambda _: ['background-color: #fff; color: black' for _ in range(len(history_df))]))