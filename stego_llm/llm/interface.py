import json
import os
import numpy as np
from llama_cpp import Llama
from .utilities import suppress_stderr, logits_to_probabilities, to_json


@suppress_stderr
def create_llm_client(
    model_path=None,
    **llm_options,
):
    """Initialize and return a Llama LLM client."""
    if model_path is None:
        model_path = os.environ.get("INNOCUOUS_LLM_PATH")
    if model_path is None:
        raise Exception("Neither INNOCUOUS_LLM_PATH nor --llm-path supplied. Exiting.")
    return Llama(
        model_path=str(model_path),
        logits_all=True,
        **llm_options
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


def check_llm(llm_path=None, verbose=False):
    """Check LLM path and perform a simple inference task."""
    model_path = llm_path
    if model_path is None:
        print("Checking for INNOCUOUS_LLM_PATH environment variable...")
        model_path = os.environ.get("INNOCUOUS_LLM_PATH")
    else:
        print(f"Using LLM path from argument: {llm_path}")

    if model_path is None:
        print("LLM path not found. Please supply --llm-path or set INNOCUOUS_LLM_PATH.")
        return False
    print(f"LLM path set to: {model_path}")

    if not os.path.exists(model_path):
        print(f"File not found at: {model_path}")
        return False
    print(f"LLM file found at: {model_path}")

    try:
        print("Attempting to load LLM...")
        llm = create_llm_client(model_path=model_path)
        print("LLM loaded successfully.")
    except Exception as e:
        print(f"Failed to load LLM: {e}")
        return False

    try:
        print("Performing simple inference task...")
        top_logprobs = get_token_probabilities(llm, "The king")
        print("Inference task successful.")
        if verbose:
            print("Top log probabilities:")
            top_logprobs = logits_to_probabilities(top_logprobs)
            print(to_json(top_logprobs))
    except Exception as e:
        print(f"Inference task failed: {e}")
        return False

    return True
