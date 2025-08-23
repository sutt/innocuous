import numpy as np
import json
import time
import io
import ctypes
from contextlib import redirect_stderr
from llama_cpp import llama_log_set
from collections import OrderedDict
from typing import Dict


# Suppressing + logging stdout/stderr -----

llama_log_obj = []


def suppress_stderr(func):
    """Decorator to suppress stderr output from function calls."""
    def wrapper(*args, **kwargs):
        capture_stderr = io.StringIO()
        with redirect_stderr(capture_stderr):
            result = func(*args, **kwargs)
            llama_log_obj.append(capture_stderr.getvalue())
        return result
    return wrapper


def my_log_callback(level, message, user_data):
    """Callback function for llama logging."""
    llama_log_obj.append(message.decode())


log_callback = ctypes.CFUNCTYPE(None, ctypes.c_int,
                                ctypes.c_char_p, ctypes.c_void_p)(my_log_callback)

llama_log_set(log_callback, ctypes.c_void_p())


# LLM helpers ------

def to_json(data: Dict) -> str:
    """Convert dictionary to formatted JSON string."""
    data_t = {k: float(v) for k, v in data.items()}
    return json.dumps(
        data_t,
        indent=2,
    )


def logits_to_probabilities(data: Dict) -> Dict:
    """Convert log probabilities to actual probabilities."""
    return {k: np.exp(v) for k, v in data.items()}


def sum_probs(logprobs: Dict) -> float:
    """Sum all probabilities in a logprobs dictionary."""
    tmp = {k: np.exp(v) for k, v in logprobs.items()}
    return float(np.sum(np.array(list(tmp.values()))))


if __name__ == "__main__":
    def demo_tojson():
        d = {'hello': np.float32(1.23), 'world': np.float32(-0.999999)}
        print(to_json(d))
    
    demo_tojson()