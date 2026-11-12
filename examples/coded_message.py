"""Hide a short message in generated text and read it back.

Uses the logits already recorded in tests/data/recorded-logits, the same
replay the test suite uses. No model download and no GPU.

Run from the repository root:

    python examples/coded_message.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stego_llm.llm.mock import (  # noqa: E402
    create_mock_get_token_probabilities,
    mock_create_llm_client,
)

INITIAL_PROMPT = "Below is an iambic penatameter poem. Complete it:\nThe king"
SECRET = b"hello world"
CHUNK_SIZE = 2
LOG_FILE = "the-king-1.log"


def main() -> None:
    token_probabilities = create_mock_get_token_probabilities(version=3, log_file=LOG_FILE)
    patches = [
        patch("stego_llm.core.encoder.create_llm_client", new=mock_create_llm_client),
        patch("stego_llm.core.encoder.get_token_probabilities", new=token_probabilities),
        patch("stego_llm.core.decoder.create_llm_client", new=mock_create_llm_client),
        patch("stego_llm.core.decoder.get_token_probabilities", new=token_probabilities),
    ]
    for item in patches:
        item.start()
    try:
        from stego_llm.core import main_decode, main_encode

        cover = main_encode(INITIAL_PROMPT, SECRET, chunk_size=CHUNK_SIZE)
        recovered = main_decode(cover, INITIAL_PROMPT, chunk_size=CHUNK_SIZE)
    finally:
        for item in reversed(patches):
            item.stop()

    if cover is None or recovered != SECRET:
        raise SystemExit(f"round trip failed: {recovered!r}")

    print(f"initial prompt : {INITIAL_PROMPT!r}")
    print(f"secret message : {SECRET!r}")
    print(f"carrier text   : {cover!r}")
    print(f"decoded message: {recovered!r}")
    print("round trip     : OK")


if __name__ == "__main__":
    main()
