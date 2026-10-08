# A railway postcard with a hidden UTF-8 message

This example hides `bring tea ☕` in an ordinary postcard about a railway museum.
The payload is encoded as UTF-8 bytes, including the three-byte coffee symbol.
The carrier and the exact decoding settings are saved in [postcard.json](postcard.json).

The [example script](../../examples/postcard.py) calls the real `main_encode` and
`main_decode` functions. It writes a generated sample only after the decoder
recovers every original byte. Its default mode independently decodes the saved
sample; it does not regenerate the text or return the stored expected message.

## Recorded postcard

> Dear friend,
> The old station building has been transformed into a charming railway museum with an extensive collection of historic steam engines that have traveled from around the world. Visitors can learn about the fascinating history of railways from the perspective of the engineers and the people who have built them for over one hundred years. The museum also features exhibits on the history of the railroad industry as well as the development of new technologies and innovations that have shaped the industry today. It

The final `It` is the actual end of generation; the payload was fully encoded.

## Reproduce the saved sample

From a repository checkout, install the package and the recorded backend version:

```bash
python -m pip install . 'llama-cpp-python==0.3.16'
curl -fL -o qwen2.5-0.5b-instruct-q5_k_m.gguf \
  https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/9217f5db79a29953eb74d5343926648285ec7e67/qwen2.5-0.5b-instruct-q5_k_m.gguf
python examples/postcard.py --model qwen2.5-0.5b-instruct-q5_k_m.gguf
```

Model: [Qwen2.5-0.5B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF),
file `qwen2.5-0.5b-instruct-q5_k_m.gguf` (522,186,592 bytes).
SHA-256:

```text
041474553fcabfc2a2d67903f9d2c2e50bd92528e670da4f33b5d0ce6e59fd55
```

The script verifies the model hash and backend version before decoding. It uses
CPU inference with one thread and the settings recorded in the JSON. A different
model or backend can rank candidate tokens differently, so an arbitrary GGUF is
not interchangeable with the recorded model. The file is downloaded separately;
no model weights are committed to this repository.

## Generate another postcard

```bash
python examples/postcard.py --model qwen2.5-0.5b-instruct-q5_k_m.gguf \
  --generate my-postcard.json
python examples/postcard.py --model qwen2.5-0.5b-instruct-q5_k_m.gguf \
  --sample my-postcard.json
```

Generation refuses to overwrite an existing file. Edit `MESSAGE` or `PROMPT` in
the script to try another payload or cover story, then generate a new file. Both
the exact prompt and settings travel with that file. Preserve the carrier's
whitespace and punctuation: editing it can prevent recovery. Encoding stops when
the payload is exhausted, so the text can end mid-sentence; do not append a
fictional ending to the saved carrier.

The JSON includes the plaintext so readers can check this demonstration. It is
not a private message container, and steganography alone does not encrypt data.
