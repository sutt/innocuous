import argparse
import logging
import sys
from pathlib import Path

from stego_llm import __version__
from stego_llm.core import main_decode, main_encode
from stego_llm.llm import check_llm

logger = logging.getLogger(__name__)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="LLM Steganography")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )
    parser.add_argument("--llm-path", type=Path, help="Path to LLM GGUF file")
    parser.add_argument(
        "--chunk_size", type=int, default=2, help="Chunk size for encoding/decoding"
    )
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
    decode_group.add_argument(
        "--file", type=Path, help="Path to file with message to decode"
    )

    # Check LLM command
    subparsers.add_parser("check-llm", help="Check LLM configuration")

    args = parser.parse_args()

    log_level = logging.WARNING
    if args.verbose == 1:
        log_level = logging.INFO
    elif args.verbose >= 2:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, stream=sys.stderr)

    initial_prompt = None
    if args.initial_prompt_text:
        initial_prompt = args.initial_prompt_text
    elif args.initial_prompt_file:
        initial_prompt = args.initial_prompt_file.read_text()

    # Hardcoded for now
    num_logprobs = 100
    if initial_prompt is None:
        initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king"

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

        encoded_message = main_encode(
            initial_prompt=initial_prompt,
            msg=message_bytes,
            chunk_size=args.chunk_size,
            num_logprobs=num_logprobs,
            llm_path=args.llm_path,
        )
        print(encoded_message)

    elif args.command == "decode":
        encoded_text = ""
        if args.message:
            encoded_text = args.message
        elif args.file:
            encoded_text = args.file.read_text()

        decoded_bytes = main_decode(
            encoded_prompt=encoded_text,
            initial_prompt=initial_prompt,
            chunk_size=args.chunk_size,
            num_logprobs=num_logprobs,
            llm_path=args.llm_path,
        )
        print(repr(decoded_bytes))

    elif args.command == "check-llm":
        check_llm(llm_path=args.llm_path, verbose=args.verbose >= 2)


if __name__ == "__main__":
    main()
