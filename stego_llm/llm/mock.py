"""Mock objects for LLM simulation."""

import numpy as np
from typing import Callable, Dict
import os
import warnings
from stego_llm.log import get_logger

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
    """
    Procedurally generates tokens and log probabilities.
    e.g. a1, a2, ... a50, b1, b2, ... b50, ..., aa1, aa2, ...
    note: does not return logit values sorted in desc order (as non-mock-obj does)
    """
    iter_prefix = _int_to_excel_col(iter_num)
    tokens = {}
    for i in range(num_logprobs):
        token_str = f" {iter_prefix}{i + 1}"
        logprob_idx = (iter_num * num_logprobs + i) % len(_MOCK_LOGPROBS)
        tokens[token_str] = _MOCK_LOGPROBS[logprob_idx]
    return tokens


def proc_gen_tokens_v2(iter_num: int, num_logprobs: int) -> Dict[str, np.float32]:
    """
    Procedurally generates tokens and log probabilities.
    e.g. Aa, Ab, ... Aax, Ba, Bb, ..., Bax, ..., AAa, AAb, ...
    note: does not return logit values sorted in desc order (as non-mock-obj does)
    """
    iter_prefix = _int_to_excel_col(iter_num)
    tokens = {}
    for i in range(num_logprobs):
        rank_suffix = _int_to_excel_col(i)
        token_str = f" {iter_prefix.upper()}{rank_suffix.lower()}"
        logprob_idx = (iter_num * num_logprobs + i) % len(_MOCK_LOGPROBS)
        tokens[token_str] = _MOCK_LOGPROBS[logprob_idx]
    return tokens


def proc_gen_tokens_v3(iter_num: int, num_logprobs: int) -> Dict[str, np.float32]:
    """
    Loads tokens and log probabilities from a log file.
    """
    logger = get_logger()
    log_data = logger.get_log_data()

    if iter_num not in log_data:
        raise IndexError(f"Log data not found for step {iter_num}")

    all_logprobs = log_data[iter_num]["top_logits"]

    if num_logprobs > len(all_logprobs):
        warnings.warn(
            f"Requested {num_logprobs} logprobs, but only {len(all_logprobs)} available. "
            "Returning all available logprobs."
        )
        return all_logprobs

    return dict(list(all_logprobs.items())[:num_logprobs])


def create_mock_get_token_probabilities(
    version: int = 1, log_file: str = None
) -> Callable[[MockLlama, str, int], Dict[str, np.float32]]:
    """
    Factory for mocks of get_token_probabilities.
    Pass version for which simulated tokens you want in your test.
    """
    if version == 3:
        if not log_file:
            raise ValueError("log_file must be provided for version 3")

        from stego_llm.log import reset_logger

        reset_logger()
        logger = get_logger()
        log_path = os.path.join("tests", "data", "recorded-logits", log_file)
        logger.load(log_path)

    def mock_func(llm, prompt, num_output=10):
        if not isinstance(llm, MockLlama):
            raise TypeError(
                "llm must be a MockLlama instance for mock_get_token_probabilities"
            )

        if version == 1:
            logprobs = proc_gen_tokens(llm.counter, num_output)
        elif version == 2:
            logprobs = proc_gen_tokens_v2(llm.counter, num_output)
        elif version == 3:
            logprobs = proc_gen_tokens_v3(llm.counter, num_output)
        else:
            raise TypeError(
                f"create_mock_get_token_probabilities version: {version} not recognized."
            )

        llm.counter += 1

        return logprobs

    return mock_func
