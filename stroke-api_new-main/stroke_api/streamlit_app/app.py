import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration générale
st.set_page_config(page_title="Stroke Data App", layout="wide")
st.title(' Stroke Data App')

API_URL = "http://127.0.0.1:8000/docs"

# Charger le CSS externe
with open("streamlit_app/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Tabs
tab_home, tab_data, tab_vis, tab_stats = st.tabs(['Accueil', 'Données', 'Visualisations', 'Statistiques'])

# Accueil
with tab_home:
    st.markdown("### **Bienvenue sur Stroke Data App !**")
    st.markdown("Stroke Data App vous permet de consulter les données anonymisées de patients ayant consulté pour des problèmes cardiaques.")
    st.markdown("Vous pouvez interroger notre base de données selon des critères que vous définissez, visualiser simplement les données et consulter les statistiques globales.")

# Données
with tab_data:
    df = pd.read_csv('df_final_test.csv')
    df.drop(columns=['Unnamed: 0'], inplace=True)
    st.markdown("###  Données brutes")
    st.dataframe(df)

# Visualisations
with tab_vis:
    st.markdown("###  IMC moyen selon l'âge et le genre")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_display_gender = st.selectbox("Choisissez un genre :", ["Homme", "Femme"])
    
    with col2:
        gender_display = {'Homme': 'Male', 'Femme': 'Female'}
        selected_gender = gender_display[selected_display_gender]

        filtered_df = df[df['gender'] == selected_gender]
        df_bmi = filtered_df.groupby('age')['bmi'].mean().reset_index()

        fig = px.line(df_bmi, x='age', y='bmi',
                      title=f"IMC moyen par âge pour le genre : {selected_display_gender}",
                      labels={'age': 'Âge', 'bmi': 'IMC moyen'},
                      template='plotly_white')

        st.plotly_chart(fig, use_container_width=True)

# Statistiques (à développer)
    from stroke_api.filters import filter_stats

with tab_stats:
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




#glucose
with tab_vis:
    st.subheader("Glucose moyen selon l'âge et le genre")

    # Sélecteur de genre
    genre_choisi = st.selectbox("Choisissez un genre :", ["Tous", "Male", "Female"])

    # Filtrer selon la sélection
    if genre_choisi == "Tous":
        df_filtre = df.copy()
    else:
        df_filtre = df[df['gender'] == genre_choisi]

    # Groupement par âge et genre (ou juste âge si genre filtré)
    df_glucose_gender = df_filtre.groupby(['age', 'gender'])['avg_glucose_level'].mean().reset_index()

    # Si "Tous", on trace les 2 genres ; sinon 1 seul
    fig = px.line(
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

    st.plotly_chart(fig, use_container_width=True)


