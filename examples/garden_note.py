"""Innocuous coded message — garden journal cover.

Hides the README TODO phrase ``the message could be anything`` inside an
ordinary garden journal entry, the kind of text you might post on a local
gardening forum or community board. The cover is casual and public; the
payload is recoverable with the same prompt + params.

Quick self-check (no model needed)::

    python examples/garden_note.py --dry-run
    python examples/garden_note.py --mock

Full round-trip (needs a llama.cpp GGUF)::

    python examples/garden_note.py --llm-path /path/to/model.gguf
"""

from __future__ import annotations

import argparse
import logging
import math
import os
import sys
from typing import List

# Cover genre: a casual garden journal entry — not a king poem, not a
# cafe note, not a yard-sale bulletin, not a seaside walk. Ordinary public prose.
INITIAL_PROMPT = (
    "Continue this casual garden journal entry in a warm, ordinary voice. "
    "Keep it under 130 words and suitable for a neighbourhood gardening forum post:\n"
    "This spring I finally cleared the back garden bed behind the shed. "
    "The soil was dark and rich and the first seedlings were already pushing through"
)

# Exactly the phrase from the README TODO line.
MESSAGE_TEXT = "the message could be anything"

CHUNK_SIZE = 2
NUM_LOGPROBS = 40

DEBUG = True
logger = logging.getLogger(__name__)
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level, format="")

ENCODED_BITS = (
    "0111010001101000011001010010000001101101011001010111001101110011"
    "0110000101100111011001010010000001100011011011110111010101101100"
    "0110010000100000011000100110010100100000011000010110111001111001"
    "0111010001101000011010010110111001100111"
)


def _message_to_chunks(message: bytes, chunk_size: int) -> List[int]:
    """Local copy of stego_llm.steganography.codecs.message_to_chunks.

    Kept local so --dry-run / --mock need no llama_cpp install.
    Must stay in sync with that function.
    """
    num_iters = math.ceil(len(message) * 8 / chunk_size)
    bits_message = "".join(format(b, "08b") for b in message)
    logger.debug(f"encode_bits: {bits_message}")
    int_message: List[int] = []
    for i in range(num_iters):
        chunk_bits = bits_message[i * chunk_size : (i + 1) * chunk_size]
        int_message.append(int(chunk_bits, 2) if chunk_bits else 0)
    return int_message


