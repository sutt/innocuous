import os

import pytest

from stego_llm.core import main_decode, main_encode

# Get model path from environment variable
LLAMA_MODEL_PATH = os.environ.get("LLAMA_MODEL_PATH")


@pytest.mark.slow
@pytest.mark.skipif(
    not LLAMA_MODEL_PATH, reason="LLAMA_MODEL_PATH environment variable not set"
)
def test_encode_decode_integration():
    """
    Test the full encode-decode cycle.
    This is a slow test and requires a language model.
    """
    initial_prompt = "This is a test."
    message_to_encode = b"secret message"
    chunk_size = 2

    # Encode the message
    encoded_text = main_encode(
        initial_prompt=initial_prompt,
        msg=message_to_encode,
        chunk_size=chunk_size,
        llm_path=LLAMA_MODEL_PATH,
    )

    assert encoded_text is not None
    assert encoded_text != initial_prompt

    # Decode the message
    decoded_message = main_decode(
        encoded_prompt=encoded_text,
        initial_prompt=initial_prompt,
        chunk_size=chunk_size,
        llm_path=LLAMA_MODEL_PATH,
    )

    assert decoded_message is not None
    assert decoded_message == message_to_encode
