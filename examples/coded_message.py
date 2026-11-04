"""
Example: Encoding and decoding an innocuous secret message using stego_llm.
Demonstrates hiding an arbitrary UTF-8 plain-text coded message inside
an innocuous LLM-generated poem, with reproducible round-trip decoding.
"""

import logging
from stego_llm import main_encode, main_decode

# Set up logging
DEBUG = True
logger = logging.getLogger(__name__)
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level, format="%(message)s")


def example_innocuous_coded_message():
    """Example encoding/decoding a real plain-text secret message."""
    
    # Secret message to hide
    secret_message = "The rendezvous is at midnight by the old lighthouse."
    original_msg = secret_message.encode("utf-8")
    
    logger.info(f"Original secret message: '{secret_message}'")
    logger.info(f"Message bytes ({len(original_msg)} bytes): {original_msg}")

    # Hyperparameters for steganographic encoding
    chunk_size = 2
    num_logprobs = 40

    # Innocuous cover prompt
    initial_prompt = "Below is an iambic pentameter poem. Complete it:\nThe king"

    logger.info("\n--- Steganographic Encoding ---")
    encoded_prompt = main_encode(
        initial_prompt=initial_prompt,
        msg=original_msg,
        chunk_size=chunk_size,
        num_logprobs=num_logprobs,
    )

    print("\n### Generated Innocuous Text (Cover):")
    print(encoded_prompt)

    logger.info("\n--- Steganographic Decoding ---")
    decoded_bytes = main_decode(
        encoded_prompt=encoded_prompt,
        initial_prompt=initial_prompt,
        chunk_size=chunk_size,
        num_logprobs=num_logprobs,
    )
    
    decoded_message = decoded_bytes.decode("utf-8", errors="replace")
    logger.info(f"Decoded message bytes: {decoded_bytes}")
    logger.info(f"Decoded secret message: '{decoded_message}'")

    # Verification
    assert original_msg == decoded_bytes, "Error: Decoded bytes do not match original!"
    assert secret_message == decoded_message, "Error: Decoded text does not match secret!"
    print("\n[SUCCESS] Round-trip steganography verified successfully!")


if __name__ == "__main__":
    example_innocuous_coded_message()
