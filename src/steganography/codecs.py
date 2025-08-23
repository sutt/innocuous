import math
import logging
from typing import List


logger = logging.getLogger(__name__)


def message_to_chunks(message: bytes, chunk_size: int = 3) -> List[int]:
    """Convert a byte message into integer chunks for steganographic encoding."""
    num_iters = math.ceil(len(message) * 8 / chunk_size)
    bits_message = "".join([format(_byte, "08b") for _byte in message])
    logger.debug(f"encode_bits: {bits_message}")
    
    int_message = []
    for i in range(num_iters):
        chunk_bits = bits_message[(i * chunk_size):(i * chunk_size) + chunk_size]
        chunk_int = int(chunk_bits, 2)
        int_message.append(chunk_int)
    
    return int_message


def chunks_to_message(enc_message: List[str], chunk_size: int = 3) -> bytes:
    """Convert encoded integer chunks back to the original byte message."""
    decoded_bits = ""
    for i, char in enumerate(enc_message):
        if i == (len(enc_message) - 1):
            current_chunk_size = 8 - (len(decoded_bits) % 8)
        else:
            current_chunk_size = chunk_size
        decoded_bits += format(int(char), f"0{current_chunk_size}b")
    
    logger.debug(f"decode_bits: {decoded_bits}")
    
    decoded_ints = []
    for i in range(len(decoded_bits) // 8):
        decoded_ints.append(int(decoded_bits[i * 8:(i * 8) + 8], 2))
    
    return bytes(decoded_ints)