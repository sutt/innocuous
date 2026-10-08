"""Generate or independently decode a postcard with an embedded UTF-8 message.

Run from an installed repository: python examples/postcard.py --help
"""
import argparse
import hashlib
import json
from importlib.metadata import version
from pathlib import Path

from stego_llm import main_decode, main_encode

VISIBLE_PREFIX = "Dear friend,\nThe old station"
PROMPT = (
    "Continue this friendly postcard about a visit to a small railway museum. "
    "Use ordinary descriptive prose, without a title or a sign-off.\n"
    + VISIBLE_PREFIX
)
MESSAGE = "bring tea ☕"
OPTIONS = {"n_ctx": 2048, "n_batch": 64, "n_threads": 1,
           "n_gpu_layers": 0, "seed": 123, "verbose": False}
SAMPLE = Path(__file__).resolve().parents[1] / "docs/showcase/postcard.json"


def model_digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def decode_sample(sample, model):
    """Decode the actual carrier, then compare bytes with the demonstration payload."""
    if model_digest(model) != sample["model_sha256"]:
        raise ValueError("Model SHA-256 differs from the recorded sample")
    installed = version("llama-cpp-python")
    if installed != sample["llama_cpp_python"]:
        raise ValueError(f"Use llama-cpp-python=={sample['llama_cpp_python']}; got {installed}")
    recovered = main_decode(
        encoded_prompt=sample["initial_prompt"] + sample["carrier_text"],
        initial_prompt=sample["initial_prompt"],
        chunk_size=sample["chunk_size"],
        num_logprobs=sample["num_logprobs"],
        llm_path=str(model), llm_extra_args=sample["llm_options"],
    )
    expected = sample["message"].encode("utf-8")
    if recovered != expected:
        raise ValueError(f"Round trip failed: expected {expected!r}, recovered {recovered!r}")
    return recovered.decode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True, help="Local GGUF model file")
    parser.add_argument("--generate", type=Path, metavar="OUTPUT_JSON",
                        help="Generate and verify a new sample; refuses to overwrite files")
    parser.add_argument("--sample", type=Path, default=SAMPLE,
                        help="Recorded sample to decode (default: bundled postcard)")
    args = parser.parse_args()
    if args.generate:
        if args.generate.exists():
            parser.error(f"Output already exists: {args.generate}")
        sample = {
            "initial_prompt": PROMPT, "visible_prefix": VISIBLE_PREFIX, "message": MESSAGE,
            "model_filename": args.model.name,
            "model_sha256": model_digest(args.model),
            "llama_cpp_python": version("llama-cpp-python"),
            "chunk_size": 2, "num_logprobs": 100, "llm_options": OPTIONS,
        }
        encoded = main_encode(
            initial_prompt=PROMPT, msg=MESSAGE.encode("utf-8"),
            chunk_size=sample["chunk_size"], num_logprobs=sample["num_logprobs"],
            llm_path=str(args.model), llm_extra_args=OPTIONS,
        )
        sample["carrier_text"] = encoded[len(PROMPT):]
        recovered = decode_sample(sample, args.model)
        # Commit a sample only after the actual LLM decoder recovers every byte.
        with args.generate.open("x", encoding="utf-8") as stream:
            json.dump(sample, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    else:
        sample = json.loads(args.sample.read_text(encoding="utf-8"))
        recovered = decode_sample(sample, args.model)
    print(sample.get("visible_prefix", "") + sample["carrier_text"])
    print(f"\nRecovered UTF-8 message: {recovered!r}")


if __name__ == "__main__":
    main()
