import streamlit as st
import pandas as pd
import requests

from utils.data import load_data

API_URL = "http://127.0.0.1:8000/patients/"

st.header('Rechercher des patients')


# Filtres 
gender = st.selectbox("Genre", options=['', 'Male', 'Female'])
# --- Slider simple pour sélectionner un âge max (de 0 à n)
# Penser à modifier les paramètres de age_max > 100 !!!
# age_max = st.slider('Âge max.', min_value=0, max_value=100, step=1)
# --- Slider de sélection de tranche d'âge, modification des paramètres
age_max = st.select_slider('Âge', options=list(range(0,100)), value=(30,50))
stroke = st.selectbox('Historique AVC', options=['', '0', '1'])

# Paramètrage API
params = {}
if gender:
    params['gender'] = gender
if age_max:
    params['max_age'] = age_max
if stroke:
    params['stroke'] = int(stroke)

if st.button('Rechercher'):

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        patients = response.json()

        if patients:
            st.success(f"{len(patients)} patient(s) trouvé(s)")
            st.dataframe(pd.DataFrame(patients))
        else:
            st.warning("Aucun patient trouvé avec ces critères.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'appel à l'API : {e}")