def _chunks_to_message(enc_message: List[int], chunk_size: int) -> bytes:
    """Local copy of stego_llm.steganography.codecs.chunks_to_message."""
    decoded_bits = ""
    for i, char in enumerate(enc_message):
        if i == (len(enc_message) - 1):
            current_chunk_size = 8 - (len(decoded_bits) % 8)
            if current_chunk_size == 0:
                current_chunk_size = chunk_size
        else:
            current_chunk_size = chunk_size
        decoded_bits += format(int(char), f"0{current_chunk_size}b")
    logger.debug(f"decode_bits: {decoded_bits}")
    decoded_ints: List[int] = []
    for i in range(len(decoded_bits) // 8):
        decoded_ints.append(int(decoded_bits[i * 8 : (i * 8) + 8], 2))
    return bytes(decoded_ints)


def _print_banner(msg: bytes) -> None:
    print("=" * 60)
    print("INNOCUOUS CODED MESSAGE — GARDEN JOURNAL")
    print("=" * 60)
    print(f"plaintext : {msg!r}")
    print(f"cover     : casual garden journal (neighbourhood forum)")
    print(f"chunk_size: {CHUNK_SIZE}   num_logprobs: {NUM_LOGPROBS}")
    print("cover is ordinary prose; payload is recoverable bytes")
    print("=" * 60)


def dry_run(msg: bytes) -> int:
    """Show how the message is packed into encode chunks (no LLM)."""
    _print_banner(msg)
    bits = "".join(format(b, "08b") for b in msg)
    assert bits == ENCODED_BITS, "ENCODED_BITS constant out of sync with MESSAGE_TEXT"
    chunks = _message_to_chunks(msg, chunk_size=CHUNK_SIZE)
    recovered = _chunks_to_message(chunks, chunk_size=CHUNK_SIZE)
    assert recovered == msg, f"codec round-trip failed: {recovered!r} != {msg!r}"

    print("\n### dry-run (no LLM required)")
    print(f"bytes      : {list(msg)}")
    print(f"bit length : {len(bits)}")
    print(f"encode_bits: {bits[:64]}... (total {len(bits)} bits)")
    print(f"n_chunks   : {len(chunks)}  (chunk_size={CHUNK_SIZE})")
    print(f"chunks     : {chunks}")
    print(f"codec check: {recovered!r} == {msg!r}  OK")
    print("\nCover prompt preview:")
    print(INITIAL_PROMPT[:200] + "...")
    print("\nTo produce the coded passage, run without --dry-run:")
    print("  python examples/garden_note.py --llm-path /path/to/model.gguf")
    print("Or verify the stego logic with mocks (no GGUF):")
    print("  python examples/garden_note.py --mock")
    return 0


def mock_round_trip(msg: bytes) -> int:
    """Verify encode→decode end-to-end with the in-repo mock LLM (no GGUF)."""
    _print_banner(msg)
    print("\n### mock round-trip (no GGUF required)")
    print("Patching LLM with proc tokens v2 (alpha-only, no filter bypass needed).")

    # Ensure a fake llama_cpp exists so stego_llm.llm.interface can be imported
    # even when llama-cpp-python is not installed in this env.
    import types

    if "llama_cpp" not in sys.modules:
        fake_llama = types.ModuleType("llama_cpp")
        fake_llama.Llama = object  # type: ignore[attr-defined]
        # stego_llm.llm.utilities imports llama_log_set at import time
        fake_llama.llama_log_set = lambda *a, **kw: None  # type: ignore[attr-defined]
        # stego_llm.llm.mock may reference llama_cpp internals indirectly — keep minimal
        sys.modules["llama_cpp"] = fake_llama
    else:
        # Ensure llama_log_set exists for utilities import
        if not hasattr(sys.modules["llama_cpp"], "llama_log_set"):
            sys.modules["llama_cpp"].llama_log_set = lambda *a, **kw: None  # type: ignore[attr-defined]

    # Local codec sanity first (no LLM involved)
    chunks = _message_to_chunks(msg, chunk_size=CHUNK_SIZE)
    assert _chunks_to_message(chunks, chunk_size=CHUNK_SIZE) == msg

    from unittest.mock import patch

    from stego_llm.llm.mock import create_mock_get_token_probabilities, mock_create_llm_client

    # Patch at core.* where main_encode/main_decode look up the symbols
    with patch("stego_llm.core.encoder.create_llm_client", new=mock_create_llm_client), patch(
        "stego_llm.core.encoder.get_token_probabilities",
        new=create_mock_get_token_probabilities(version=2),
    ), patch("stego_llm.core.decoder.create_llm_client", new=mock_create_llm_client), patch(
        "stego_llm.core.decoder.get_token_probabilities",
        new=create_mock_get_token_probabilities(version=2),
    ):
        from stego_llm.core import main_decode, main_encode

        encoded_prompt = main_encode(
            initial_prompt=INITIAL_PROMPT,
            msg=msg,
            chunk_size=CHUNK_SIZE,
            num_logprobs=NUM_LOGPROBS,
        )
        print(f"\nencoded_prompt length: {len(encoded_prompt)} chars")
        cover = encoded_prompt[len(INITIAL_PROMPT) :]
        print(f"cover continuation   : {cover[:160]!r} ...")
        decoded = main_decode(
            encoded_prompt=encoded_prompt,
            initial_prompt=INITIAL_PROMPT,
            chunk_size=CHUNK_SIZE,
            num_logprobs=NUM_LOGPROBS,
        )
        print(f"\ndecoded_msg: {decoded!r}")
        assert decoded == msg, f"mock round-trip failed: {decoded!r} != {msg!r}"
        print(f"recovered  : {decoded.decode('utf-8')!r}")
        print("\ndone. mock encode->decode round-tripped!")

    bits = "".join(format(b, "08b") for b in msg)
    print(f"\nencode_bits preview: {bits[:64]}... (total {len(bits)} bits)")
    return 0


def live_round_trip(msg: bytes, llm_path: str) -> int:
    """Encode then decode with a real GGUF model."""
    from stego_llm import main_decode, main_encode

    _print_banner(msg)
    print(f"\nLLM path: {llm_path}")
    encoded_prompt = main_encode(
        initial_prompt=INITIAL_PROMPT,
        msg=msg,
        chunk_size=CHUNK_SIZE,
        num_logprobs=NUM_LOGPROBS,
        llm_path=llm_path,
    )
    cover_only = encoded_prompt[len(INITIAL_PROMPT) :]
    print("\n### coded garden journal (cover text only):")
    print(cover_only)
    print("\n### full encoded_prompt (prompt + cover):")
    print(encoded_prompt)

    decoded = main_decode(
        encoded_prompt=encoded_prompt,
        initial_prompt=INITIAL_PROMPT,
        chunk_size=CHUNK_SIZE,
        num_logprobs=NUM_LOGPROBS,
        llm_path=llm_path,
    )
    print(f"\ndecoded_msg: {decoded!r}")
    assert decoded == msg, (msg, decoded)
    print(f"recovered  : {decoded.decode('utf-8')!r}")
    print("\ndone. live encode->decode round-tripped!")
    return 0


def example_garden_note(llm_path: str | None = None) -> None:
    """Programmatic entry point (mirrors other examples/*)."""
    msg = MESSAGE_TEXT.encode("utf-8")
    if llm_path:
        live_round_trip(msg, llm_path)
    else:
        # Default to mock so `from examples.yard_sale_note import example_yard_sale_note`
        # works in CI without a GGUF.
        mock_round_trip(msg)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", help="Show packing without an LLM")
    g.add_argument("--mock", action="store_true", help="Mock LLM encode->decode (no GGUF)")
    parser.add_argument("--llm-path", default=os.environ.get("INNOCUOUS_LLM_PATH"), help="Path to GGUF")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args(argv)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    msg = MESSAGE_TEXT.encode("utf-8")

    if args.dry_run:
        return dry_run(msg)
    if args.mock:
        return mock_round_trip(msg)
    if not args.llm_path:
        print(
            "No LLM path. Use --dry-run (packing), --mock (mock LLM), "
            "or --llm-path / set INNOCUOUS_LLM_PATH for a live round-trip.",
            file=sys.stderr,
        )
        dry_run(msg)
        return 2
    return live_round_trip(msg, args.llm_path)


if __name__ == "__main__":
    raise SystemExit(main())
