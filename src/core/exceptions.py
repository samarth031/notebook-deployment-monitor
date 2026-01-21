"""
Custom exceptions
"""

class NotebookExecutionError(Exception):
    """Raised when notebook execution fails"""
    pass


class ModelNotFoundError(Exception):
    """Raised when model file is not found"""
    pass


class DriftDetectionError(Exception):
    """Raised when drift detection fails"""
    pass
