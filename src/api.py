"""
API routes and endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import logging

from models.schemas import (
    PredictionRequest, 
    PredictionResponse, 
    TrainingRequest,
    TrainingResponse,
    DriftReportResponse
)
from services.prediction_service import PredictionService
from services.drift_monitor import DriftMonitor
from monitoring.metrics import (
    prediction_counter,
    prediction_latency,
    prediction_error_counter
)
import time

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
prediction_service = PredictionService()
drift_monitor = DriftMonitor()


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Make predictions using the ML model
    """
    start_time = time.time()
    
    try:
        # Execute prediction
        result = await prediction_service.predict(request.data)
        
        # Record metrics
        latency = time.time() - start_time
        prediction_counter.labels(
            model_version=result.model_version
        ).inc(len(result.predictions))
        prediction_latency.observe(latency)
        
        logger.info(f"Prediction completed in {latency:.2f}s")
        return result
        
    except Exception as e:
        prediction_error_counter.inc()
        logger.error(f"Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/retrain", response_model=TrainingResponse)
async def retrain_model(
    request: TrainingRequest,
    background_tasks: BackgroundTasks
):
    """
    Trigger model retraining
    """
    try:
        # Run training in background
        background_tasks.add_task(
            prediction_service.retrain_model,
            request.training_data_path,
            request.model_version
        )
        
        return TrainingResponse(
            status="training_started",
            message="Model retraining initiated in background"
        )
        
    except Exception as e:
        logger.error(f"Retraining failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/drift-report", response_model=DriftReportResponse)
async def get_drift_report():
    """
    Get latest data drift report
    """
    try:
        report = await drift_monitor.get_latest_report()
        return report
        
    except Exception as e:
        logger.error(f"Drift report failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-drift")
async def check_drift(background_tasks: BackgroundTasks):
    """
    Trigger drift detection
    """
    background_tasks.add_task(drift_monitor.check_drift)
    return {"status": "drift_check_started"}
