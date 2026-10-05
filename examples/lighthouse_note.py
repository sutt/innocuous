"""Generate or verify a real Innocuous message hidden in a seaside note.

From the repository root, after installing the package:
    python -m examples.lighthouse_note --llm-path /path/to/model.gguf
    python -m examples.lighthouse_note --llm-path /path/to/model.gguf --generate
"""

import argparse
import hashlib
import json
import logging
from pathlib import Path

from llama_cpp import __version__ as llama_cpp_version
from stego_llm import main_decode, main_encode


MODEL_URL = (
    "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/"
    "qwen2.5-0.5b-instruct-q5_k_m.gguf"
)
MODEL_SHA256 = "041474553fcabfc2a2d67903f9d2c2e50bd92528e670da4f33b5d0ce6e59fd55"
SAMPLE_PATH = Path(__file__).with_suffix(".json")
MESSAGE = "meet at dawn"
INITIAL_PROMPT = (
    "<|im_start|>user\n"
    "Continue a friendly seaside walking note in plain English. Describe the "
    "lighthouse, the path, gulls, the weather, and a flask of tea.\n"
    "<|im_end|>\n<|im_start|>assistant\n"
    "This morning, I followed the path toward the lighthouse"
)
LLM_OPTIONS = {
    "n_ctx": 2048,
    "n_threads": 4,
    "n_gpu_layers": 0,
    "seed": 0,
    "verbose": False,
}


def check_model(model_path: Path) -> None:
    """Check the exact GGUF bytes used for the committed example."""
    with model_path.open("rb") as model_file:
        actual = hashlib.file_digest(model_file, "sha256").hexdigest()
    if actual != MODEL_SHA256:
        raise ValueError("Model SHA-256 does not match the example's GGUF file.")


def generate(model_path: Path) -> dict:
    # main_encode returns the initial prompt followed by the generated text.
    encoded = main_encode(
        initial_prompt=INITIAL_PROMPT,
        msg=MESSAGE.encode("utf-8"),
        chunk_size=2,
        num_logprobs=100,
        llm_path=str(model_path),
        llm_extra_args=LLM_OPTIONS.copy(),
    )
    return {
        "model_url": MODEL_URL,
        "model_sha256": MODEL_SHA256,
        "llama_cpp_python_version": llama_cpp_version,
        "initial_prompt": INITIAL_PROMPT,
        "carrier_text": encoded[len(INITIAL_PROMPT):],
        "message": MESSAGE,
        "chunk_size": 2,
        "num_logprobs": 100,
        "llm_extra_args": LLM_OPTIONS.copy(),
    }


def decode(sample: dict, model_path: Path) -> bytes:
    # The decoder needs the exact prompt, not only the visible carrier text.
    recovered = main_decode(
        encoded_prompt=sample["initial_prompt"] + sample["carrier_text"],
        initial_prompt=sample["initial_prompt"],
        chunk_size=sample["chunk_size"],
        num_logprobs=sample["num_logprobs"],
        llm_path=str(model_path),
        llm_extra_args=sample["llm_extra_args"].copy(),
    )
    if recovered != sample["message"].encode("utf-8"):
        raise ValueError(
            f"Round trip failed: recovered {recovered!r}. Use the recorded "
            "model, llama-cpp-python version, and CPU settings."
        )
    return recovered


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--llm-path", type=Path, required=True)
    parser.add_argument("--generate", action="store_true", help="Encode a new sample")
    parser.add_argument("--sample", type=Path, default=SAMPLE_PATH)
    args = parser.parse_args()
    logging.getLogger("stego_llm").setLevel(logging.WARNING)
    check_model(args.llm_path)

    sample = generate(args.llm_path) if args.generate else json.loads(
        args.sample.read_text(encoding="utf-8")
    )
    recovered = decode(sample, args.llm_path)
    if args.generate:
        # Keep failed or unverified generations out of the saved example.
        args.sample.write_text(json.dumps(sample, indent=2) + "\n", encoding="utf-8")

    print(sample["initial_prompt"].rsplit("\n", 1)[-1] + sample["carrier_text"])
    print(f"Recovered message: {recovered!r}")


if __name__ == "__main__":
    main()
