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

def main_encode():
    
    msg = bytes([19,17])
    # msg = bytes([19,17,99,0,3,230,62])
    # msg = bytes([random.randint(0,255) for e in range(20)])
    logger.debug(f"msg: {msg}")
    
    num_logprobs = 40
    chunk_size = 2
    
    enc_ints = encode(msg, chunk_size=chunk_size)

    llm = init_llm()
    current_prompt="Below is an iambic penatameter poem. Complete it:\nThe king" 
    
    for enc_int in enc_ints:

        toks = infer_llm(llm, prompt=current_prompt, num_output=num_logprobs)

        logger.debug(to_json(cvt_to_logprobs(toks)))

        toks = filter_tok(toks)

        logger.debug(f"filter non-alpha: {num_logprobs} -> {len(toks)}")

        current_tok = list(toks.keys())[enc_int]

        logger.debug(f"enc_int: {enc_int} | token: {current_tok}")

        current_prompt += current_tok

    logger.info(f"final: {current_prompt}")



if __name__ == "__main__":
    # llm_example()
    # stego_demo()
    main_encode()