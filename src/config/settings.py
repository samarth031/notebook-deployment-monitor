from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Churn Prediction API - v1"
    VERSION: str = "0.0.1"
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # Path Settings
    BASE_DIR: Path = Path(__file__).parent.parent
    NOTEBOOK_PATH: Path = BASE_DIR / "notebooks"
    EXECUTED_NOTEBOOKS_DIR: Path = BASE_DIR / "notebooks" / "executed"
    DATA_DIR: Path = BASE_DIR / "data"
    INPUT_DIR: Path = DATA_DIR / "input"
    OUTPUT_DIR: Path = DATA_DIR / "output"
    MONITORING_DIR: Path = BASE_DIR / "monitoring"
    REPORTS_DIR: Path = BASE_DIR / "reports"

    # Notebook Execution Settings
    NOTEBOOK_EXECUTION_TIMEOUT: int = 300 # 5 minutes
    MAX_NOTEBOOK_EXECUTIONS: int = 3
    NOTEBOOK_EXECUTION_INTERVAL: int = 300 # 5 minutes

    # Drift Monitoring Settings
    DRIFT_THRESHOLD: float = 0.1
    DRIFT_MONITORING_INTERVAL: int = 86400 # 1 day

    # Prometheus
    PROMETHEUS_PORT: int = 8085

    class Config:
        env_file = ".env"
        case_sensitive = True
        
settings = Settings()

# Create directories if they don't exist
settings.EXECUTED_NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)
settings.INPUT_DIR.mkdir(parents=True, exist_ok=True)
settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
settings.MONITORING_DIR.mkdir(parents=True, exist_ok=True)
settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    
if __name__ == "__main__":
    print(f"BASE_DIR: {settings.BASE_DIR}")
    print(f"NOTEBOOK_PATH: {settings.NOTEBOOK_PATH}")
    print(f"EXECUTED_NOTEBOOKS_DIR: {settings.EXECUTED_NOTEBOOKS_DIR}")
    print(f"DATA_DIR: {settings.DATA_DIR}")
    print(f"INPUT_DIR: {settings.INPUT_DIR}")
    print(f"OUTPUT_DIR: {settings.OUTPUT_DIR}")
    print(f"MONITORING_DIR: {settings.MONITORING_DIR}")
    print(f"REPORTS_DIR: {settings.REPORTS_DIR}")
    print(f"NOTEBOOK_EXECUTION_TIMEOUT: {settings.NOTEBOOK_EXECUTION_TIMEOUT}")
    print(f"MAX_NOTEBOOK_EXECUTIONS: {settings.MAX_NOTEBOOK_EXECUTIONS}")
    print(f"NOTEBOOK_EXECUTION_INTERVAL: {settings.NOTEBOOK_EXECUTION_INTERVAL}")
    print(f"DRIFT_THRESHOLD: {settings.DRIFT_THRESHOLD}")
    print(f"DRIFT_MONITORING_INTERVAL: {settings.DRIFT_MONITORING_INTERVAL}")
    print(f"PROMETHEUS_PORT: {settings.PROMETHEUS_PORT}")