import logging
from stego_llm.steganography import (
    chunks_to_message,
    find_acceptable_token,
    pre_selection_filter,
    post_selection_filter,
)
from stego_llm.llm import get_token_probabilities, logits_to_probabilities
from .trace import _trace_decoding_step


logger = logging.getLogger(__name__)


def main_decode(
    llm,
    encoded_prompt,
    initial_prompt,
    chunk_size,
    num_logprobs,
):
    """Main decoding function for steganographic message extraction."""
    message_carrying_text = encoded_prompt[len(initial_prompt):]
    memo = {}

    def solve(current_prompt, remaining_text):
        if not remaining_text:
            return []

        state = (current_prompt, remaining_text)
        if state in memo:
            return memo[state]

        toks = get_token_probabilities(llm, prompt=current_prompt, num_output=num_logprobs)
        toks = logits_to_probabilities(toks)
        toks = pre_selection_filter(toks)

        accepted_tok = find_acceptable_token(toks)
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

        toks = post_selection_filter(toks)
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
        _trace_decoding_step('decode_failed')
        return None

    _trace_decoding_step('decoding_complete', decoded_ints=decoded_ints)

    decoded_msg = chunks_to_message(decoded_ints, chunk_size=chunk_size)
    logger.info(f"decoded_msg: {decoded_msg}")

    return decoded_msg