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
    "2": {
        "initial_prompt": "Below is an iambic penatameter poem. Complete it:\nThe king",
        "msg": b"groovy baby",
        "chunk_size": 2,
        "num_logprobs": 100,
        "log_file": "./tests/data/recorded-logits/the-king-3.log",
        # "llm_path": "../mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    },
    "3": {
        "initial_prompt": "Below is an iambic penatameter poem. Complete it:\nThe king",
        "msg": b"groovy baby",
        "chunk_size": 3,
        "num_logprobs": 100,
        "log_file": "./tests/data/recorded-logits/the-king-4.log",
        # "llm_path": "../mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    },
    "4": {
        "initial_prompt": "Below is an iambic penatameter poem. Complete it:\nThe king",
        "msg": b"visit boston",
        "chunk_size": 3,
        "num_logprobs": 100,
        "log_file": "./tests/data/recorded-logits/the-king-5.log",
        # "llm_path": "../mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    },
}


def gen_logits_for_tests():
    """
    Generate token-logprobs logs into the test data directory. This can be used
    to setup replay tests.
    """
    from stego_llm.core import main_encode, main_decode

    keys = list(GEN_SCHEDULE.keys())
    for current_key in keys:
        print(f"generating on key: {current_key}\n=======\n")
        enc_args = GEN_SCHEDULE[current_key]
        covertext = main_encode(**enc_args)
        print(covertext)
    print("gen_logit complete.")


@pytest.mark.parametrize(
    "schedule_key",
    [
        "0",
        "1",
        "2",
        "3",
    ],
)
def test_mocked_enc_dec(mocker, schedule_key):
    """
    Tests encode/decode cycle with a particular logfile and saved arguments
    No backtracking hits in decoder for these items
    """

    # From test parameter `schedule_key`, load relevant info from schedule:
    enc_args = GEN_SCHEDULE[schedule_key]

    # Extract relevant data
    log_file = os.path.basename(enc_args["log_file"])
    initial_prompt = enc_args["initial_prompt"]
    secret_message = enc_args["msg"]
    chunk_size = enc_args["chunk_size"]

    # Apply mocks to LLM methods
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

    # Main test logic + logging
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


@pytest.mark.parametrize(
    "schedule_key",
    [
        "4",
    ],
)
def test_mocked_enc_dec_with_backtracking(mocker, schedule_key):
    """
    Tests encode/decode cycle with a particular logfile and saved arguments
    Allow backtracking hits in decoder for these items with more sophisticated mock logic
    """

    # From test parameter `schedule_key`, load relevant info from schedule:
    enc_args = GEN_SCHEDULE[schedule_key]

    # Extract relevant argument data for the methods we're testing and/or mocks
    log_file = os.path.basename(enc_args["log_file"])
    initial_prompt = enc_args["initial_prompt"]
    secret_message = enc_args["msg"]
    chunk_size = enc_args["chunk_size"]

    # Apply mocks to LLM-encoding methods
    mocker.patch("stego_llm.core.encoder.create_llm_client", new=mock_create_llm_client)
    mocker.patch(
        "stego_llm.core.encoder.get_token_probabilities",
        new=create_mock_get_token_probabilities(version=3, log_file=log_file),
    )
    from stego_llm.core import main_encode

    # Test Logic for encoding portion
    print(f"\ninitial_prompt: '{initial_prompt}'")
    print(f"secret_message: {secret_message}")

    encoded_prompt = main_encode(
        initial_prompt,
        secret_message,
        chunk_size=chunk_size,
    )

    # Helper methods for mocking LLM-decoding methods
    from stego_llm.core.trace import _trace_decoding_step as original_trace

    decoder_llm = MockLlama()
    patched_trace_call_count = 0

    def mock_decoder_create_llm_client(*args, **kwargs):
        return decoder_llm

    def patched_trace(step_name, **kwargs):
        if step_name == "branch_deadend":
            # This should work since every time we hit this branch in decoder
            # we have generated 1 new mock token (and incremented the counter).
            # But by the decoder's logic, we'll remove that newest token and
            # regenerate on the previous step. So we need to cancel-out counter
            # increment side-effect from previous step here by decrementing.
            # But this might not work for decoding that takes multiple iterations
            # to discover it needs to backtrack. For more power you can potentially
            # check how many recursive solve() on the callstack.
            nonlocal patched_trace_call_count
            patched_trace_call_count += 1
            decoder_llm.counter -= 1
        return original_trace(step_name, **kwargs)

    # Apply mocks to LLM-decoding methods
    mocker.patch(
        "stego_llm.core.decoder.create_llm_client", new=mock_decoder_create_llm_client
    )
    mocker.patch(
        "stego_llm.core.decoder.get_token_probabilities",
        new=create_mock_get_token_probabilities(version=3, log_file=log_file),
    )
    mocker.patch("stego_llm.core.decoder._trace_decoding_step", new=patched_trace)

    from stego_llm.core import main_decode

    # Test logic for decoding portion
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

    # check if backtracking was actually used in this test
    # if not, it's not a flaw per-se, but this example can be moved
    # via (pytest paramters) to `test_mocked_enc_dec` instead.
    assert patched_trace_call_count > 0



if __name__ == "__main__":
    pytest.main([__file__, "-s", "-vv"])
    # gen_logits_for_tests()
