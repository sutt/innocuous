import json
import os
import numpy as np
from llama_cpp import Llama
from .utilities import suppress_stderr, logits_to_probabilities, to_json


@suppress_stderr
def create_llm_client(
    model_path=None,
):
    """Initialize and return a Llama LLM client."""
    if model_path is None:
        model_path = os.environ.get(
            "INNOCUOUS_LLM_PATH",
            "/home/user/dev/innocuous/data/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        )
    return Llama(
        model_path=model_path,
        logits_all=True,
    )


@suppress_stderr
def get_token_probabilities(llm, prompt, num_output=10):
    """Get top token probabilities from the LLM for the given prompt."""
    output = llm(
        prompt,
        max_tokens=1,
        logprobs=num_output,
        echo=False,
    )
    top_logprobs = output["choices"][0]["logprobs"]["top_logprobs"][0]
    return top_logprobs


def demo():
    """Demo function showing basic LLM usage."""
    # TODO - add this cli status check command
    llm = create_llm_client()
    top_logprobs = get_token_probabilities(llm)
    top_logprobs = logits_to_probabilities(top_logprobs)
    print(to_json(top_logprobs))
