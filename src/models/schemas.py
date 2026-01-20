"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import datetime


class PredictionRequest(BaseModel):
    data: List[Dict[str, Any]] = Field(
        ..., 
        description="List of input records for prediction"
    )
    model_version: Optional[str] = Field(
        None,
        description="Specific model version to use"
    )


class PredictionResponse(BaseModel):
    predictions: List[float]
    model_version: str
    execution_time: float
    notebook_path: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)


class TrainingRequest(BaseModel):
    training_data_path: str
    model_version: str = "v1.0"
    hyperparameters: Optional[Dict[str, Any]] = None


class TrainingResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)


class DriftReportResponse(BaseModel):
    drift_detected: bool
    drift_score: float
    report_path: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    affected_features: List[str] = []
