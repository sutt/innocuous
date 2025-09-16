"""Mock objects for LLM simulation."""
import numpy as np
from typing import Dict

_MOCK_LOGPROBS = np.linspace(-0.1, -10.0, 500, dtype=np.float32)
np.random.default_rng(0).shuffle(_MOCK_LOGPROBS)


def _int_to_excel_col(n: int) -> str:
    """Converts a zero-based integer to a spreadsheet-style column name."""
    name = ""
    while n >= 0:
        name = chr(ord("a") + n % 26) + name
        n = n // 26 - 1
    return name


class MockLlama:
    """A mock Llama object with a counter."""

    def __init__(self):
        self.counter = 0


def mock_create_llm_client(model_path=None, **llm_options):
    """Mock factory for the Llama object."""
    return MockLlama()


def proc_gen_tokens(iter_num: int, num_logprobs: int) -> Dict[str, np.float32]:
    """Procedurally generates tokens and log probabilities."""
    iter_prefix = _int_to_excel_col(iter_num)
    tokens = {}
    for i in range(num_logprobs):
        token_str = f" {iter_prefix}{i+1}"
        logprob_idx = (iter_num * num_logprobs + i) % len(_MOCK_LOGPROBS)
        tokens[token_str] = _MOCK_LOGPROBS[logprob_idx]
    return tokens


def mock_get_token_probabilities(llm, prompt, num_output=10):
    """Mock for get_token_probabilities."""
    if not isinstance(llm, MockLlama):
        raise TypeError(
            "llm must be a MockLlama instance for mock_get_token_probabilities"
        )

    logprobs = proc_gen_tokens(llm.counter, num_output)
    llm.counter += 1
    return logprobs
