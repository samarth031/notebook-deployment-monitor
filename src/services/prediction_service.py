"""
Prediction business logic
"""
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict, Any
import time

from services.notebook_executor import NotebookExecutor
from models.schemas import PredictionResponse
from config.settings import settings

logger = logging.getLogger(__name__)


class PredictionService:
    """Handle prediction requests and model execution"""
    
    def __init__(self):
        self.executor = NotebookExecutor()
        self.model_version = settings.MODEL_VERSION
    
    async def predict(
        self,
        data: List[Dict[str, Any]]
    ) -> PredictionResponse:
        """
        Make predictions on input data
        
        Args:
            data: List of input records
            
        Returns:
            PredictionResponse with predictions
        """
        start_time = time.time()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save input data
        input_file = settings.INPUT_DIR / f"input_{timestamp}.csv"
        output_file = settings.OUTPUT_DIR / f"predictions_{timestamp}.json"
        
        df = pd.DataFrame(data)
        df.to_csv(input_file, index=False)
        logger.info(f"Saved input data: {input_file}")
        
        # Execute notebook with parameters
        parameters = {
            'input_file': str(input_file),
            'output_file': str(output_file),
            'model_version': self.model_version
        }
        
        notebook_path = await self.executor.execute(
            parameters=parameters,
            output_name=f"prediction_{timestamp}.ipynb"
        )
        
        # Load predictions
        with open(output_file, 'r') as f:
            predictions = json.load(f)
        
        execution_time = time.time() - start_time
        
        return PredictionResponse(
            predictions=predictions,
            model_version=self.model_version,
            execution_time=execution_time,
            notebook_path=str(notebook_path)
        )
    
    async def retrain_model(
        self,
        training_data_path: str,
        model_version: str
    ):
        """
        Retrain model with new data
        
        Args:
            training_data_path: Path to training data
            model_version: Version identifier for new model
        """
        logger.info(f"Starting model retraining: {model_version}")
        
        parameters = {
            'training_data': training_data_path,
            'model_version': model_version,
            'mode': 'training'
        }
        
        await self.executor.execute(
            parameters=parameters,
            output_name=f"training_{model_version}.ipynb"
        )
        
        logger.info(f"Model retraining completed: {model_version}")
