"""A local-model postcard with a recoverable UTF-8 message (issue #1).

From the repository root, after installing innocuous and downloading a GGUF:
  python examples/coded_postcard.py encode --model /path/to/model.gguf --output postcard.json
  python examples/coded_postcard.py decode --model /path/to/model.gguf --input postcard.json

The JSON preserves the exact carrier, prompt, settings and model fingerprint.
Keep its text unchanged; reflowing or editing it can prevent recovery. This is
a demonstration of steganography, not encryption or a place to store secrets.

The checked-in garden_postcard.json recovers MESSAGE using llama-cpp-python
0.3.16 (the version in uv.lock) and the official Qwen/Qwen2.5-0.5B-Instruct-GGUF file:
https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/9217f5db79a29953eb74d5343926648285ec7e67/qwen2.5-0.5b-instruct-q4_k_m.gguf
Its SHA-256 is recorded in the postcard. No model weights are bundled here.
The encoder stops as soon as the payload is embedded, so the final sentence
may be unfinished. Do not append a completion to the saved carrier.
"""

import argparse
import hashlib
import json
from importlib.metadata import version
from pathlib import Path

from stego_llm import main_decode, main_encode


PROMPT = "Write a friendly postcard about a quiet walk through a garden.\nDear friend,\n"
MESSAGE = "Hẹn ở vườn."
OPTIONS = {"n_ctx": 2048, "n_threads": 1, "n_gpu_layers": 0, "seed": 42, "verbose": False}
SETTINGS = {"chunk_size": 2, "num_logprobs": 100, "llm_extra_args": OPTIONS}


def model_sha256(model):
    with Path(model).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def decode_postcard(postcard, model):
    if not isinstance(postcard, dict) or postcard.get("format") != "innocuous-postcard-v1":
        raise ValueError("Unsupported postcard format")
    if postcard.get("settings") != SETTINGS:
        raise ValueError("This example requires its original encoding settings")
    prompt, carrier = postcard.get("prompt"), postcard.get("carrier")
    if not isinstance(prompt, str) or not prompt or not isinstance(carrier, str):
        raise ValueError("Postcard must contain a prompt and carrier text")
    if not carrier.startswith(prompt) or carrier == prompt:
        raise ValueError("Carrier must contain the exact initial prompt and generated text")
    if postcard.get("model_sha256") != model_sha256(model):
        raise ValueError("Use the same GGUF file that encoded this postcard")
    if postcard.get("llama_cpp_python") != version("llama-cpp-python"):
        raise ValueError("Use the recorded llama-cpp-python version for this postcard")
    recovered = main_decode(carrier, prompt, llm_path=str(model), **SETTINGS)
    if recovered is None:
        raise ValueError("The model could not recover this postcard")
    return recovered.decode("utf-8")


def encode_postcard(message, model):
    if not message:
        raise ValueError("Choose a nonempty message")
    payload = message.encode("utf-8")
    fingerprint = model_sha256(model)
    carrier = main_encode(PROMPT, payload, llm_path=str(model), **SETTINGS)
    postcard = {
        "format": "innocuous-postcard-v1",
        "model_sha256": fingerprint,
        "llama_cpp_python": version("llama-cpp-python"),
        "prompt": PROMPT,
        "carrier": carrier,
        "settings": SETTINGS,
    }
    if decode_postcard(postcard, model) != message:
        raise ValueError("Round trip failed; no postcard was saved")
    return postcard


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)
    encode = subparsers.add_parser("encode")
    encode.add_argument("--model", type=Path, required=True)
    encode.add_argument("--message", default=MESSAGE)
    encode.add_argument("--output", type=Path, required=True)
    decode = subparsers.add_parser("decode")
    decode.add_argument("--model", type=Path, required=True)
    decode.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "encode":
            postcard = encode_postcard(args.message, args.model)
            with args.output.open("x", encoding="utf-8") as stream:
                json.dump(postcard, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
            print(postcard["carrier"][len(PROMPT):])
        else:
            print(decode_postcard(json.loads(args.input.read_text(encoding="utf-8")), args.model))
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
