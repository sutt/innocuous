from llama_cpp import Llama
import numpy as np
from contextlib import redirect_stderr
from llama_cpp import (
    Llama,
    # llama_log_set,
)
# from collections import OrderedDict
# from typing import (
#     Dict,
# )
# import json
# import time
# import io
# import ctypes
# import json

from utils import llama_log_set

PROMPT = "The capital of France is"

# @suppress_stderr
def init_llm():
    return Llama(
        model_path="../data/mistral-7b-instruct-v0.2.Q4_K_M.gguf", 
        logits_all=True,
    )

# @suppress_stderr
def infer_llm(num_output=10):
    output = llm(
        PROMPT, 
        max_tokens=1, 
        # temperature=2.0,
        logprobs=num_output,
        echo=False
    )
    top_logprobs = output['choices'][0]['logprobs']['top_logprobs'][0]
    return top_logprobs

def sum_probs(logprobs):
    tmp = {k: np.exp(v) for k,v in logprobs.items()}
    return np.sum(np.array(list(tmp.values())))


llm = init_llm()
top_logprobs = infer_llm()
print(top_logprobs)
    
    