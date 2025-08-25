import argparse
import logging
import sys
from pathlib import Path

from stego_llm.core import main_decode, main_encode
from stego_llm.llm import create_llm_client

logger = logging.getLogger(__name__)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="LLM Steganography")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )
    parser.add_argument("--chunk_size", type=int, default=3, help="Chunk size for encoding/decoding")
    prompt_group = parser.add_mutually_exclusive_group()
    prompt_group.add_argument(
        "--initial-prompt-text", type=str, help="Initial prompt text"
    )
    prompt_group.add_argument(
        "--initial-prompt-file", type=Path, help="Path to initial prompt file"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encode command
    encode_parser = subparsers.add_parser("encode", help="Encode a message")
    encode_group = encode_parser.add_mutually_exclusive_group(required=True)
    encode_group.add_argument("--text", type=str, help="ASCII text to encode")
    encode_group.add_argument("--bytes", type=str, help="Hex byte data to encode")
    encode_group.add_argument("--btc-addr", type=str, help="Bitcoin address to encode")

    # Decode command
    decode_parser = subparsers.add_parser("decode", help="Decode a message")
    decode_group = decode_parser.add_mutually_exclusive_group(required=True)
    decode_group.add_argument("--message", type=str, help="Message to decode")
    decode_group.add_argument("--file", type=Path, help="Path to file with message to decode")

    args = parser.parse_args()

    log_level = logging.WARNING
    if args.verbose == 1:
        log_level = logging.INFO
    elif args.verbose >= 2:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, stream=sys.stderr)

    initial_prompt = "you are a helpful assistant."
    if args.initial_prompt_text:
        initial_prompt = args.initial_prompt_text
    elif args.initial_prompt_file:
        initial_prompt = args.initial_prompt_file.read_text()

    # Hardcoded for now, as per file summaries
    num_logprobs = 100

    if args.command == "encode":
        message_bytes = b""
        if args.text:
            message_bytes = args.text.encode("utf-8")
        elif args.bytes:
            try:
                message_bytes = bytes.fromhex(args.bytes)
            except ValueError:
                parser.error("Invalid hex string for --bytes")
        elif args.btc_addr:
            message_bytes = args.btc_addr.encode("utf-8")

        llm = create_llm_client()
        encoded_message = main_encode(
            llm=llm,
            initial_prompt=initial_prompt,
            msg=message_bytes,
            chunk_size=args.chunk_size,
            num_logprobs=num_logprobs,
        )
        print(encoded_message)

    elif args.command == "decode":
        encoded_text = ""
        if args.message:
            encoded_text = args.message
        elif args.file:
            encoded_text = args.file.read_text()

        llm = create_llm_client()
        decoded_bytes = main_decode(
            llm=llm,
            encoded_prompt=encoded_text,
            initial_prompt=initial_prompt,
            chunk_size=args.chunk_size,
            num_logprobs=num_logprobs,
        )
        print(repr(decoded_bytes))


if __name__ == "__main__":
    main()
