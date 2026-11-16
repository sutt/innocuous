#!/usr/bin/env python3
"""Hide a short coded message in generated text and read it back.

This example replays logits already stored in
``tests/data/recorded-logits/the-king-3.log``, the same fixture used by
``tests/test_replay_v1.py``. It does not download a model or need a GGUF
file.

Hidden message: ``b"groovy baby"``
Initial prompt: the repository's standard king-poem fixture.

Run from the repository root:

    python examples/coded_message.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Allow running as `python examples/coded_message.py` without installing the package.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.chdir(REPO_ROOT)

from stego_llm.llm.mock import (  # noqa: E402
    mock_create_llm_client,
    create_mock_get_token_probabilities,
)


INITIAL_PROMPT = "Below is an iambic penatameter poem. Complete it:\nThe king"
SECRET_MESSAGE = b"groovy baby"
CHUNK_SIZE = 2
NUM_LOGPROBS = 100
LOG_FILE = "the-king-3.log"


def _install_replay_mocks() -> None:
    """Replay recorded logits so encode/decode need no live model."""
    import stego_llm.core.encoder as encoder
    import stego_llm.core.decoder as decoder

    replay = create_mock_get_token_probabilities(version=3, log_file=LOG_FILE)
    encoder.create_llm_client = mock_create_llm_client
    encoder.get_token_probabilities = replay
    decoder.create_llm_client = mock_create_llm_client
    decoder.get_token_probabilities = replay


def run_coded_message() -> bytes:
    """Encode SECRET_MESSAGE into cover text and decode it back."""
    _install_replay_mocks()
    from stego_llm.core import main_decode, main_encode

    covertext = main_encode(
        initial_prompt=INITIAL_PROMPT,
        msg=SECRET_MESSAGE,
        chunk_size=CHUNK_SIZE,
        num_logprobs=NUM_LOGPROBS,
    )
    if covertext is None:
        raise RuntimeError("encoding failed: main_encode returned None")
    if not covertext.startswith(INITIAL_PROMPT):
        raise RuntimeError("encoding failed: cover text does not start with the prompt")

    recovered = main_decode(
        encoded_prompt=covertext,
        initial_prompt=INITIAL_PROMPT,
        chunk_size=CHUNK_SIZE,
        num_logprobs=NUM_LOGPROBS,
    )
    if recovered != SECRET_MESSAGE:
        raise AssertionError(
            f"round trip failed: expected {SECRET_MESSAGE!r}, got {recovered!r}"
        )
    return covertext


def main() -> None:
    covertext = run_coded_message()
    generated = covertext[len(INITIAL_PROMPT) :]
    print("initial prompt:")
    print(INITIAL_PROMPT)
    print()
    print("hidden message:")
    print(SECRET_MESSAGE)
    print()
    print("generated cover text:")
    print(generated)
    print()
    print("recovered message:")
    print(SECRET_MESSAGE)
    print()
    print("round trip: ok")


if __name__ == "__main__":
    main()
