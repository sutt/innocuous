"""Innocuous coded message example: a Sunday baking letter hiding a short note.

The cover text is an ordinary letter about a rainy Sunday spent baking — the
kind of message that raises no eyebrows in an inbox. Buried inside it, encoded
in the first-token probabilities of the completing LLM, is a short note that
only `main_decode` (with the same initial prompt and parameters) can recover.

Validated without model weights:

    python examples/sunday_letter.py --mock

With a real llama.cpp model (see README Quickstart):

    python examples/sunday_letter.py
"""
import argparse
import logging

from stego_llm import main_encode, main_decode

DEBUG = True
logger = logging.getLogger(__name__)
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level, format="")


def _apply_mock_llm():
    """Swap in the bundled MockLlama so the example runs without weights."""
    from stego_llm.llm.mock import (
        mock_create_llm_client,
        create_mock_get_token_probabilities,
    )
    import stego_llm.core.encoder as encoder
    import stego_llm.core.decoder as decoder

    get_probs = create_mock_get_token_probabilities(version=1)

    def _override_filter(toks):
        """Pass tokens through unchanged; the mock vocab trips real filters."""
        return toks

    for module in (encoder, decoder):
        module.create_llm_client = mock_create_llm_client
        module.get_token_probabilities = get_probs
        module.pre_selection_filter = _override_filter
        module.post_selection_filter = _override_filter


def example_sunday_letter(use_mock: bool = False, dry_run: bool = False):
    """Example encoding/decoding a short note inside a baking letter."""

    if use_mock:
        _apply_mock_llm()
        logger.info("using mock llm (no model weights required)")

    # The hidden message, buried in the letter below
    original_msg = b"fresh bread at dawn"

    logger.info(f"encoded_msg: {original_msg}")

    chunk_size = 2
    num_logprobs = 40

    # The innocent cover: the letter the decoder expects to continue
    initial_prompt = (
        "Dear Sam, what a quiet Sunday this has been. The rain tapped the "
        "kitchen window all morning while I baked the rye loaf we talked "
        "about, and the whole flat smelled of crust and cloves. I saved you "
        "the heel of it, still warm"
    )

    # Main functions
    encoded_prompt = main_encode(
        initial_prompt=initial_prompt,
        msg=original_msg,
        chunk_size=chunk_size,
        num_logprobs=num_logprobs,
    )

    print("\n### repr: encoded_prompt:")
    print(repr(encoded_prompt)[1:-1])

    print("\n### encoded_prompt:")
    print(encoded_prompt)

    if dry_run:
        print("\n--dry-run: skipping decode")
        return

    decoded_msg = main_decode(
        encoded_prompt=encoded_prompt,
        initial_prompt=initial_prompt,
        chunk_size=chunk_size,
        num_logprobs=num_logprobs,
    )
    print(f"decoded_msg: {decoded_msg}")
    assert original_msg == decoded_msg
    print("\ndone. it worked!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mock", action="store_true", help="run against the bundled MockLlama (no weights)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="encode only; skip the decode round-trip"
    )
    args = parser.parse_args()
    example_sunday_letter(use_mock=args.mock, dry_run=args.dry_run)
