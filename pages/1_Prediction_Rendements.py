import streamlit as st
from models.predict import predict_yield

st.title("Prédiction Détaillée des Rendements")

region = st.selectbox("Choisis une région", ["Thiès", "Fatick", "Kaolack", "Saint-Louis"])
crop = st.selectbox("Choisis une culture", ["Arachide", "Mil", "Maïs", "Riz"])

if st.button("Prédire"):
    pred = predict_yield(region, crop, 650, 27.5, 0.65)
    st.metric(label="Rendement estimé", value=f"{pred:.2f} t/ha")