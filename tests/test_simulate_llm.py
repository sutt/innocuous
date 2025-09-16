import pytest
import numpy as np

from stego_llm.llm.mock import (
    mock_create_llm_client,
    mock_get_token_probabilities,
    MockLlama,
)


def _int_to_excel_col(n: int) -> str:
    """Converts a zero-based integer to a spreadsheet-style column name."""
    name = ""
    while n >= 0:
        name = chr(ord("a") + n % 26) + name
        n = n // 26 - 1
    return name


def test_mock_llm_simulation(mocker):
    """Tests the mock LLM simulation by inferring ten tokens."""
    mocker.patch(
        "stego_llm.llm.interface.create_llm_client", new=mock_create_llm_client
    )
    mocker.patch(
        "stego_llm.llm.interface.get_token_probabilities",
        new=mock_get_token_probabilities,
    )

    # We need to import these after patching
    from stego_llm.llm.interface import create_llm_client, get_token_probabilities

    llm = create_llm_client()
    assert isinstance(llm, MockLlama)
    assert llm.counter == 0

    num_inferences = 10
    num_logprobs = 50

    output = ""

    for i in range(num_inferences):
        logprobs = get_token_probabilities(llm, f"prompt {i}", num_output=num_logprobs)

        assert llm.counter == i + 1
        assert isinstance(logprobs, dict)
        assert len(logprobs) == num_logprobs

        prefix = f" {_int_to_excel_col(i)}"
        for token, logprob_val in logprobs.items():
            assert token.startswith(prefix)
            assert isinstance(logprob_val, np.float32)
            assert -10.0 <= logprob_val <= -0.1

        _tokens = list(logprobs.items())
        _top_token = _tokens[0]
        # debugging
        # print(f"=== iter={i}")
        # print(_tokens[:3])
        # print("...")
        # print(_tokens[-3:])

        output += _top_token[0]

    assert llm.counter == num_inferences
    
    print(f"output: {output}")


def test_encode_decode_simulation(mocker):
    """Tests encode/decode cycle with mock LLM."""
    mocker.patch(
        "stego_llm.llm.interface.create_llm_client", new=mock_create_llm_client
    )
    mocker.patch(
        "stego_llm.llm.interface.get_token_probabilities",
        new=mock_get_token_probabilities,
    )

    # We need to import these after patching
    from stego_llm.core import main_encode, main_decode

    initial_prompt = "The secret to life is"
    secret_message = b"42"
    chunk_size = 2

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
    pytest.main([__file__, "-s", "-vv"])
