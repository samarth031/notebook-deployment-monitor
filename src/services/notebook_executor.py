"""
Papermill notebook execution service
"""
import papermill
from pathlib import Path
import datetime
import logging
from typing import Dict, Any, Optional

from config.settings import settings
from core.exceptions import NotebookExecutionError

logger = logging.getLogger(__name__)


class NotebookExecutor:
    """Execute Jupyter notebooks with parameters using Papermill"""
    
    def __init__(self):
        self.notebook_path = settings.NOTEBOOK_PATH
        self.output_dir = settings.EXECUTED_NOTEBOOKS_DIR
        self.timeout = settings.NOTEBOOK_EXECUTION_TIMEOUT
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        output_name: Optional[str] = None
    ) -> Path:
        """
        Execute notebook with given parameters
        
        Args:
            parameters: Dictionary of parameters to pass to notebook
            output_name: Custom name for output notebook
            
        Returns:
            Path to executed notebook
        """
        if output_name is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            output_name = f"executed_{timestamp}.ipynb"
        
        output_path = self.output_dir / output_name
        
        try:
            logger.info(f"Executing notebook: {self.notebook_path}")
            logger.info(f"Parameters: {parameters}")
            
            papermill.execute_notebook(
                input_path=str(self.notebook_path),
                output_path=str(output_path),
                parameters=parameters,
                kernel_name='python3',
                progress_bar=True,
                request_save_on_cell_execute=True,
                execution_timeout=self.timeout
            )
            
            logger.info(f"Notebook executed successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Notebook execution failed: {str(e)}", exc_info=True)
            raise NotebookExecutionError(f"Failed to execute notebook: {str(e)}")
