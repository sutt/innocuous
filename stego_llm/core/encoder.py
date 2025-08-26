import logging
from stego_llm.steganography import (
    message_to_chunks,
    find_acceptable_token,
    pre_selection_filter,
    post_selection_filter,
)
from stego_llm.llm import (
    create_llm_client,
    get_token_probabilities,
    logits_to_probabilities,
)
from .trace import _trace_encoding_step


logger = logging.getLogger(__name__)


def main_encode(
    initial_prompt,
    msg,
    chunk_size,
    num_logprobs,
    llm_path=None,
):
    """Main encoding function for steganographic text generation."""
    llm = create_llm_client(model_path=llm_path)
    enc_ints = message_to_chunks(msg, chunk_size=chunk_size)
    current_prompt = initial_prompt

    while len(enc_ints) != 0:
        toks = get_token_probabilities(
            llm, prompt=current_prompt, num_output=num_logprobs
        )
        toks = logits_to_probabilities(toks)
        _trace_encoding_step("tokens_processed", toks=toks)

        toks = pre_selection_filter(toks)
        _trace_encoding_step("pre_filter", before=num_logprobs, after=len(toks))

        accepted_tok = find_acceptable_token(toks)
        if accepted_tok is not None:
            _trace_encoding_step("token_accepted", token=accepted_tok)
            current_prompt += accepted_tok
            continue

        _num_toks = len(toks)
        toks = post_selection_filter(toks)
        _trace_encoding_step("post_filter", before=_num_toks, after=len(toks))

        enc_int = enc_ints.pop(0)
        current_tok = list(toks.keys())[enc_int]
        _trace_encoding_step("token_selected", enc_int=enc_int, token=current_tok)
        current_prompt += current_tok

    _trace_encoding_step("encoding_complete", prompt=current_prompt)
    return current_prompt
