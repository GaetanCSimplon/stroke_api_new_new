import streamlit as st
from utils.data import load_data
from stroke_api.filters import filter_stats

df = load_data()

st.header("Statistiques Globales")

genre = st.selectbox("Choisir le genre :", ["Tous", "Homme", "Femme"])
max_age = st.slider("Âge maximal :", 0, 100, 100)
max_bmi = st.slider("IMC maximal :", 10.0, 60.0, 60.0)

genre_map = {"Homme": "Male", "Femme": "Female"}
genre_filtered = genre_map[genre] if genre != "Tous" else None

stats = filter_stats(df, gender=genre_filtered, max_age=max_age, max_bmi=max_bmi)

st.markdown(f"""
- **Nombre total de patients** : {stats['total_patients']}
- **Âge moyen** : {stats['avg_age']}
- **IMC moyen** : {stats['avg_bmi']}
- **Taux d'AVC** : {stats['stroke_rate'] * 100:.2f}%
- **Répartition hommes/femmes** : {stats['gender_distribution']}
""")
