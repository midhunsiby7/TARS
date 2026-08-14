import abc

class BaseRunner(abc.ABC):
    """Abstract base class for all benchmark runners."""
    
    def __init__(self, config_manager):
        self.config = config_manager
        
    @abc.abstractmethod
    def run_benchmark(self, model_info):
        """Runs the benchmark and returns the metrics."""
        pass
