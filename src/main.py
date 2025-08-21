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
    accept_tok,
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
    
    # for enc_int in enc_ints:
    while len(enc_ints) != 0:

        toks = infer_llm(llm, prompt=current_prompt, num_output=num_logprobs)

        logger.debug(to_json(cvt_to_logprobs(toks)))

        toks = filter_tok(toks)

        logger.debug(f"filter non-alpha: {num_logprobs} -> {len(toks)}")

        accepted_tok = accept_tok(toks)
        if accepted_tok is not None:
            current_prompt += accepted_tok
            logger.debug(f"accept_tok hit: {repr(accepted_tok)} | continuing...")
            continue

        enc_int = enc_ints.pop(0)

        current_tok = list(toks.keys())[enc_int]

        logger.debug(f"enc_int: {enc_int} | token: {repr(current_tok)}")

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
    memo = {}

    def solve(current_prompt, remaining_text):
        if not remaining_text:
            return []

        state = (current_prompt, remaining_text)
        if state in memo:
            return memo[state]

        toks = infer_llm(llm, prompt=current_prompt, num_output=num_logprobs)
        toks = filter_tok(toks)

        possible_matches = []
        
        num_candidate_toks = 2**chunk_size
        candidate_toks = list(toks.keys())
        
        if len(candidate_toks) < num_candidate_toks:
            logger.warning(f"Not enough tokens after filtering. Have {len(candidate_toks)}, need {num_candidate_toks}")
            num_candidate_toks = len(candidate_toks)

        candidate_toks_slice = candidate_toks[:num_candidate_toks]

        for i, token_str in enumerate(candidate_toks_slice):
            if remaining_text.startswith(token_str):
                possible_matches.append((i, token_str))
        
        possible_matches.sort(key=lambda x: len(x[1]), reverse=True)

        for decoded_int, token_str in possible_matches:
            new_prompt = current_prompt + token_str
            new_remaining = remaining_text[len(token_str):]
            
            result = solve(new_prompt, new_remaining)

            if result is not None:
                solution = [decoded_int] + result
                memo[state] = solution
                return solution
        
        memo[state] = None
        return None

    decoded_ints = solve(initial_prompt, message_carrying_text)

    if decoded_ints is None:
        logger.error("Failed to decode message.")
        return None

    logger.debug(f"decoded_ints: {decoded_ints}")

    decoded_msg = decode(decoded_ints, chunk_size=chunk_size)
    logger.info(f"decoded_msg: {decoded_msg}")

    return decoded_msg


def example_random_msg():
    
    original_msg = bytes([255,255])
    # original_msg = bytes([0,0])
    # original_msg = bytes([random.randint(0,255) for e in range(20)])
    logger.info(f"encoded_msg: {original_msg}")

    chunk_size = 3
    num_logprobs = 40
    
    # standard inital prompt
    # initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king" 
    
    # high prob word: (" land" 0.91)
    # initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king, whose power and pride, were known through the"
    
    # punctuation is top token: ("\n" 0.3)
    initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king, whose power and pride, were known through the realms of earth to shine,"

    llm = init_llm()
    
    encoded_prompt = main_encode(
        llm=llm,
        initial_prompt=initial_prompt,
        msg=original_msg,
        chunk_size=chunk_size,
        num_logprobs=num_logprobs,
    )
    print("done with encode...")
    # must re-init llm here or decode fails for some reason
    llm = init_llm()
    print("starting decode...")
    
    decoded_msg = main_decode(
        llm=llm, 
        encoded_prompt=encoded_prompt, 
        initial_prompt=initial_prompt, 
        chunk_size=chunk_size, 
        num_logprobs=num_logprobs,
    )
    
    print(f"decoded_msg: {decoded_msg}")
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

    # must re-init llm here of decode fails for some reason
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
    example_random_msg()
    # example_addr()
