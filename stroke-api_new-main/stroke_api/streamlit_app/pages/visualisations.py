import streamlit as st
import plotly.express as px
from utils.data import load_data

df = load_data()

st.title("Visualisation des données")

# IMC moyen selon âge et genre
st.markdown("### IMC moyen selon l'âge et le genre")
selected_display_gender = st.selectbox("Choisissez un genre :", ["Homme", "Femme"])
gender_display = {"Homme": "Male", "Femme": "Female"}
selected_gender = gender_display[selected_display_gender]

filtered_df = df[df["gender"] == selected_gender]
df_bmi = filtered_df.groupby("age")["bmi"].mean().reset_index()

fig_bmi = px.line(df_bmi, x="age", y="bmi",
                  title=f"IMC moyen par âge pour le genre : {selected_display_gender}",
                  labels={"age": "Âge", "bmi": "IMC moyen"},
                  template="plotly_white")

st.plotly_chart(fig_bmi, use_container_width=True)

# Glucose moyen
st.markdown("### Glucose moyen selon l'âge et le genre")
genre_choisi = st.selectbox("Choisissez un genre :", ["Tous", "Male", "Female"])
df_filtre = df if genre_choisi == "Tous" else df[df["gender"] == genre_choisi]
df_glucose = df_filtre.groupby(["age", "gender"])["avg_glucose_level"].mean().reset_index()

fig_glucose = px.line(df_glucose, x="age", y="avg_glucose_level",
                      color="gender" if genre_choisi == "Tous" else None,
                      labels={"avg_glucose_level": "Glucose moyen", "age": "Âge", "gender": "Genre"},
                      title="Glucose moyen selon l'âge et le genre")

st.plotly_chart(fig_glucose, use_container_width=True)

# AVC par catégorie d'âge
df_avc_by_age = df.groupby("age_category", as_index=False)["stroke"].mean()
st.subheader("Taux d'AVC selon la catégorie d'âge")
fig_age = px.bar(df_avc_by_age, x="age_category", y="stroke",
                 labels={"stroke": "Taux d'AVC", "age_category": "Catégorie d'âge"},
                 template="plotly_white")
st.plotly_chart(fig_age, use_container_width=True)

# AVC par genre
df_avc_by_gender = df.groupby("gender", as_index=False)["stroke"].mean()
st.subheader("Taux d'AVC selon le genre")
fig_gender = px.bar(df_avc_by_gender, x="gender", y="stroke",
                    labels={"stroke": "Taux d'AVC", "gender": "Genre"},
                    template="plotly_white")
st.plotly_chart(fig_gender, use_container_width=True)
