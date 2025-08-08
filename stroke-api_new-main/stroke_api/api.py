from fastapi import APIRouter, HTTPException
from stroke_api import filters

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Stroke Prediction !"}

# TODO décommenter et compléter
@router.get('/patients/')
def get_patients(gender: str = None, stroke: int = None, max_age: float = None):
    filtered_df = filters.filter_patient(
        stroke_data_df=filters.df,
        gender=gender,
        stroke=stroke,
        max_age=max_age
    )
    return filtered_df

# TODO décommenter et compléter
@router.get("/patients/{patient_id}")
def get_patient_id(patient_id: int):
    patient_data = filters.filter_id(
        stroke_data_df=filters.df,
        id=patient_id
    )

    if patient_data is None:
        raise HTTPException(status_code=404, detail="Patient non trouvé.")

    return patient_data
    # Gérer le cas où l'id de patient passé en paramètre n'existe pas


#  Ajout de la route stats 

@router.get('/stats/')
def get_stats():
    pass