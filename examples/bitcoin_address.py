import logging
from stego_llm import main_encode, main_decode
from stego_llm.llm import create_llm_client
from stego_llm.crypto import decode_bitcoin_address

import psutil  # TMP-DEBUG
import os  # TMP-DEBUG

process = psutil.Process(os.getpid())  # TMP-DEBUG


DEBUG = True
logger = logging.getLogger(__name__)
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level, format="")


def example_bitcoin_address():
    """Example encoding/decoding a Bitcoin address."""

    # Parameters
    addr = "12Wfw4L3oPJFk2q6osDoZLYAwdFkhvgt4E"
    info = decode_bitcoin_address(addr)
    original_msg = bytes.fromhex(info["payload_hex"])

    logger.info(f"encoded_msg: {original_msg}")

    chunk_size = 2
    num_logprobs = 40

    # Standard initial prompt
    initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king"

    # Main functions
    llm = create_llm_client()

    encoded_prompt = main_encode(
        llm=llm,
        initial_prompt=initial_prompt,
        msg=original_msg,
        chunk_size=chunk_size,
        num_logprobs=num_logprobs,
    )

    print("\n### repr: encoded_prompt:")
    print(repr(encoded_prompt)[1:-1])

    print("\n### encoded_prompt:")
    print(encoded_prompt)

    # Must re-init llm here or decode fails for some reason
    # IMPORTANT: this can trigger OOM silent fail, in which case decode
    # and verify message match never runs and program exits as if successful.
    print(
        f"Memory before decode init: {process.memory_info().rss / 1024 / 1024:.1f} MB"
    )  # TMP-DEBUG
    llm = create_llm_client()
    print(
        f"Memory after decode init: {process.memory_info().rss / 1024 / 1024:.1f} MB"
    )  # TMP-DEBUG

    decoded_msg = main_decode(
        llm=llm,
        encoded_prompt=encoded_prompt,
        initial_prompt=initial_prompt,
        chunk_size=chunk_size,
        num_logprobs=num_logprobs,
    )

    print(
        f"Memory after decode: {process.memory_info().rss / 1024 / 1024:.1f} MB"
    )  # TMP-DEBUG
    print(f"decoded_msg: {decoded_msg}")
    assert original_msg == decoded_msg
    print("\ndone. it worked!")


if __name__ == "__main__":
    example_bitcoin_address()
