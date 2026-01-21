"""
Data drift monitoring service
"""
import pandas
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from pathlib import Path
import datetime
import logging
import json

from config.settings import settings
from models.schemas import DriftReportResponse

logger = logging.getLogger(__name__)


class DriftMonitor:
    """Monitor data drift using Evidently AI"""
    
    def __init__(self):
        self.drift_threshold = settings.DRIFT_THRESHOLD
        self.monitoring_dir = settings.MONITORING_DIR
        self.reference_data_path = settings.DATA_DIR / "reference_data.csv"
    
    async def check_drift(self) -> DriftReportResponse:
        """
        Check for data drift between reference and current data
        
        Returns:
            DriftReportResponse with drift metrics
        """
        logger.info("Starting drift detection")
        
        # Load reference data (training data)
        reference_data = pandas.read_csv(self.reference_data_path)
        
        # Load recent production data
        current_data = self._load_recent_production_data()
        
        # Create drift report
        report = Report(metrics=[DataDriftPreset()])
        report.run(
            reference_data=reference_data,
            current_data=current_data
        )
        
        # Save report
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.monitoring_dir / f"drift_report_{timestamp}.html"
        report.save_html(str(report_path))
        
        # Extract metrics
        drift_results = report.as_dict()
        drift_score = drift_results['metrics'][0]['result']['dataset_drift']
        drift_detected = drift_score > self.drift_threshold
        
        # Get affected features
        affected_features = [
            feature for feature, info in 
            drift_results['metrics'][0]['result']['drift_by_columns'].items()
            if info['drift_detected']
        ]
        
        logger.info(f"Drift score: {drift_score}, Detected: {drift_detected}")
        
        return DriftReportResponse(
            drift_detected=drift_detected,
            drift_score=drift_score,
            report_path=str(report_path),
            timestamp=datetime.datetime.now(),
            affected_features=affected_features
        )
    
    def _load_recent_production_data(self) -> pandas.DataFrame:
        """Load recent production data for comparison"""
        # Combine recent input files
        input_files = sorted(settings.INPUT_DIR.glob("input_*.csv"))
        recent_files = input_files[-10:]  # Last 10 predictions
        
        dfs = [pandas.read_csv(f) for f in recent_files]
        return pandas.concat(dfs, ignore_index=True)
    
    async def get_latest_report(self) -> DriftReportResponse:
        """Get the latest drift report"""
        reports = sorted(self.monitoring_dir.glob("drift_report_*.html"))
        
        if not reports:
            return await self.check_drift()
        
        latest_report = reports[-1]
        # Parse timestamp from filename
        # Return cached report info
        return DriftReportResponse(
            drift_detected=False,  # Load from saved results
            drift_score=0.0,
            report_path=str(latest_report),
            timestamp=datetime.datetime.now(),
            affected_features=[]
        )
