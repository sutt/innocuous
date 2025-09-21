import pytest
import numpy as np
import os

from stego_llm.llm.mock import (
    mock_create_llm_client,
    create_mock_get_token_probabilities,
    MockLlama,
)

GEN_SCHEDULE = {
    "0": {
        "initial_prompt": "Below is an iambic penatameter poem. Complete it:\nThe king",
        "msg": b"hello world",
        "chunk_size": 2,
        "num_logprobs": 100,
        "log_file": "./tests/data/recorded-logits/the-king-1.log",
        # "llm_path": "../mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    },
    "1": {
        "initial_prompt": "Below is an iambic penatameter poem. Complete it:\nThe king",
        "msg": b"hello world",
        "chunk_size": 3,
        "num_logprobs": 100,
        "log_file": "./tests/data/recorded-logits/the-king-2.log",
        # "llm_path": "../mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    },
}


def gen_logits_for_tests():
    """
    Generate token-logprobs logs into the test data directory. This can be used
    to setup replay tests.
    """
    from stego_llm.core import main_encode, main_decode

    keys = ["0", "1"]
    for current_key in keys:
        print(f"generating on key: {current_key}\n=======\n")
        enc_args = GEN_SCHEDULE[current_key]
        covertext = main_encode(**enc_args)
        print(covertext)
    print("gen_logit complete.")


def test_gen_0(mocker):
    """Tests encode/decode cycle with a particular logfile and saved arguments"""

    # Select which replay logfile and arguments you'll use:
    key = "0"
    enc_args = GEN_SCHEDULE[key]
    log_file = enc_args["log_file"]
    log_file = os.path.basename(log_file)

    mocker.patch("stego_llm.core.encoder.create_llm_client", new=mock_create_llm_client)
    mocker.patch(
        "stego_llm.core.encoder.get_token_probabilities",
        new=create_mock_get_token_probabilities(version=3, log_file=log_file),
    )
    mocker.patch("stego_llm.core.decoder.create_llm_client", new=mock_create_llm_client)
    mocker.patch(
        "stego_llm.core.decoder.get_token_probabilities",
        new=create_mock_get_token_probabilities(version=3, log_file=log_file),
    )

    from stego_llm.core import main_encode, main_decode

    initial_prompt = enc_args["initial_prompt"]
    secret_message = enc_args["msg"]
    chunk_size = enc_args["chunk_size"]

    print(f"\ninitial_prompt: '{initial_prompt}'")
    print(f"secret_message: {secret_message}")

    encoded_prompt = main_encode(
        initial_prompt,
        secret_message,
        chunk_size=chunk_size,
    )

    assert encoded_prompt is not None
    assert encoded_prompt != initial_prompt
    print(f"encoded_prompt: '{encoded_prompt}'")

    decoded_message = main_decode(
        encoded_prompt,
        initial_prompt,
        chunk_size=chunk_size,
    )

    print(f"decoded_message: {decoded_message}")
    assert decoded_message == secret_message


if __name__ == "__main__":
    # pytest.main([__file__, "-s", "-vv"])
    gen_logits_for_tests()
