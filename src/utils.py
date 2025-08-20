from llama_cpp import Llama
import numpy as np
import json

import json
import time
import io
import ctypes
from contextlib import redirect_stderr
from llama_cpp import (
    Llama,
    llama_log_set,
)
from collections import OrderedDict
from typing import (
    Dict,
)

# suppressing + logging stdout/stderr -----

llama_log_obj = []

def suppress_stderr(func):
    def wrapper(*args, **kwargs):
        capture_stderr = io.StringIO()
        with redirect_stderr(capture_stderr):
            result = func(*args, **kwargs)
            llama_log_obj.append(capture_stderr.getvalue())
        return result
    return wrapper

def my_log_callback(level, message, user_data):
    llama_log_obj.append(message.decode())

log_callback = ctypes.CFUNCTYPE(None, ctypes.c_int, 
            ctypes.c_char_p, ctypes.c_void_p)(my_log_callback)

llama_log_set(log_callback, ctypes.c_void_p())
