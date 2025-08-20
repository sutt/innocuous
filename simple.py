import random
import json
import math
import logging
from typing import List

# Toggle below to control logging level
DEBUG = True
logger = logging.getLogger(__name__)
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level, format="")


def demo():
    """
        examples of how to work with bits and bytes in python
    """
    byte_values = bytes([13, 17])   # same as b'\x0d'
    print("Len of bytes:", len(byte_values))
    print("As bytes:", byte_values)

    for i in range(len(byte_values)):
        # Get its integer representation
        int_value = byte_values[i]
        print("As integer:", int_value)

        # Print in binary with 8 bits
        binary_str = format(int_value, "08b")
        print("As binary string:", binary_str)

        # Convert to a string encoding (base64 or hex is common)
        hex_str = bytes([byte_values[i]]).hex()
        print("As hex string:", hex_str)

# demo()

def build_selections():
    """
        build selections array: simulate top_p logprobs from llama
    """
    N_TRIALS = 30  # round_up(len(SECRET_MESSAGE)*8/3)
    N_CHOICES = 33  # top_p
    A_TOTAL = 1.1
    B_TOTAL = 1.3

    selections = []
    for _ in range(N_TRIALS):
        vals = [random.random() for _ in range(N_CHOICES)]
        vals = sorted(vals, reverse=True)
        choices = {i:v for i,v in enumerate(vals)}
        exps = [math.exp(v) for v in choices.values()]
        sum_exps = sum(exps)
        sum_exps = sum_exps * random.uniform(A_TOTAL, B_TOTAL)
        selections.append({k: v / sum_exps for k, v in zip(choices.keys(), exps)})
    
    # check that all values in each dict sum to around 0.7 - 0.9
    # check = [sum(e.values()) for e in selections]
    # logger.debug(json.dumps(check, indent=2))
    # logger.debug(json.dumps(selections, indent=2))
    
    return selections

selections = build_selections()

### naive encode/decode algos ------

def encode(message: bytes, chunk_size: int = 3) -> List[str]:
    num_iters = math.ceil(len(message)*8/chunk_size)
    bits_message = "".join([format(_byte, "08b") for _byte in message])
    logger.debug(f"encode_bits: {bits_message}")
    int_message = []
    for i in range(num_iters):
        chunk_bits = bits_message[(i*chunk_size):(i*chunk_size)+chunk_size]
        chunk_int = int(chunk_bits, 2)
        int_message.append(chunk_int)
    enc_message = []
    for i in range(len(int_message)):
        enc_message.append( str(list(selections[i].keys())[int_message[i]]) )
    return enc_message


def decode(enc_message: List[str], chunk_size: int = 3) -> bytes:
    decoded_bits = ""
    for i, char in enumerate(enc_message):
        if (i == (len(enc_message)-1)) :
            current_chunk_size = 8 - (len(decoded_bits) % 8)
        else:
            current_chunk_size = chunk_size
        decoded_bits += format(int(char), f"0{current_chunk_size}b")
    logger.debug(f"decode_bits: {decoded_bits}")
    decoded_ints = []
    for i in range(len(decoded_bits) // 8):
        decoded_ints.append(int(decoded_bits[i*8:(i*8)+8], 2))
    return bytes(decoded_ints)

### print an example out

def example():
    msg = bytes([19,17])
    print("orig msg:", msg)
    msg_enc = encode(msg)
    print("msg_enc:", msg_enc)
    dec_msg = decode(msg_enc)
    print("dec_msg:", dec_msg)
    assert msg == dec_msg

if __name__ == "__main__":
    example()


### test section ------
import pytest

@pytest.mark.parametrize(
    "input_bytes, chunk_size",
    [
        (bytes([19,1,244]), 4),
        (bytes([19,1,244]), 3),
        (bytes([19,1,244]), 2),
        (bytes([19,1,244]), 1),
        (bytes([17,5]), 3),
        (bytes([17,5]), 2),
        (bytes([17,5]), 1),
        (bytes([255]), 1),
        (bytes([0]), 1),
    ],
)
def test_encode_decode(input_bytes, chunk_size):
    msg_enc = encode(input_bytes, chunk_size=chunk_size)
    logger.debug("msg_enc:", msg_enc)
    dec_msg = decode(msg_enc, chunk_size=chunk_size)
    logger.debug("dec_msg:", dec_msg)
    assert input_bytes == dec_msg    

