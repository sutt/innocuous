import logging
import random
from stego_llm import main_encode, main_decode
from stego_llm.llm import create_llm_client


DEBUG = True
logger = logging.getLogger(__name__)
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level, format="")


def example_custom_prompts():
    """Example showing different initial prompts for steganography."""

    # Parameters
    original_msg = bytes([random.randint(0, 255) for _ in range(10)])
    chunk_size = 3
    num_logprobs = 40

    logger.info(f"encoded_msg: {original_msg}")

    # Different prompt styles
    prompts = {
        "iambic": "Below is an iambic penatameter poem. Complete it:\nThe king",
        "high_prob": "Below is an iambic penatameter poem. Complete it:\nThe king, whose power and pride, were known through the",
        "punctuation": "Below is an iambic penatameter poem. Complete it:\nThe king, whose power and pride, were known through the realms of earth to shine,",
        "story": "Once upon a time, in a kingdom far away, there lived a",
        "technical": "The algorithm processes data by first analyzing the input and then",
    }

    llm = create_llm_client()

    for prompt_name, initial_prompt in prompts.items():
        print(f"\n=== Testing with {prompt_name} prompt ===")
        print(f"Initial prompt: {repr(initial_prompt)}")

        encoded_prompt = main_encode(
            llm=llm,
            initial_prompt=initial_prompt,
            msg=original_msg,
            chunk_size=chunk_size,
            num_logprobs=num_logprobs,
        )

        print(f"Generated text: {encoded_prompt[len(initial_prompt) :]}")
        print(f"Full length: {len(encoded_prompt)} characters")

        # Test decoding
        llm = create_llm_client()  # Re-init for decoding

        decoded_msg = main_decode(
            llm=llm,
            encoded_prompt=encoded_prompt,
            initial_prompt=initial_prompt,
            chunk_size=chunk_size,
            num_logprobs=num_logprobs,
        )

        success = original_msg == decoded_msg
        print(f"Decoding {'SUCCESS' if success else 'FAILED'}")

        if not success:
            print(f"Original:  {original_msg}")
            print(f"Decoded:   {decoded_msg}")


if __name__ == "__main__":
    example_custom_prompts()
