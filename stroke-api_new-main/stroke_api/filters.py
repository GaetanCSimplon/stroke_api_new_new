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
    """Filters patients from a dataset

    Args:
        stroke_data_df (pd.DataFrame): Select dataframe
        stroke (Optional[int], optional): 2 values (1 = positive / 0 = negative). Defaults to None.
        gender (Optional[str], optional): Either 'Male' or 'Female' . Defaults to None.
        max_age (Optional[int], optional): Between 0 and 100. Defaults to None.

    Returns:
        dict: dictionary with selected data
    """
    filtered_df = stroke_data_df.copy()
    if max_age is not None:
        filtered_df = filtered_df[filtered_df['age'] <= max_age]
    if stroke is not None:
        filtered_df = filtered_df[filtered_df['stroke'] == stroke]
    if gender is not None:
        filtered_df = filtered_df[filtered_df['gender'] == gender]
    return filtered_df.to_dict(orient='records')

def filter_id(stroke_data_df: pd.DataFrame, id: int) -> Optional[dict]:
    """Filters patients id

    Args:
        stroke_data_df (pd.DataFrame): Select dataframe
        id (int): Integer 

    Returns:
        Optional[dict]: Dictionnary with data from patient id
    """
    filtered_df = stroke_data_df[stroke_data_df['id'] == id]
    
    if filtered_df.empty:
        return None  # Rien trouvé

    return filtered_df.to_dict(orient='records')[0] 
# Ensuite faire appel à ces fonctions dans le fichier api.py où sont définies les routes.
def filter_stats(stroke_data_df: pd.DataFrame, 
                 gender: Optional[str] = None, 
                 max_age: Optional[float] = None,
                 max_bmi: Optional[float] = None) -> dict:
    """Shows differents stats from dataset

    Args:
        stroke_data_df (pd.DataFrame): Select a dataframe
        gender (Optional[str], optional): Select gender (Male or Female). Defaults to None.
        max_age (Optional[float], optional): Select age (Between 0 to 100). Defaults to None.
        max_bmi (Optional[float], optional): Select BMI (Between 16 to 70). Defaults to None.

    Returns:
        dict: Dictionnary with all stats
    """
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
# Ajouter les fonctions de filtrage pour les autres routes.

