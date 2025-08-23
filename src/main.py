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
    pre_accept_filter,
    post_accept_filter,
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
    
    while len(enc_ints) != 0:

        toks = infer_llm(llm, prompt=current_prompt, num_output=num_logprobs)

        toks = cvt_to_logprobs(toks)
        logger.debug(to_json(toks))

        toks = filter_tok(toks)
        toks = pre_accept_filter(toks)
        logger.debug(f"pre_accept_filter: {num_logprobs} -> {len(toks)}")

        accepted_tok = accept_tok(toks)
        if accepted_tok is not None:
            current_prompt += accepted_tok
            logger.debug(f"accept_tok hit: {repr(accepted_tok)} | continuing...")
            continue

        _num_toks = len(toks)
        toks = post_accept_filter(toks)
        logger.debug(f"post_accept_filter: {_num_toks} -> {len(toks)}")

        enc_int = enc_ints.pop(0)
        current_tok = list(toks.keys())[enc_int]
        logger.debug(f"enc_int: {enc_int} | token: {repr(current_tok)}")
        current_prompt += current_tok

    logger.debug(f"final: {current_prompt}")

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
        toks = cvt_to_logprobs(toks)
        toks = filter_tok(toks)
        toks = pre_accept_filter(toks)

        accepted_tok = accept_tok(toks)
        if accepted_tok is not None:
            if remaining_text.startswith(accepted_tok):
                new_prompt = current_prompt + accepted_tok
                new_remaining = remaining_text[len(accepted_tok):]
                
                result = solve(new_prompt, new_remaining)
                memo[state] = result
                return result
            else:
                memo[state] = None
                return None

        toks = post_accept_filter(toks)
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
    
    # params -----
    # original_msg = bytes([255,255])
    # original_msg = bytes([0,0])
    original_msg = bytes([random.randint(0,255) for e in range(20)])
    
    addr = "12Wfw4L3oPJFk2q6osDoZLYAwdFkhvgt4E"
    info = decode_bitcoin_address(addr)
    original_msg = bytes.fromhex(info["payload_hex"])
    
    logger.info(f"encoded_msg: {original_msg}")

    chunk_size = 2
    num_logprobs = 40
    
    # standard inital prompt
    initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king" 
    
    # high prob word: (" land" 0.91)
    # initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king, whose power and pride, were known through the"
    
    # punctuation is top token: ("\n" 0.3)
    # initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king, whose power and pride, were known through the realms of earth to shine,"


    # main functions ----
    
    llm = init_llm()
    
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
    
    # must re-init llm here or decode fails for some reason
    # IMPORTANT: this can trigger OOM silent fail, in which case decode
    # and verify message match never runs and program exits as if succesful.
    llm = init_llm()
    
    decoded_msg = main_decode(
        llm=llm, 
        encoded_prompt=encoded_prompt, 
        initial_prompt=initial_prompt, 
        chunk_size=chunk_size, 
        num_logprobs=num_logprobs,
    )
    
    print(f"decoded_msg: {decoded_msg}")
    assert original_msg == decoded_msg
    print("\ndone. it worked!")


def example_decode_test():
    
    # params -----
    addr = "12Wfw4L3oPJFk2q6osDoZLYAwdFkhvgt4E"
    info = decode_bitcoin_address(addr)
    original_msg = bytes.fromhex(info["payload_hex"])
    
    logger.info(f"encoded_msg: {original_msg}")

    chunk_size = 2
    num_logprobs = 40
    
    initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king" 
    #TODO
    encoded_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king sat high upon his throne so grand,\nWith scepter in his hand, a look so bold,\nThe room did tremble in awe and stand,\nIn hushed reverence the tales were told,\nOf valor deeds and deeds of old so gold.\n\nBut as the sun began to wane away,\nHis subjects pleaded for their daily bread,\nHe sighed with weary heart and cast his gaze,\nUpon his treasurer who knelt to stay,\nTo share the news with him that he had read.\n\nThe treasures were depleted, gold had gone,\nNo more for"


    # main functions ----
    llm = init_llm()
    
    decoded_msg = main_decode(
        llm=llm, 
        encoded_prompt=encoded_prompt, 
        initial_prompt=initial_prompt, 
        chunk_size=chunk_size, 
        num_logprobs=num_logprobs,
    )
    
    print(f"decoded_msg: {decoded_msg}")
    assert original_msg == decoded_msg
    print("\ndone. it worked!")


if __name__ == "__main__":
    # example_random_msg()
    example_decode_test()
