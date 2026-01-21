"""
Prometheus metrics configuration
"""
from prometheus_client import Counter, Histogram, Gauge
from prometheus_fastapi_instrumentator import Instrumentator


# Custom metrics
prediction_counter = Counter(
    'model_predictions_total',
    'Total number of predictions made',
    ['model_version']
)

prediction_latency = Histogram(
    'model_prediction_latency_seconds',
    'Model prediction latency in seconds',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

prediction_error_counter = Counter(
    'model_prediction_errors_total',
    'Total number of prediction errors'
)

drift_score_gauge = Gauge(
    'model_data_drift_score',
    'Current data drift score'
)

model_accuracy_gauge = Gauge(
    'model_accuracy',
    'Current model accuracy'
)


def setup_metrics(app):
    """Setup Prometheus metrics instrumentation"""
    Instrumentator().instrument(app).expose(app)
