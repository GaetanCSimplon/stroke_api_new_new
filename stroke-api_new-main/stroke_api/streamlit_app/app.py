import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px

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

    # ---------------------------
    # IMC moyen selon l'âge et le genre
    st.markdown("### IMC moyen selon l'âge et le genre")
    
    # Sélection du genre
    selected_display_gender = st.selectbox("Choisissez un genre :", ["Homme", "Femme"])
    
    gender_display = {'Homme': 'Male', 'Femme': 'Female'}
    selected_gender = gender_display[selected_display_gender]

    filtered_df = df[df['gender'] == selected_gender]
    df_bmi = filtered_df.groupby('age')['bmi'].mean().reset_index()

    fig_bmi = px.line(df_bmi, x='age', y='bmi',
                      title=f"IMC moyen par âge pour le genre : {selected_display_gender}",
                      labels={'age': 'Âge', 'bmi': 'IMC moyen'},
                      template='plotly_white')
    
    # Centrer le graphique IMC
    with st.container():
        st.plotly_chart(fig_bmi, use_container_width=True)

    # ---------------------------
    # Glucose moyen selon l'âge et le genre
    st.markdown("### Glucose moyen selon l'âge et le genre")

    # Sélecteur de genre
    genre_choisi = st.selectbox("Choisissez un genre :", ["Tous", "Male", "Female"])

    # Filtrer selon la sélection
    if genre_choisi == "Tous":
        df_filtre = df.copy()
    else:
        df_filtre = df[df['gender'] == genre_choisi]

    df_glucose_gender = df_filtre.groupby(['age', 'gender'])['avg_glucose_level'].mean().reset_index()

    fig_glucose = px.line(
        df_glucose_gender,
        x='age',
        y='avg_glucose_level',
        color='gender' if genre_choisi == "Tous" else None,
        labels={
            'avg_glucose_level': 'Glucose moyen',
            'age': 'Âge',
            'gender': 'Genre'
        },
        title="Glucose moyen selon l'âge et le genre"
    )
    
    # Centrer le graphique Glucose
    with st.container():
        st.plotly_chart(fig_glucose, use_container_width=True)

    # ---------------------------
    # Taux d'AVC selon la catégorie d'âge
    with st.container():
        df_avc_by_age = df.groupby('age_category', as_index=False)['stroke'].mean()
        st.subheader('Taux d\'AVC selon la catégorie d\'âge')
        fig_age = px.bar(data_frame=df_avc_by_age,
                         x='age_category',
                         y='stroke',
                         labels={'stroke': 'Taux d\'AVC', 'age_category': 'Catégorie d\'âge'},
                         template='plotly_white')
        st.plotly_chart(fig_age, use_container_width=True)

    # ---------------------------
    # Taux d'AVC selon le genre
    with st.container():
        df_avc_by_gender = df.groupby('gender', as_index=False)['stroke'].mean()
        st.subheader('Taux d\'AVC selon le genre')
        fig_gender = px.bar(data_frame=df_avc_by_gender,
                            x='gender',
                            y='stroke',
                            labels={'stroke': 'Taux d\'AVC', 'gender': 'Genre'},
                            template='plotly_white')
        st.plotly_chart(fig_gender, use_container_width=True)
    
from stroke_api.filters import filter_stats
with tab_stats:
    st.header('**Statistiques**')
    st.subheader(" Statistiques Globales")
    genre = st.selectbox("Choisir le genre :", ["Tous", "Homme", "Femme"])
    max_age = st.slider("Âge maximal :", 0, 100, 100)
    max_bmi = st.slider("IMC maximal :", 10.0, 60.0, 60.0)

    genre_map = {'Homme': 'Male', 'Femme': 'Female'}
    genre_filtered = genre_map[genre] if genre != "Tous" else None

    stats = filter_stats(df, gender=genre_filtered, max_age=max_age, max_bmi=max_bmi)

    st.markdown(f"""
    - **Nombre total de patients** : {stats['total_patients']}
    - **Âge moyen** : {stats['avg_age']}
    - **IMC moyen** : {stats['avg_bmi']}
    - **Taux d'AVC** : {stats['stroke_rate'] * 100:.2f}%
    - **Répartition hommes/femmes** : {stats['gender_distribution']}
    """)

    

