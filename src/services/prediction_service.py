import joblib
import numpy as np
from pathlib import Path
from typing import Optional

from src.schemas.prediction import PredictionCreate
from src.models.prediction import Prediction
from src.models.result import Result
from sqlalchemy.orm import Session

class PredictionService:
    def __init__(self):
        ml_model_path = Path(__file__).parent.parent / "ml" / "model"
        self.model = joblib.load(ml_model_path / "hcv_classifier.joblib")
        self.scaler = joblib.load(ml_model_path / "scaler.joblib")

    def predict(self, prediction_data: PredictionCreate) -> int:
        """
        Make a prediction using the trained HCV model
        
        Args:
            prediction_data: PredictionCreate schema containing the required parameters
            
        Returns:
            int: The predicted HCV class
        """
        # Extract the required features in the correct order
        features = np.array([
            prediction_data.ALB,  # Albumin
            prediction_data.ALP,  # Alkaline Phosphatase
            prediction_data.AST,  # Aspartate Aminotransferase
            prediction_data.CHE,  # Choline Esterase
            prediction_data.CGT,  # Gamma-Glutamyl Transferase
        ]).reshape(1, -1)
        
        # Scale the features
        scaled_features = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.model.predict(scaled_features)[0]
        return int(prediction)

    async def create_prediction_with_result(self, 
                                          db: Session, 
                                          prediction_data: PredictionCreate, 
                                          user_id: Optional[int] = None) -> Prediction:
        """
        Create a prediction record and its associated result
        
        Args:
            db: Database session
            prediction_data: The prediction data
            user_id: Optional user ID for the prediction
            
        Returns:
            Prediction: The created prediction record
        """
        # Make prediction
        predicted_class = self.predict(prediction_data)
        
        # Get the result from database
        result = db.query(Result).get(predicted_class)
        if not result:
            raise ValueError(f"Invalid prediction class: {predicted_class}")
        
        # Create prediction record
        prediction = Prediction(
            **prediction_data.model_dump(),
            user_id=user_id,
            result_id=result.id
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        
        return prediction

# Create a singleton instance
prediction_service = PredictionService()
