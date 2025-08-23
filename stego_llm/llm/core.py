import json
import numpy as np
from llama_cpp import (
    Llama,
)
from .utils import (
    llama_log_set,
    suppress_stderr,
    cvt_to_logprobs,
    to_json,
)
    

@suppress_stderr
def init_llm(
    model_path="/home/user/dev/innocuous/data/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
):
    return Llama(
        model_path=model_path, 
        logits_all=True,
    )

@suppress_stderr
def infer_llm(
    llm, 
    prompt,
    num_output=10
    ):
    output = llm(
        prompt, 
        max_tokens=1, 
        logprobs=num_output,
        echo=False,
    )
    top_logprobs = output['choices'][0]['logprobs']['top_logprobs'][0]
    return top_logprobs


def demo():
    llm = init_llm()
    top_logprobs = infer_llm(llm)
    top_logprobs = cvt_to_logprobs(top_logprobs)
    print(to_json(top_logprobs))

    
    