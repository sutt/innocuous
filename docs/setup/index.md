# Installing `llama-cpp-python` with custom build
_October 4, 2025_

> [!IMPORTANT]
> **Currently looks only CPU-only builds**

### Overview

When `llama-cpp-python` is installed it downloads the C/C++ source files and builds the llama.cpp binary for the computer's architecture. Since llama.cpp is an attempt to build a fast inference engine it utilizes the full suite of CPU optimizations available to the target machine. But different machine have different CPU versions, which have different optimizations and due to to floating point arithmetic, this will cause discrepencies in the logits which in rare cases cause a different ordering of top tokens at an iterations which cause the encoding/decoding algorithm to fall-out of sync between machines running different CPU's.

However this can be controlled by specifying a standardized build across all CPU architectures. This document describes why these occur and how to debug and setup, and force an install of the correct build version. Ideally this should all work automatically when you install with **uv** but this will take

### Project installer: `pyproject.toml`

Innocuous expects [**uv**](https://docs.astral.sh/uv/getting-started/installation/) for package installs and has custom insturctions for installing/building llama-cpp-python. To utilize the custom build instructions you need **uv** version `>= 0.8.1` to recognize `[tool.uv.config-settings-package]`.

### Resources

#### [check_drift.py](./check_drift.py)

Run `uv run docs/setup/check_drift.py` and you should get:
```
sha256 full_logits: 69a1a31fb9af2b67f7953b3614e6e04fa8147033a3029bdcb8d004dbaf713f25
Sha of logits matches! Your llama.cpp is configured properly.
```

If you don't use the next script...

**Note:** this script expects the model to be **mistral-7b-instruct-v0.2.Q4_K_M.gguf**. You can check if you have the right version by running:

```bash
sha256sum mistral-7b-instruct-v0.2.Q4_K_M.gguf
# expected output:
# 3e0039fd0273fcbebb49228943b17831aadd55cbcbf56f0af00499be2040ccf9
```

If you don't have a match here, you'll want to get this exact weights file and re-run the script to check if you have a match.

#### [custom-install.sh](./custom-install.sh)

If you don't have a match from `check_drift.py` you should use this script to pass `--config-settings` flags to the builder and 

Running `custom-install.sh` should produce a build log to stderr / stdout which can be checked against a reference build logs for discrepancies.

**Note:** you'll need the correct build tools for this to work. If you don't have it run:

```bash
sudo apt update
sudo apt install -y build-essential cmake ninja-build pkg-config python3-dev libopenblas-dev
```


### More details
- SIMD instructions + non-associative addition
- `python -c "from llama_cpp import *; print(llama_print_system_info())"`
    - `b'CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 | '`
- Unfortunately, these custom instructions reduce the CPU optimizations, and thus make inference often 2-3x slower than they would be otherwise.