import os
import time
import gc

import pytest

from stego_llm.core import main_decode, main_encode

# Get model path from environment variable: preferred and fallabck
TEST_LLM_PATH = os.environ.get("INNOCUOUS_TEST_LLM_PATH")
if TEST_LLM_PATH is None:
    TEST_LLM_PATH = os.environ.get("INNOCUOUS_LLM_PATH")


@pytest.fixture(autouse=True)
def cleanup_between_tests():
    """
    Allow memory cleanup between heavy LLM tests to avoid OOM.
    Run as `pytest -m slow -s -v` to see this fixture at work with timings.
    Run the following and look for exit code 137 if oom kill suspected:
    >  dmesg -T | egrep -i 'out of memory|oom-kill|Killed process|cgroup: memory'
    """
    yield
    print(
        f"\n[CLEANUP] Running garbage collection and 2s sleep at {time.strftime('%H:%M:%S')}"
    )
    gc.collect()
    time.sleep(2)


@pytest.mark.slow
@pytest.mark.skipif(
    not TEST_LLM_PATH,
    reason="Neither INNOCUOUS_TEST_LLM_PATH nor INNOCUOUS_LLM_PATH environment variable are set",
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
        llm_path=TEST_LLM_PATH,
    )

    assert encoded_text is not None
    assert encoded_text != initial_prompt

    # Decode the message
    decoded_message = main_decode(
        encoded_prompt=encoded_text,
        initial_prompt=initial_prompt,
        chunk_size=chunk_size,
        llm_path=TEST_LLM_PATH,
    )

    assert decoded_message is not None
    assert decoded_message == message_to_encode


@pytest.mark.slow
@pytest.mark.skipif(
    not TEST_LLM_PATH,
    reason="Neither INNOCUOUS_TEST_LLM_PATH nor INNOCUOUS_LLM_PATH environment variable are set",
)
def test_decode_example_1():
    """
    Test decoder only with previously generated example
    Will be used for punctuation re-insertion proof-of-concept
    """
    GENERATED_TEXT = """
Below is an iambic penatameter poem. Complete it:
The king of all the realms did lie there weak,
With eyes that wept their last goodbye to day,
The crown did glister by his lifeless cheeks,
Yet still no heir to
"""
    GENERATED_TEXT = GENERATED_TEXT.strip()
    assert GENERATED_TEXT == GENERATED_TEXT

    encoded_message = b"hello world"
    initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king"

    decoded_message = main_decode(
        encoded_prompt=GENERATED_TEXT,
        initial_prompt=initial_prompt,
        chunk_size=3,
        llm_path=TEST_LLM_PATH,
    )

    assert decoded_message == encoded_message


@pytest.mark.slow
@pytest.mark.skipif(
    not TEST_LLM_PATH,
    reason="Neither INNOCUOUS_TEST_LLM_PATH nor INNOCUOUS_LLM_PATH environment variable are set",
)
def test_decode_example_2():
    """
    Test decoder only
    Use example from previous test: test_decode_example_1
    But with punctuation removed (commas at end of each line)
    to confuse the decoding and see if it can recover.
    """

    GENERATED_TEXT_NO_PUNCTUATION = """
Below is an iambic penatameter poem. Complete it:
The king of all the realms did lie there weak
With eyes that wept their last goodbye to day
The crown did glister by his lifeless cheeks
Yet still no heir to
"""
    GENERATED_TEXT_NO_PUNCTUATION = GENERATED_TEXT_NO_PUNCTUATION.strip()
    assert GENERATED_TEXT_NO_PUNCTUATION == GENERATED_TEXT_NO_PUNCTUATION

    encoded_message = b"hello world"
    initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king"

    decoded_message = main_decode(
        encoded_prompt=GENERATED_TEXT_NO_PUNCTUATION,
        initial_prompt=initial_prompt,
        chunk_size=3,
        llm_path=TEST_LLM_PATH,
    )

    assert decoded_message == encoded_message


if __name__ == "__main__":
    import sys
    import logging

    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)

    # test_encode_decode_integration()
    # test_decode_example_1()
    # test_decode_example_2()
