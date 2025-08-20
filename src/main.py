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
    filter_non_alpha,
    filter_tok,
)


DEBUG = True
logger = logging.getLogger(__name__)
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level, format="")


def llm_example():
    demo()

def stego_demo():
    msg = bytes([19,17])
    print("orig msg:", msg)
    msg_enc = encode(msg)
    print("msg_enc:", msg_enc)
    msg_enc_t = [str(e) for e in msg_enc]
    dec_msg = decode(msg_enc)
    print("dec_msg:", dec_msg)
    assert msg == dec_msg

def main_encode(llm):
    
    msg = bytes([19,17])
    # msg = bytes([19,17,99,0,3,230,62])
    # msg = bytes([random.randint(0,255) for e in range(20)])
    logger.debug(f"msg: {msg}")
    
    num_logprobs = 40
    chunk_size = 2
    
    enc_ints = encode(msg, chunk_size=chunk_size)

    initial_prompt="Below is an iambic penatameter poem. Complete it:\nThe king" 
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

    return current_prompt, initial_prompt, msg, chunk_size, num_logprobs

def main_decode(llm, encoded_prompt, initial_prompt, original_msg, chunk_size, num_logprobs):
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

    assert original_msg == decoded_msg


if __name__ == "__main__":
    # llm_example()
    # stego_demo()
    llm = init_llm()
    encoded_prompt, initial_prompt, msg, chunk_size, num_logprobs = main_encode(llm)
    main_decode(llm, encoded_prompt, initial_prompt, msg, chunk_size, num_logprobs)
