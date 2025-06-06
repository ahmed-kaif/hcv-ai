from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src import models, schemas, database, oauth

router = APIRouter(prefix="/predictions", tags=["Predictions"])

@router.post("/", response_model=schemas.PredictionOut)
def create_prediction(data: schemas.PredictionCreate,
                      db: Session = Depends(database.get_db),
                      current_user: models.User = Depends(oauth.get_current_user)):
    prediction = models.Prediction(**data.model_dump(), user_id=current_user.id)
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction

@router.get("/", response_model=list[schemas.PredictionOut])
def get_my_predictions(db: Session = Depends(database.get_db),
                       current_user: models.User = Depends(oauth.get_current_user)):
    return db.query(models.Prediction).filter(models.Prediction.user_id == current_user.id).all()

@router.get("/{prediction_id}", response_model=schemas.PredictionOut)
def get_prediction(prediction_id: int,
                   db: Session = Depends(database.get_db),
                   current_user: models.User = Depends(oauth.get_current_user)):
    prediction = db.query(models.Prediction).get(prediction_id)
    if not prediction or prediction.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return prediction

@router.get("/user/{user_id}", response_model=list[schemas.PredictionOut])
def get_predictions_for_user(user_id: int,
                             db: Session = Depends(database.get_db),
                             current_user: models.User = Depends(oauth.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db.query(models.Prediction).filter(models.Prediction.user_id == user_id).all()

@router.delete("/{prediction_id}")
def delete_prediction(prediction_id: int,
                      db: Session = Depends(database.get_db),
                      current_user: models.User = Depends(oauth.get_current_user)):
    prediction = db.query(models.Prediction).get(prediction_id)
    if not prediction or prediction.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db.delete(prediction)
    db.commit()
    return {"message": "Prediction deleted"}
