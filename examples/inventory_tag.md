# A binary inventory tag in a weather bulletin

This example encodes four arbitrary bytes (`00 ff 2a 7e`) in a weather bulletin and recovers the exact bytes. In particular, the NUL and 0xff bytes demonstrate binary data rather than UTF-8 text. It uses the real encoder and decoder, not mocked token probabilities.

The checked-in JSON contains the complete original prompt, carrier text, settings, model checksum and library version. The generated continuation is:

> of the first day of winter brings an unusually cold day for our village. Expect clear weather for

The encoder stops when the payload is exhausted; the final sentence is intentionally unfinished. Do not edit the carrier or append punctuation before decoding. This demonstrates steganography, not encryption or guaranteed secrecy.

## Reproduce

Use Python 3.12, this repository on PYTHONPATH, and llama-cpp-python 0.3.18 with its dependencies. Obtain the Qwen2.5-0.5B-Instruct Q5_K_M GGUF from the [pinned official model revision](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/blob/9217f5db79a29953eb74d5343926648285ec7e67/qwen2.5-0.5b-instruct-q5_k_m.gguf). Its SHA-256 is `041474553fcabfc2a2d67903f9d2c2e50bd92528e670da4f33b5d0ce6e59fd55`. Model weights are not included.

From the repository root:

```sh
PYTHONPATH=. python examples/inventory_tag.py decode --model /path/to/qwen2.5-0.5b-instruct-q5_k_m.gguf
PYTHONPATH=. python examples/inventory_tag.py generate --model /path/to/qwen2.5-0.5b-instruct-q5_k_m.gguf --record /tmp/new-inventory-tag.json
```

Expected final line: `Recovered 4 bytes: 00ff2a7e (exact match)`.

Generation refuses to overwrite a record and only saves after exact recovery. Decode verifies the model checksum, library version and recorded settings. The script performs no downloads or network calls. Treat model/platform numerical differences as a possible reproduction limitation; do not silently change decoding settings.

Validation: generation plus immediate decoding and a separate-process decoding of the saved JSON both passed on Linux x86_64 CPU, Python 3.12.13, llama-cpp-python 0.3.18. Runs were isolated without network access. Base repository revision: `a60f5c6a036eda581d4a476559e349d68df5900b`.
