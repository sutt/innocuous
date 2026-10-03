"""Innocuous coded message example.

Hides a short, friendly plaintext inside an ordinary botanical field note —
the cover text looks like something you might post on a garden forum; the
payload is the README-suggested phrase ``the message could be anything``.

This is the catchy "use case" example: an innocuous coded message you can
encode, publish as plain prose, and later decode with the same prompt + params.

Requires ``INNOCUOUS_LLM_PATH`` (or ``--llm-path``) for a live round-trip.
Pass ``--dry-run`` to inspect the message bits/chunks without an LLM.
"""

from __future__ import annotations

import argparse
import logging
import math
import os
import sys
from typing import List


# The cover genre on purpose: not another king poem — a quiet public garden note.
INITIAL_PROMPT = (
    "Continue this short botanical field note in a calm, ordinary voice. "
    "Keep it under 120 words and suitable for a community garden newsletter:\n"
    "Late afternoon light filtered through the greenhouse glass as volunteers "
    "tended the tomato vines. Near the tool shed, a small chalkboard listed "
)

# Exactly the phrase called out in the README TODO.
MESSAGE_TEXT = "the message could be anything"

CHUNK_SIZE = 2
NUM_LOGPROBS = 40


DEBUG = True
logger = logging.getLogger(__name__)
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level, format="")


def _message_to_chunks(message: bytes, chunk_size: int = 3) -> List[int]:
    """Local copy of the codec helper so --dry-run needs no llama.cpp install."""
    num_iters = math.ceil(len(message) * 8 / chunk_size)
    bits_message = "".join(format(_byte, "08b") for _byte in message)
    logger.debug(f"encode_bits: {bits_message}")
    int_message = []
    for i in range(num_iters):
        chunk_bits = bits_message[(i * chunk_size) : (i * chunk_size) + chunk_size]
        int_message.append(int(chunk_bits, 2))
    return int_message


def _print_banner(msg: bytes) -> None:
    print("=" * 60)
    print("INNOCUOUS CODED MESSAGE")
    print("=" * 60)
    print(f"plaintext : {msg!r}")
    print(f"cover     : botanical field note (garden newsletter)")
    print(f"chunk_size: {CHUNK_SIZE}   num_logprobs: {NUM_LOGPROBS}")
    print("one-liner : ordinary prose in; recoverable bytes out")
    print("=" * 60)


def dry_run(msg: bytes) -> None:
    """Show how the innocuous message is packed into encode chunks (no LLM)."""
    _print_banner(msg)
    bits = "".join(format(b, "08b") for b in msg)
    chunks = _message_to_chunks(msg, chunk_size=CHUNK_SIZE)
    print("\n### dry-run (no LLM required)")
    print(f"bytes     : {list(msg)}")
    print(f"bit length: {len(bits)}")
    print(f"encode_bits (first 64): {bits[:64]}{'...' if len(bits) > 64 else ''}")
    print(f"n_chunks  : {len(chunks)}")
    print(f"chunks    : {chunks}")
    print("\nCover prompt preview:")
    print(INITIAL_PROMPT[:180] + "...")
    print("\nTo produce the coded passage, re-run without --dry-run once")
    print("INNOCUOUS_LLM_PATH points at a llama.cpp GGUF model.")


def example_innocuous_coded_message(llm_path: str | None = None) -> None:
    """Encode then decode a short innocuous plaintext in a field-note cover."""
    # Lazy imports: encode/decode pull in llama-cpp-python.
    from stego_llm import main_decode, main_encode

    original_msg = MESSAGE_TEXT.encode("utf-8")
    _print_banner(original_msg)

    logger.info(f"encoded_msg: {original_msg}")

    encoded_prompt = main_encode(
        initial_prompt=INITIAL_PROMPT,
        msg=original_msg,
        chunk_size=CHUNK_SIZE,
        num_logprobs=NUM_LOGPROBS,
        llm_path=llm_path,
    )

    cover_only = encoded_prompt[len(INITIAL_PROMPT) :]
    print("\n### coded field note (cover text only):")
    print(cover_only)
    print("\n### full encoded_prompt (prompt + cover):")
    print(encoded_prompt)

    decoded_msg = main_decode(
        encoded_prompt=encoded_prompt,
        initial_prompt=INITIAL_PROMPT,
        chunk_size=CHUNK_SIZE,
        num_logprobs=NUM_LOGPROBS,
        llm_path=llm_path,
    )

    print(f"\ndecoded_msg: {decoded_msg}")
    assert original_msg == decoded_msg, (original_msg, decoded_msg)
    print(f"recovered  : {decoded_msg.decode('utf-8')!r}")
    print("\ndone. it worked — the innocuous coded message round-tripped!")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print message packing + cover prompt without calling an LLM",
    )
    parser.add_argument(
        "--llm-path",
        default=os.environ.get("INNOCUOUS_LLM_PATH"),
        help="Path to a llama.cpp GGUF model (or set INNOCUOUS_LLM_PATH)",
    )
    args = parser.parse_args(argv)

    msg = MESSAGE_TEXT.encode("utf-8")
    if args.dry_run:
        dry_run(msg)
        return 0

    if not args.llm_path:
        print(
            "No LLM path set. Pass --llm-path, export INNOCUOUS_LLM_PATH, "
            "or use --dry-run to inspect the message without a model.",
            file=sys.stderr,
        )
        dry_run(msg)
        return 2

    example_innocuous_coded_message(llm_path=args.llm_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
