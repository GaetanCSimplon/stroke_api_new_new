import streamlit as st
import pandas as pd
import numpy as np
st.title('Stroke Data App')

tab_home, tab_data, tab_vis, tab_stats = st.tabs(['Accueil', 'Données', 'Visualisations', 'Statistiques'])

with tab_home:
    st.markdown(''' **Bienvenue sur Stroke Data App !** ''')
    st.markdown(''' Stroke Data App vous permet de consulter les données anonymisées de patients ayant consultés pour des problèmes cardiaques''')
    st.markdown(''' Vous pouvez interroger notre base de données selon des critères que vous définissez, visualiser simplements les données et consulter les statistiques globales''')


with tab_data:
    df = pd.read_csv('df_final_test.csv')
    df.drop(columns=['Unnamed: 0'], inplace=True)

    st.dataframe(df)

with tab_vis:
    df_bmi = df.groupby(['gender', 'age'])['bmi'].mean().reset_index()
    st.write('IMC moyen selon l\'âge')
    st.bar_chart(data=df_bmi,
                x='age',
                y='bmi',
                x_label='age',
                y_label='bmi')
