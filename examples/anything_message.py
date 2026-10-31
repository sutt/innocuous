"""Example: hide an arbitrary UTF-8 message inside a bulletin-board note.

Closes the README TODO ("add one more example ... where message is
'the message could be anything'").

Reproduce (CPU only, ~1 minute):

    # 1. a small public model (~490 MB)
    curl -L -o qwen2.5-0.5b-instruct-q4_k_m.gguf \
      https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf
    # 2. run
    INNOCUOUS_LLM_PATH=./qwen2.5-0.5b-instruct-q4_k_m.gguf python examples/anything_message.py

Verified with llama-cpp-python 0.3.36 (CPU wheel), Python 3.13. The encoded
text below was produced by this script and decodes back to the message;
other models/quantizations will generate different (but equally decodable)
text.
"""

from stego_llm import main_encode, main_decode

INITIAL_PROMPT = (
    "Write a short, cheerful note a neighbor might leave on a community "
    "bulletin board:\n"
)
MESSAGE = b"the message could be anything"
CHUNK_SIZE = 3
NUM_LOGPROBS = 100

# Output observed with qwen2.5-0.5b-instruct-q4_k_m.gguf (deterministic across runs)
EXPECTED_TEXT = (
    "Hello there everyone at your convenience we would like to take a moment "
    "to thank you for sharing such lovely memories here and in many different "
    "places all throughout our lives. It brings back many wonderful experiences "
    "and reminds us of those that made life such as the love of nature that we "
    "now have for our neighbor John from a previous community who has lived for "
    "more than twenty years but who now passed away in January and we still "
    "have such lovely memories to hold and cherish"
)


def main():
    encoded_prompt = main_encode(
        initial_prompt=INITIAL_PROMPT,
        msg=MESSAGE,
        chunk_size=CHUNK_SIZE,
        num_logprobs=NUM_LOGPROBS,
    )
    carrier = encoded_prompt[len(INITIAL_PROMPT):]
    print("### carrier text:\n" + carrier)

    decoded = main_decode(
        encoded_prompt=encoded_prompt,
        initial_prompt=INITIAL_PROMPT,
        chunk_size=CHUNK_SIZE,
        num_logprobs=NUM_LOGPROBS,
    )
    print(f"\n### decoded: {decoded!r}")
    assert decoded == MESSAGE, "round trip failed"
    if carrier == EXPECTED_TEXT:
        print("matches the documented example text")
    print("done. it worked!")


if __name__ == "__main__":
    main()
