import streamlit as st
import pandas as pd
import numpy as np
import requests

API_URL = "http://127.0.0.1:8000/patients/"

st.title('Stroke Data App')

df = pd.read_csv('df_final_test.csv')
df.drop(columns=['Unnamed: 0'], inplace=True)

tab_home, tab_data, tab_vis, tab_stats = st.tabs(['Accueil', 'Données', 'Visualisations', 'Statistiques'])

with tab_home:
    
    st.markdown(''' **Bienvenue sur Stroke Data App !** ''')
    st.markdown(''' Stroke Data App vous permet de consulter les données anonymisées de patients ayant consultés pour des problèmes cardiaques''')
    st.markdown(''' Vous pouvez interroger notre base de données selon des critères que vous définissez, visualiser simplements les données et consulter les statistiques globales''')



with tab_data:
    st.header('Rechercher des patients')


    # Filtres 
    gender = st.selectbox("Genre", options=['', 'Male', 'Female'])
    age_max = st.slider('Âge max.', min_value=0, max_value=100, step=1)
    stroke = st.selectbox('Historique AVC', options=['', '0', '1'])

    # Paramètrage API
    params = {}
    if gender:
        params['gender'] = gender
    if age_max < 100:
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


with tab_vis:
    st.title('Visualisation des données')
    with st.container(border=True):
        df_bmi = df.groupby(['gender', 'age'])['bmi'].mean().reset_index()
        st.write('IMC moyen selon l\'âge')
        st.bar_chart(data=df_bmi,
                    x='age',
                    y='bmi',
                    x_label='age',
                    y_label='bmi')
    

with tab_stats:
    st.header('**Statistiques**')


    

