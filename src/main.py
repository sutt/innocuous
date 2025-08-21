import logging
import random
from llm.core import demo
from llm.core import (
    init_llm,
    infer_llm,
)
from llm.utils import (
    cvt_to_logprobs,
    to_json,
)
from stego.basic import (
    encode,
    decode,
)
from stego.utils import (
    filter_tok,
)
from btc.addr_codec import (
    decode_bitcoin_address,
)


DEBUG = True
logger = logging.getLogger(__name__)
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level, format="")


def main_encode(
    llm, 
    initial_prompt, 
    msg, 
    chunk_size, 
    num_logprobs,
    ):
    
    enc_ints = encode(msg, chunk_size=chunk_size)

    current_prompt = initial_prompt
    
    for enc_int in enc_ints:

        toks = infer_llm(llm, prompt=current_prompt, num_output=num_logprobs)

        logger.debug(to_json(cvt_to_logprobs(toks)))

        toks = filter_tok(toks)

        logger.debug(f"filter non-alpha: {num_logprobs} -> {len(toks)}")

        current_tok = list(toks.keys())[enc_int]

        logger.debug(f"enc_int: {enc_int} | token: {current_tok}")

        current_prompt += current_tok

    logger.info(f"final: {current_prompt}")

    return current_prompt

def main_decode(
    llm, 
    encoded_prompt, 
    initial_prompt, 
    chunk_size, 
    num_logprobs,
    ):
    message_carrying_text = encoded_prompt[len(initial_prompt):]

    current_prompt = initial_prompt
    decoded_ints = []
    remaining_text = message_carrying_text

    while remaining_text:
        toks = infer_llm(llm, prompt=current_prompt, num_output=num_logprobs)
        toks = filter_tok(toks)

        found_match = False
        for i, token_str in enumerate(toks.keys()):
            if remaining_text.startswith(token_str):
                decoded_int = i
                decoded_ints.append(decoded_int)

                current_prompt += token_str
                remaining_text = remaining_text[len(token_str):]
                found_match = True
                logger.debug(f"Found token: '{token_str}', index: {decoded_int}")
                break

        if not found_match:
            logger.error("Could not decode next token. Aborting.")
            logger.error(f"Remaining text: '{remaining_text}'")
            logger.error(f"Candidate tokens: {list(toks.keys())}")
            break

    logger.debug(f"decoded_ints: {decoded_ints}")

    decoded_msg = decode(decoded_ints, chunk_size=chunk_size)
    logger.info(f"decoded_msg: {decoded_msg}")

    return decoded_msg


def main():
    
    # original_msg = bytes([19,17])
    original_msg = bytes([random.randint(0,255) for e in range(20)])
    logger.info(f"encoded_msg: {original_msg}")

    chunk_size = 2
    initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king" 
    num_logprobs = 40

    llm = init_llm()
    
    encoded_prompt = main_encode(
        llm=llm,
        initial_prompt=initial_prompt,
        msg=original_msg,
        chunk_size=chunk_size,
        num_logprobs=num_logprobs,
    )
    
    decoded_msg = main_decode(
        llm=llm, 
        encoded_prompt=encoded_prompt, 
        initial_prompt=initial_prompt, 
        chunk_size=chunk_size, 
        num_logprobs=num_logprobs,
    )
    
    assert original_msg == decoded_msg


def example_addr():

    # https://mempool.space/address/12Wfw4L3oPJFk2q6osDoZLYAwdFkhvgt4E
    addr = "12Wfw4L3oPJFk2q6osDoZLYAwdFkhvgt4E"
    info = decode_bitcoin_address(addr)
    original_msg = bytes.fromhex(info["payload_hex"])
    logger.info(f"encoded_msg: {original_msg}")

    chunk_size = 2
    initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king" 
    num_logprobs = 40

    llm = init_llm()
    
    encoded_prompt = main_encode(
        llm=llm,
        initial_prompt=initial_prompt,
        msg=original_msg,
        chunk_size=chunk_size,
        num_logprobs=num_logprobs,
    )
    
    decoded_msg = main_decode(
        llm=llm, 
        encoded_prompt=encoded_prompt, 
        initial_prompt=initial_prompt, 
        chunk_size=chunk_size, 
        num_logprobs=num_logprobs,
    )
    
    assert original_msg == decoded_msg

def test_decode_branch():
    addr = "12Wfw4L3oPJFk2q6osDoZLYAwdFkhvgt4E"
    info = decode_bitcoin_address(addr)
    original_msg = bytes.fromhex(info["payload_hex"])
    chunk_size = 2
    initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king"
    num_logprobs = 40

    encoded_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king, a man of noble grace, did dwell in state within a towr that loomed above all other loft, where eagles, soaring free in azured heights would cast, in envied sight, a winking glace at him who ruled, and in his hand a golden rod of rule he held alight, with sceptered power to rule and right, and with"
    
    llm = init_llm()
    decoded_msg = main_decode(
        llm=llm, 
        encoded_prompt=encoded_prompt, 
        initial_prompt=initial_prompt, 
        chunk_size=chunk_size, 
        num_logprobs=num_logprobs,
    )
    
    assert original_msg == decoded_msg

if __name__ == "__main__":
    # main()
    # example_addr()
    test_decode_branch()
