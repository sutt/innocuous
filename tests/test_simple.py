import pytest
import logging
from stego_llm.steganography.codecs import (
    chunks_to_message,
    message_to_chunks,
)


logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "input_bytes, chunk_size",
    [
        (bytes([19, 1, 244]), 4),
        (bytes([19, 1, 244]), 3),
        (bytes([19, 1, 244]), 2),
        (bytes([19, 1, 244]), 1),
        (bytes([17, 5]), 3),
        (bytes([17, 5]), 2),
        (bytes([17, 5]), 1),
        (bytes([255]), 1),
        (bytes([0]), 1),
    ],
)
def test_encode_decode(input_bytes, chunk_size):
    msg_enc = message_to_chunks(input_bytes, chunk_size=chunk_size)
    logger.debug("msg_enc:", msg_enc)
    dec_msg = chunks_to_message(msg_enc, chunk_size=chunk_size)
    logger.debug("dec_msg:", dec_msg)
    assert input_bytes == dec_msg
