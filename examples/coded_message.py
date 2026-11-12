"""Hide a short message in generated text and read it back.

Uses the logits already recorded in tests/data/recorded-logits, the same
replay the test suite uses. No model download, no GPU, and no llama-cpp-python
install: the script puts a stand-in module in place before stego_llm imports it.

Run from the repository root:

    python examples/coded_message.py
"""

from __future__ import annotations

import sys
import types
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# The replay path never constructs a model. llama-cpp-python has no wheel
# here, and stego_llm imports it at module load, so a stand-in is enough.
if "llama_cpp" not in sys.modules:
    _llama = types.ModuleType("llama_cpp")

    def _llama_log_set(*_args, **_kwargs):
        return None

    class _Llama:
        pass

    _llama.llama_log_set = _llama_log_set
    _llama.Llama = _Llama
    sys.modules["llama_cpp"] = _llama

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
