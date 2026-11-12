"""Round-trip a four-byte sample inventory tag through an ordinary weather note.

Generate a verified JSON record, or decode that record in a fresh process.
No downloads or network calls are made by this example.
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path

from stego_llm import main_decode, main_encode

PROMPT = "Write a short, ordinary morning weather bulletin for a village newsletter. Use plain English prose.\nThe morning"
PAYLOAD = bytes.fromhex("00ff2a7e")
OPTIONS = {"n_ctx": 2048, "n_threads": 2, "n_batch": 128, "seed": 42, "verbose": False}
SAMPLE = Path(__file__).with_name("inventory_tag.json")


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("generate", "decode"))
    parser.add_argument("--model", required=True, type=Path, help="Existing local GGUF file")
    parser.add_argument("--record", type=Path, default=SAMPLE)
    args = parser.parse_args()
    model_hash = digest(args.model)
    version = importlib.metadata.version("llama-cpp-python")
    if args.mode == "generate":
        if args.record.exists():
            parser.error("record already exists; select a new --record path")
        encoded = main_encode(PROMPT, PAYLOAD, chunk_size=2, num_logprobs=100,
                              llm_path=str(args.model), llm_extra_args=OPTIONS)
        record = {"prompt": PROMPT, "encoded_prompt": encoded,
                  "payload_hex": PAYLOAD.hex(), "chunk_size": 2, "num_logprobs": 100,
                  "model_sha256": model_hash, "llama_cpp_python": version,
                  "llm_options": OPTIONS}
    else:
        record = json.loads(args.record.read_text(encoding="utf-8"))
        if record["model_sha256"] != model_hash:
            parser.error("model checksum differs from the recorded sample")
        if record["llama_cpp_python"] != version:
            parser.error("use the recorded llama-cpp-python version")
        if record["llm_options"] != OPTIONS or record["chunk_size"] != 2 or record["num_logprobs"] != 100:
            parser.error("record uses unsupported decoding settings")
        if not record["encoded_prompt"].startswith(record["prompt"]):
            parser.error("encoded text must start with its exact original prompt")
    decoded = main_decode(record["encoded_prompt"], record["prompt"], chunk_size=2,
                          num_logprobs=100, llm_path=str(args.model), llm_extra_args=OPTIONS)
    expected = bytes.fromhex(record["payload_hex"])
    if decoded != expected:
        raise SystemExit("Round-trip mismatch; no verified sample written")
    if args.mode == "generate":
        with args.record.open("x", encoding="utf-8") as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    print(record["encoded_prompt"][len(record["prompt"]):])
    print(f"Recovered {len(decoded)} bytes: {decoded.hex()} (exact match)")


if __name__ == "__main__":
    main()
