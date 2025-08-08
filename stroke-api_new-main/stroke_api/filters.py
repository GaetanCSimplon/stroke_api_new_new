from typing import Optional
import pandas as pd


# Chargement des données (une fois)
df = pd.read_csv('df_final_test.csv')
df.drop(columns=['Unnamed: 0'], inplace=True)
print(df)

# Tester l'app avec :S
# poetry run fastapi dev stroke_api/main.py
# http://127.0.0.1:8000/docs : utiliser la fonctionnalité Try it out pour tester les routes

# Ajout des fonctions de filtrage des données cf notebook 1

def filter_patient(stroke_data_df: pd.DataFrame, stroke: Optional[int] = None, gender: Optional[str] = None, max_age: Optional[int] = None):
    filtered_df = stroke_data_df.copy()
    if max_age is not None:
        filtered_df = filtered_df[filtered_df['age'] <= max_age]
    if stroke is not None:
        filtered_df = filtered_df[filtered_df['stroke'] == stroke]
    if gender is not None:
        filtered_df = filtered_df[filtered_df['gender'] == gender]
    return filtered_df.to_dict(orient='records')

def filter_id(stroke_data_df: pd.DataFrame, id: int) -> Optional[dict]:
    filtered_df = stroke_data_df[stroke_data_df['id'] == id]
    
    if filtered_df.empty:
        return None  # Rien trouvé

    return filtered_df.to_dict(orient='records')[0] 
# Ensuite faire appel à ces fonctions dans le fichier api.py où sont définies les routes.
def filter_stats(stroke_data_df: pd.DataFrame, 
                 gender: Optional[str] = None, 
                 max_age: Optional[float] = None,
                 max_bmi: Optional[float] = None) -> dict:
    
    # Étape 1 : filtrage
    filtered_df = stroke_data_df.copy()
    
    if gender:
        filtered_df = filtered_df[filtered_df['gender'] == gender]
    
    if max_age:
        filtered_df = filtered_df[filtered_df['age'] <= max_age]
    
    if max_bmi:
        filtered_df = filtered_df[filtered_df['bmi'] <= max_bmi]
    
    # Étape 2 : statistiques (sur les données filtrées)
    stats = {
        "total_patients": len(filtered_df),
        "avg_age": round(filtered_df["age"].mean(), 2),
        "avg_bmi": round(filtered_df["bmi"].mean(), 2),
        "stroke_rate": round(filtered_df["stroke"].mean(), 4),  # Moyenne de 0/1 = taux d’AVC
        "gender_distribution": filtered_df["gender"].value_counts(normalize=True).round(2).to_dict()
    }
    
    return stats


