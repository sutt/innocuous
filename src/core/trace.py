import logging
from llm import to_json


logger = logging.getLogger(__name__)


def _trace_encoding_step(step_name, **kwargs):
    """Single trace function for all encoding steps"""
    if not logger.isEnabledFor(logging.DEBUG):
        return
    
    trace_messages = {
        'tokens_processed': lambda: f"tokens: {to_json(kwargs['toks'])}",
        'pre_filter': lambda: f"pre_accept_filter: {kwargs['before']} -> {kwargs['after']}",
        'token_accepted': lambda: f"accept_tok hit: {repr(kwargs['token'])} | continuing...",
        'post_filter': lambda: f"post_accept_filter: {kwargs['before']} -> {kwargs['after']}",
        'token_selected': lambda: f"enc_int: {kwargs['enc_int']} | token: {repr(kwargs['token'])}",
        'encoding_complete': lambda: f"final: {kwargs['prompt']}"
    }
    
    if step_name in trace_messages:
        logger.debug(trace_messages[step_name]())


def _trace_decoding_step(step_name, **kwargs):
    """Single trace function for all decoding steps"""
    if not logger.isEnabledFor(logging.DEBUG):
        return
        
    trace_messages = {
        'decoding_complete': lambda: f"decoded_ints: {kwargs['decoded_ints']}",
        'decode_failed': lambda: "Failed to decode message."
    }
    
    if step_name in trace_messages:
        if step_name == 'decode_failed':
            logger.error(trace_messages[step_name]())
        else:
            logger.debug(trace_messages[step_name]())