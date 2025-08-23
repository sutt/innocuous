"""
Basic package demonstration - minimal example showing main functionality.
This is kept in the package for documentation/demo purposes.
"""

import logging
from stego_llm import main_encode, main_decode
from stego_llm.llm import create_llm_client

# Simple logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def basic_demo():
    """Minimal demo of encode/decode functionality."""
    # Simple test message
    test_message = b"Hello, World!"
    
    # Basic parameters
    chunk_size = 2
    num_logprobs = 20
    initial_prompt = "Once upon a time"
    
    logger.info(f"Encoding message: {test_message}")
    
    # Initialize LLM
    llm = create_llm_client()
    
    # Encode
    encoded_text = main_encode(
        llm=llm,
        initial_prompt=initial_prompt,
        msg=test_message,
        chunk_size=chunk_size,
        num_logprobs=num_logprobs,
    )
    
    print(f"Generated text: {encoded_text}")
    
    # Decode
    llm = create_llm_client()  # Re-init for decoding
    
    decoded_message = main_decode(
        llm=llm,
        encoded_prompt=encoded_text,
        initial_prompt=initial_prompt,
        chunk_size=chunk_size,
        num_logprobs=num_logprobs,
    )
    
    # Verify
    success = test_message == decoded_message
    print(f"Decoding {'SUCCESS' if success else 'FAILED'}")
    
    if success:
        logger.info("Demo completed successfully!")
    else:
        logger.error(f"Failed: {test_message} != {decoded_message}")


if __name__ == "__main__":
    basic_demo()