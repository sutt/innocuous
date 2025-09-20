import json
import numpy as np
from typing import Dict, Any


class StegoLogger:
    """Logger for steganography process."""

    def __init__(self):
        self.log_data: Dict[int, Dict[str, Any]] = {}
        self.step_count = 0

    def add_step(self, top_logits: Dict[str, np.float32]):
        """Adds a step to the log."""
        serializable_logits = {k: float(v) for k, v in top_logits.items()}
        self.log_data[self.step_count] = {"top_logits": serializable_logits}
        self.step_count += 1

    def dump(self, filepath: str):
        """Dumps the log data to a file."""
        with open(filepath, "w") as f:
            json.dump(self.log_data, f, indent=4)

    def load(self, filepath: str):
        """Loads log data from a file."""
        with open(filepath, "r") as f:
            raw_data = json.load(f)

        transformed_data = {}
        for step, data in raw_data.items():
            probs = data["top_logits"]
            logprobs = {
                token: np.float32(np.log(prob))
                for token, prob in probs.items()
                if prob > 0
            }
            transformed_data[int(step)] = {"top_logits": logprobs}

        self.log_data = transformed_data
        self.step_count = len(self.log_data)

    def get_log_data(self):
        """Returns the log data."""
        return self.log_data


_logger_instance = None


def get_logger():
    """Returns the singleton logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = StegoLogger()
    return _logger_instance


def reset_logger():
    """Resets the singleton logger instance."""
    global _logger_instance
    _logger_instance = None
