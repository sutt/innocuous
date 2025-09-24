# Dev Summary

## v0.2.3

#### `extra-args-test.md`
- **Spec Summary:** *Add 1-2 tests for llm_extra_args feature. Test that args pass through encode/decode to constructors without real inference. Example usage: llm_extra_args={"n_ctx": 1024}. Mock instantiation/loading.*
- **Commit Message:** *test: add tests for llm_extra_args passthrough*
- **Task Notes:** Simple task, not best execution.
- **Src Diffs:** +0/-0 | **Test Diffs:** +29/-0
- **Spec:** extra-args-test.md | **Patch Sha:** 9abdb61
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
Add 1-2 tests for the following feature add in the commit.
For an example you use llm_extra_args={"n_ctx": 1024}
Do not create a slow test that requires real inference.
Simply test that the arg is being called through the encode/decode into the constructors but don't actually instantiate / load the weights.

```diff
commit 97819177e506c0bbfc3774b47d7b06be37a4438d
Author: sutt <wsutton17@gmail.com>
Date:   Thu Sep 11 11:53:30 2025 -0400

    feat: adding llm_extra_args for use in library functions

diff --git a/stego_llm/core/decoder.py b/stego_llm/core/decoder.py
index e9cd0de..857cf02 100644
--- a/stego_llm/core/decoder.py
+++ b/stego_llm/core/decoder.py
@@ -1,5 +1,5 @@
 import logging
-from typing import Optional
+from typing import Optional, Dict, Any
 from stego_llm.steganography import (
     chunks_to_message,
     find_acceptable_token,
@@ -24,6 +24,7 @@ def main_decode(
     chunk_size: int = 2,
     num_logprobs: int = 100,
     llm_path: Optional[str] = None,
+    llm_extra_args: Dict[str, Any] = {}
 ) -> Optional[bytes]:
     """Decodes a message hidden in a text.
 
@@ -38,6 +39,7 @@ def main_decode(
         num_logprobs (int): The number of token probabilities to consider.
         llm_path (Optional[str]): The path to the language model file.
             If None, the default model is used.
+        llm_extra_args (Optional Dict): additional args to pass to llama_cpp constructor.
 
     Returns:
         Optional[bytes]: The decoded message as bytes, or None if decoding fails.
diff --git a/stego_llm/core/encoder.py b/stego_llm/core/encoder.py
index fb4b0e0..b4b3bf1 100644
--- a/stego_llm/core/encoder.py
+++ b/stego_llm/core/encoder.py
@@ -1,5 +1,5 @@
 import logging
-from typing import Optional
+from typing import Optional, Dict, Any
 from stego_llm.steganography import (
     message_to_chunks,
     find_acceptable_token,
@@ -23,6 +23,7 @@ def main_encode(
     chunk_size: int = 2,
     num_logprobs: int = 100,
     llm_path: Optional[str] = None,
+    llm_extra_args: Dict[str, Any] = {}
 ) -> str:
     """Encodes a message into a text using steganography.
 
@@ -37,11 +38,12 @@ def main_encode(
         num_logprobs (int): The number of next-token probabilities to request from the LLM.
         llm_path (Optional[str]): The path to the language model file.
             If None, the default model is used.
+        llm_extra_args (Optional Dict): additional args to pass to llama_cpp constructor.
 
     Returns:
         str: The generated text with the message embedded within it.
     """
-    llm = create_llm_client(model_path=llm_path)
+    llm = create_llm_client(model_path=llm_path, **llm_extra_args)
     enc_ints = message_to_chunks(msg, chunk_size=chunk_size)
     current_prompt = initial_prompt
 
diff --git a/stego_llm/llm/interface.py b/stego_llm/llm/interface.py
index 9cb4e27..3ed543f 100644
--- a/stego_llm/llm/interface.py
+++ b/stego_llm/llm/interface.py
@@ -8,6 +8,7 @@ from .utilities import suppress_stderr, logits_to_probabilities, to_json
 @suppress_stderr
 def create_llm_client(
     model_path=None,
+    **llm_options,
 ):
     """Initialize and return a Llama LLM client."""
     if model_path is None:
@@ -17,6 +18,7 @@ def create_llm_client(
     return Llama(
         model_path=str(model_path),
         logits_all=True,
+        **llm_options
     )
```
</pre>

<h3>Patch</h3>

<pre>
commit 9abdb61deaea959061e62b6d3aae2e73311b26b8
Author: sutt <wsutton17@gmail.com>
Date:   Thu Sep 11 12:13:38 2025 -0400

    test: add tests for llm_extra_args passthrough

diff --git a/tests/test_integration.py b/tests/test_integration.py
index 9368179..b39e8e0 100644
--- a/tests/test_integration.py
+++ b/tests/test_integration.py
@@ -6,6 +6,35 @@ import pytest
 
 from stego_llm.core import main_decode, main_encode
 
+
+def test_encode_llm_extra_args(mocker):
+    """Test that llm_extra_args are passed to create_llm_client in main_encode."""
+    mock_create_llm = mocker.patch("stego_llm.core.encoder.create_llm_client")
+
+    main_encode(
+        initial_prompt="test",
+        msg=b"",
+        llm_extra_args={"n_ctx": 1024},
+        llm_path="dummy",
+    )
+
+    mock_create_llm.assert_called_once_with(model_path="dummy", n_ctx=1024)
+
+
+def test_decode_llm_extra_args(mocker):
+    """Test that llm_extra_args are passed to create_llm_client in main_decode."""
+    mock_create_llm = mocker.patch("stego_llm.core.decoder.create_llm_client")
+
+    main_decode(
+        encoded_prompt="test",
+        initial_prompt="test",
+        llm_extra_args={"n_ctx": 1024},
+        llm_path="dummy",
+    )
+
+    mock_create_llm.assert_called_once_with(model_path="dummy", n_ctx=1024)
+
+
 # Get model path from environment variable: preferred and fallabck
 TEST_LLM_PATH = os.environ.get("INNOCUOUS_TEST_LLM_PATH")
 if TEST_LLM_PATH is None:
</pre>
</details>

#### `cli-numlogprobs.md`
- **Spec Summary:** *Create optional CLI argument --num-logprobs with default value of 100.*
- **Commit Message:** *feat: add --num-logprobs argument to CLI*
- **Task Notes:** Simple.
- **Src Diffs:** +8/-4 | **Test Diffs:** +0/-0
- **Spec:** cli-numlogprobs.md | **Patch Sha:** fe8dbf6
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
on the cli, create an optional argument for --num-logprobs which defaults to 100.
</pre>

<h3>Patch</h3>

<pre>
commit fe8dbf691cf51328eb9e80555aa91e8c5eebc293
Author: sutt <wsutton17@gmail.com>
Date:   Thu Sep 11 08:33:23 2025 -0400

    feat: add --num-logprobs argument to CLI

diff --git a/stego_llm/cli.py b/stego_llm/cli.py
index de411e0..9280c80 100644
--- a/stego_llm/cli.py
+++ b/stego_llm/cli.py
@@ -23,6 +23,12 @@ def main():
     parser.add_argument(
         "--chunk_size", type=int, default=2, help="Chunk size for encoding/decoding"
     )
+    parser.add_argument(
+        "--num-logprobs",
+        type=int,
+        default=100,
+        help="Number of log probabilities to consider",
+    )
     prompt_group = parser.add_mutually_exclusive_group()
     prompt_group.add_argument(
         "--initial-prompt-text", type=str, help="Initial prompt text"
@@ -66,8 +72,6 @@ def main():
     elif args.initial_prompt_file:
         initial_prompt = args.initial_prompt_file.read_text()
 
-    # Hardcoded for now
-    num_logprobs = 100
     if initial_prompt is None:
         initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king"
 
@@ -87,7 +91,7 @@ def main():
             initial_prompt=initial_prompt,
             msg=message_bytes,
             chunk_size=args.chunk_size,
-            num_logprobs=num_logprobs,
+            num_logprobs=args.num_logprobs,
             llm_path=args.llm_path,
         )
         print(encoded_message)
@@ -103,7 +107,7 @@ def main():
             encoded_prompt=encoded_text,
             initial_prompt=initial_prompt,
             chunk_size=args.chunk_size,
-            num_logprobs=num_logprobs,
+            num_logprobs=args.num_logprobs,
             llm_path=args.llm_path,
         )
         print(repr(decoded_bytes))
</pre>
</details>

#### `integration-test.md`
- **Spec Summary:** *Add integration test: msg0 -> encode -> decode -> msg1, assert msg0==msg1. Use pytest marker for slow tests. Mock env variable or config for model_path.*
- **Commit Message:** *test: add integration test for full encode/decode cycle*
- **Task Notes:** Tricky tests implemented with best practices.
- **Src Diffs:** +0/-0 | **Test Diffs:** +44/-0
- **Spec:** integration-test.md | **Patch Sha:** 6203b4a
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
add new test which run an msg0 -> encode -> decode -> msg1, assert msg0==msg1 check.
use a pytest test marker to indicate these will run slowly and don't run by default.
add structure to mock the env variable or to pass in the model_path via a config.
</pre>

<h3>Patch</h3>

<pre>
commit 6203b4a7d8fd56fffca6df21fe55a8b85397a900
Author: sutt <wsutton17@gmail.com>
Date:   Thu Sep 4 16:29:22 2025 -0400

    test: add integration test for full encode/decode cycle

diff --git a/pyproject.toml b/pyproject.toml
index 12041a3..6135f19 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -55,3 +55,7 @@ dev = [
 
 [tool.pytest.ini_options]
 testpaths = ["tests"]
+markers = [
+    "slow: marks tests as slow to run",
+]
+addopts = "-m 'not slow'"
diff --git a/tests/test_integration.py b/tests/test_integration.py
new file mode 100644
index 0000000..471dc89
--- /dev/null
+++ b/tests/test_integration.py
@@ -0,0 +1,44 @@
+import os
+
+import pytest
+
+from stego_llm.core import main_decode, main_encode
+
+# Get model path from environment variable
+LLAMA_MODEL_PATH = os.environ.get("LLAMA_MODEL_PATH")
+
+
+@pytest.mark.slow
+@pytest.mark.skipif(
+    not LLAMA_MODEL_PATH, reason="LLAMA_MODEL_PATH environment variable not set"
+)
+def test_encode_decode_integration():
+    """
+    Test the full encode-decode cycle.
+    This is a slow test and requires a language model.
+    """
+    initial_prompt = "This is a test."
+    message_to_encode = b"secret message"
+    chunk_size = 2
+
+    # Encode the message
+    encoded_text = main_encode(
+        initial_prompt=initial_prompt,
+        msg=message_to_encode,
+        chunk_size=chunk_size,
+        llm_path=LLAMA_MODEL_PATH,
+    )
+
+    assert encoded_text is not None
+    assert encoded_text != initial_prompt
+
+    # Decode the message
+    decoded_message = main_decode(
+        encoded_prompt=encoded_text,
+        initial_prompt=initial_prompt,
+        chunk_size=chunk_size,
+        llm_path=LLAMA_MODEL_PATH,
+    )
+
+    assert decoded_message is not None
+    assert decoded_message == message_to_encode
</pre>
</details>

#### `type-main-funcs.md`
- **Spec Summary:** *Add type hints for args and return types to decoder.main_decoder and encoder.main_encode in stego_llm.core. Include expanded docstrings.*
- **Commit Message:** *refactor: add type hints and docstrings to main functions*
- **Task Notes:** Simple but the verbose docstrings are useful to handle with ai.
- **Src Diffs:** +48/-14 | **Test Diffs:** +0/-0
- **Spec:** type-main-funcs.md | **Patch Sha:** b00dd60
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
in stego_llm.core for:
    - decoder.main_decoder 
    - encoder.main_encode
- implement types for args
- implement types for return type
- add more expansive doc string
</pre>

<h3>Patch</h3>

<pre>
commit b00dd60a7165070e42c6f1f3b04e7b1c2105b8f1
Author: sutt <wsutton17@gmail.com>
Date:   Wed Sep 3 12:09:11 2025 -0400

    refactor: add type hints and docstrings to main functions

diff --git a/stego_llm/core/decoder.py b/stego_llm/core/decoder.py
index 5b20748..e9cd0de 100644
--- a/stego_llm/core/decoder.py
+++ b/stego_llm/core/decoder.py
@@ -1,5 +1,6 @@
 import logging
+from typing import Optional
 
 from stego_llm.steganography import (
     chunks_to_message,
@@ -18,15 +19,29 @@
 
 
 def main_decode(
-    encoded_prompt,
-    initial_prompt,
-    chunk_size,
-    num_logprobs,
-    llm_path=None,
-):
-    """Main decoding function for steganographic message extraction."""
+    encoded_prompt: str,
+    initial_prompt: str,
+    chunk_size: int = 2,
+    num_logprobs: int = 100,
+    llm_path: Optional[str] = None,
+) -> Optional[bytes]:
+    """Decodes a message hidden in a text.
+
+    Args:
+        encoded_prompt (str): The text containing the hidden message.
+        initial_prompt (str): The initial prompt used for encoding.
+        chunk_size (int): The size of the chunks in bits.
+        num_logprobs (int): The number of token probabilities to consider.
+        llm_path (Optional[str]): The path to the language model file.
+            If None, the default model is used.
+
+    Returns:
+        Optional[bytes]: The decoded message as bytes, or None if decoding fails.
+    """
     llm = create_llm_client(model_path=llm_path)
     message_carrying_text = encoded_prompt[len(initial_prompt) :]
     memo = {}
diff --git a/stego_llm/core/encoder.py b/stego_llm/core/encoder.py
index 4b6e5ea..fb4b0e0 100644
--- a/stego_llm/core/encoder.py
+++ b/stego_llm/core/encoder.py
@@ -1,5 +1,6 @@
 import logging
 
+from typing import Optional
 from stego_llm.steganography import (
     message_to_chunks,
     find_acceptable_token,
@@ -18,15 +19,29 @@
 
 
 def main_encode(
-    initial_prompt,
-    msg,
-    chunk_size,
-    num_logprobs,
-    llm_path=None,
-):
-    """Main encoding function for steganographic text generation."""
+    initial_prompt: str,
+    msg: bytes,
+    chunk_size: int = 2,
+    num_logprobs: int = 100,
+    llm_path: Optional[str] = None,
+) -> str:
+    """Encodes a message into a text using steganography.
+
+    Args:
+        initial_prompt (str): The initial prompt to start text generation.
+        msg (bytes): The message to be hidden in the text.
+        chunk_size (int): The size of the chunks in bits for encoding.
+        num_logprobs (int): The number of next-token probabilities to request from the LLM.
+        llm_path (Optional[str]): The path to the language model file.
+            If None, the default model is used.
+
+    Returns:
+        str: The generated text with the message embedded within it.
+    """
     llm = create_llm_client(model_path=llm_path)
     enc_ints = message_to_chunks(msg, chunk_size=chunk_size)
     current_prompt = initial_prompt
</pre>
</details>

#### `version-cmd.md`
- **Spec Summary:** *Enable CLI and Python import to display package version from pyproject.toml.*
- **Commit Message:** *feat: add --version flag and dynamic version loading*
- **Task Notes:** Easy, but esoteric.
- **Src Diffs:** +10/-2 | **Test Diffs:** +0/-0
- **Spec:** version-cmd.md | **Patch Sha:** 80791f9
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
allow the cli and the python import to list the version of the package that exists in the pyproject.toml
</pre>

<h3>Patch</h3>

<pre>
commit 80791f943a3816a4e981971ba1c6d6566f680244
Author: sutt <wsutton17@gmail.com>
Date:   Wed Sep 3 18:47:53 2025 -0400

    feat: add --version flag and dynamic version loading

diff --git a/stego_llm/__init__.py b/stego_llm/__init__.py
index 739b68f..c1fa2ad 100644
--- a/stego_llm/__init__.py
+++ b/stego_llm/__init__.py
@@ -3,9 +3,13 @@ LLM Steganography Package
 
 A library for embedding and extracting hidden messages in LLM-generated text.
 """
+from importlib import metadata
 
 from .core import main_encode, main_decode
 from .llm import check_llm
 
-__all__ = ["main_encode", "main_decode", "check_llm"]
-__version__ = "0.1.0"
+__all__ = ["main_encode", "main_decode", "check_llm", "__version__"]
+try:
+    __version__ = metadata.version("innocuous")
+except metadata.PackageNotFoundError:
+    __version__ = "0.0.0"  # Local development version
diff --git a/stego_llm/cli.py b/stego_llm/cli.py
index e97194c..8f92870 100644
--- a/stego_llm/cli.py
+++ b/stego_llm/cli.py
@@ -3,6 +3,7 @@ import logging
 import sys
 from pathlib import Path
 
+from stego_llm import __version__
 from stego_llm.core import main_decode, main_encode
 from stego_llm.llm import check_llm
 
@@ -12,6 +13,9 @@ logger = logging.getLogger(__name__)
 def main():
     """CLI entry point."""
     parser = argparse.ArgumentParser(description="LLM Steganography")
+    parser.add_argument(
+        "--version", action="version", version=f"%(prog)s {__version__}"
+    )
     parser.add_argument(
         "-v", "--verbose", action="count", default=0, help="Increase verbosity"
     )
</pre>
</details>

---

## v0.2.2

---

## v0.2.1

#### `devsummary-task-b.md`
- **Spec Summary:** *Update table in docs/dev-summary.md for v0.1.0 with git diff values for code changes columns. Each value represented as "+A/-D" format for additions/deletions from git diff --stat.*
- **Commit Message:** *feat: impl devsummary-task-b with claude (agro auto-commit)*
- **Task Notes:** 
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-0
- **Spec:** devsummary-task-b.md | **Patch Sha:** 97da5a8
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
### Script Vars
Utilize these variables below for the task as you read it and process it. The script var will be denoted with $my_script_var when utilized and should be read the value corresponding.

- target_doc: docs/dev-summary.md 
- version_to_update: v0.2.3
- diffs_main_directory: stego_llm
- diffs_on_other_directories: tests

### Steps to Update & Execute this Spec
This section should be ignored by the AI agent; it's for the developer's reference to edit this file for:
Updating:
- Update the variables in script vars:
    - the diffs vars are helpful for different repo setups
Executing:
- Claude excels at this task.
- Enable the `Bash(git:*)` permissions for the claude agent.

### Task
These are the instructions for your task. Remember to insert the script vars from above when seeing a variable preseeded by $.
update the table in $target_doc:
- update the table for $version_to_update
- add values for all (or some of) the "code changes" / "diffs" columns:
    - use the column name to understand which slices of the codebase should be considered for the diffs.
    - these code diffs should only apply to the particular git commit referenced in that row of the table (it should not be the total diffs over the whole version)
    - for the first diff column, use the diffs from within directory $diff_main_directory
    - for the second diff column, use the the diffs from within directory $diff_on_other_directories
- each value should be represented as "+A/-D" where A is the number of additions and -D is deletion or modifications from a git diff / git diff --stat,
    - e.g. "+23/-12", or "+5/-0"

Use git commands to investigate these commit shas and run git diffs that will allows you to fill in the full table.

Rules used to build the table previously:
- only include specs/* files for rows
- sort by date order desc (the date information will supplied at the end)

Reference for commit sha's in the table
```
04d2537 build: v0.2.3
222a1ca specs: v0.2.3
f01571c docs: update dev-summary for 0.2.1 and 0.2.2
b7c73e9 refactor: ruff format
9abdb61 test: add tests for llm_extra_args passthrough
2f85f37 feat: adding llm_extra_args for use in library functions
deac5b5 refactor: llama logging override now wrapped as function
77a030d refactor: cli arguments --chunk-size
cbc0de0 refactor: logging enables info level, repr of output for -v mode.
fe8dbf6 feat: add --num-logprobs argument to CLI
313efe3 fix: cli defaults to chunk_size=2 (aligns with library method defaults)
5b23579 feat: decoder fills in missing auto_accept tokens + debugging trace for decoder
711aea0 test: add sleep + gc fixture to integration test setup
f57aea1 test: refactor previous test, add decoder-only integration test
6203b4a test: add integration test for full encode/decode cycle
ddcd740 fix: add default arg vals
b00dd60 refactor: add type hints and improve docstrings for core functions
80791f9 feat: add --version flag and dynamic version loading
1505e99 build: bump version v0.2.2
```
</pre>

<h3>Patch</h3>

<pre>
commit 97da5a8052e8781351509203382f1d621322154b
Author: agro <agro-committer@users.noreply.github.com>
Date:   Tue Aug 26 15:12:05 2025 -0400

    feat: impl devsummary-task-b with claude (agro auto-commit)

diff --git a/docs/dev-summary.md b/docs/dev-summary.md
index 8c33a1b..3302820 100644
--- a/docs/dev-summary.md
+++ b/docs/dev-summary.md
@@ -1,13 +1,13 @@
 # Dev Summary
 
-| Taskfile | Summary | Commit |
-|---|---|---|
-| [fix-tests.md](/.public-agdocs/specs/fix-tests.md) | Update tests to pass after changes to create_llm_client import and function signature. Tests were failing because create_llm_client was moved from cli.py and the function interface changed to accept llm_path parameter. | [c7cdd56](https://github.com/innocuous-dev/innocuous/commit/c7cdd56) |
-| [check-llm.md](/.public-agdocs/specs/check-llm.md) | Add subcommand "check-llm" and exportable function "check_llm" to verify LLM path from CLI/env var, check file existence, and execute simple inference task. Print terse confirmation of each step. | [0355954](https://github.com/innocuous-dev/innocuous/commit/0355954) |
-| [modelpath-env.md](/.public-agdocs/specs/modelpath-env.md) | In llm.interface:create_llm_client have model_path load from env var "INNOCUOUS_LLM_PATH". Add optional CLI arg and function args to override env var. | [55cf7ce](https://github.com/innocuous-dev/innocuous/commit/55cf7ce) |
-| [devsummary-task-b.md](/.public-agdocs/specs/devsummary-task-b.md) | Update table in docs/dev-summary.md for v0.1.0 with git diff values for code changes columns. Each value represented as "+A/-D" format for additions/deletions from git diff --stat. | [d3321ed](https://github.com/innocuous-dev/innocuous/commit/d3321ed) |
-| [devsummary-task-a.md](/.public-agdocs/specs/devsummary-task-a.md) | Add updated taskfiles to markdown table in docs/dev-summary.md for v0.1.0 with filename, summary, and GitHub SHA links. Sort by date descending and include only specs/* files. | [9f91a82](https://github.com/innocuous-dev/innocuous/commit/9f91a82) |
-| [cli-add.md](/.public-agdocs/specs/cli-add.md) | Add CLI interface for stego-llm package with script "innocuous" having encode/decode subcommands. Include optional flags for verbosity, chunk size, and initial prompt options. Create tests for functionality. | [0cb642f](https://github.com/innocuous-dev/innocuous/commit/0cb642f) |
+| Taskfile | Summary | Commit | Non-test Diffs | Test Diffs |
+|---|---|---|---|---|
+| [fix-tests.md](/.public-agdocs/specs/fix-tests.md) | Update tests to pass after changes to create_llm_client import and function signature. Tests were failing because create_llm_client was moved from cli.py and the function interface changed to accept llm_path parameter. | [c7cdd56](https://github.com/innocuous-dev/innocuous/commit/c7cdd56) | +0/-0 | +0/-10 |
+| [check-llm.md](/.public-agdocs/specs/check-llm.md) | Add subcommand "check-llm" and exportable function "check_llm" to verify LLM path from CLI/env var, check file existence, and execute simple inference task. Print terse confirmation of each step. | [0355954](https://github.com/innocuous-dev/innocuous/commit/0355954) | +51/-9 | +38/-0 |
+| [modelpath-env.md](/.public-agdocs/specs/modelpath-env.md) | In llm.interface:create_llm_client have model_path load from env var "INNOCUOUS_LLM_PATH". Add optional CLI arg and function args to override env var. | [55cf7ce](https://github.com/innocuous-dev/innocuous/commit/55cf7ce) | +24/-10 | +0/-0 |
+| [devsummary-task-b.md](/.public-agdocs/specs/devsummary-task-b.md) | Update table in docs/dev-summary.md for v0.1.0 with git diff values for code changes columns. Each value represented as "+A/-D" format for additions/deletions from git diff --stat. | [d3321ed](https://github.com/innocuous-dev/innocuous/commit/d3321ed) | +0/-0 | +0/-0 |
+| [devsummary-task-a.md](/.public-agdocs/specs/devsummary-task-a.md) | Add updated taskfiles to markdown table in docs/dev-summary.md for v0.1.0 with filename, summary, and GitHub SHA links. Sort by date descending and include only specs/* files. | [9f91a82](https://github.com/innocuous-dev/innocuous/commit/9f91a82) | +0/-0 | +0/-0 |
+| [cli-add.md](/.public-agdocs/specs/cli-add.md) | Add CLI interface for stego-llm package with script "innocuous" having encode/decode subcommands. Include optional flags for verbosity, chunk size, and initial prompt options. Create tests for functionality. | [0cb642f](https://github.com/innocuous-dev/innocuous/commit/0cb642f) | +101/-0 | +139/-0 |
 
 ---
 
</pre>
</details>

#### `devsummary-task-a.md`
- **Spec Summary:** *Add updated taskfiles to markdown table in docs/dev-summary.md for v0.1.0 with filename, summary, and GitHub SHA links. Sort by date descending and include only specs/* files.*
- **Commit Message:** *feat: impl devsummary-task-a with claude (agro auto-commit)*
- **Task Notes:** 
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-0
- **Spec:** devsummary-task-a.md | **Patch Sha:** 46468bd
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
### Script Vars
Utilize these variables below for the task as you read it and process it. The script var will be denoted with $my_script_var when utilized and should be read the value corresponding.

- target_doc: docs/dev-summary.md 
- version_to_update: v0.2.3
- max_summary_chars: 250
- repo_url: github.com/sutt/innocuous

### Steps to Update & Execute this Spec
This section should be ignored by the AI agent; it's for the developer's reference to edit this file for:
Updating:
- Update the variables in script vars
- Run the 3 reference commands and add output to the sections "Command Outputs".
Executing:
- Claude often excels at this task
- Descriptive commit messages are helpful; multiple commit messages with same verbiage can confuse it.

### Command Reference:
These commands you should not run or pay attention to any of these. They are simply are reference for the developer:
> git diff --stat v0.2.2 v0.2.3 -- .public-agdocs/specs
> ls -lt .agdocs/specs/ 
> git log --oneline --no-merges  --not  -n 36

### Task
These are the instructions for your task. Remember to insert the script vars from above when seeing avariable preseeded by $.

Add the updated taskfiles to a markdown table in $target_doc 
for $version_to_update with a row containing:
- just the filename and have it be linked with relative path notation to where it resides in .public-agdocs
- a summary of the files contents (max $max_summary_chars chars)
- add a field that links to a 6-char git sha entry  on the github repo: $repo_url. Do your best guess to find the corresponding commit (available with commit message below). If your guess is too uncertain, or it appears there is no commit for it, place an n/a for this entry.

Rules for the table:
- only include specs/* files for rows
- sort by date order desc (the date information will supplied at the end)
- don't update the rightmost three columns ("diffs" + "notes"). These values will be supplied in a later task.

#### Command Outputs

##### Spec Changes
Here's the result for the following command:

git diff --stat v0.2.2 v0.2.3 -- .public-agdocs/specs

 .public-agdocs/specs/cli-numlogprobs.md   |  1 +
 .public-agdocs/specs/extra-args-test.md   | 92 +++++++++++++++++++++++++++++++
 .public-agdocs/specs/integration-test.md  |  3 +
 .public-agdocs/specs/type-main-funcs.md   |  6 ++
 .public-agdocs/specs/version-cmd.md       |  1 +
 7 files changed, 175 insertions(+), 84 deletions(-)



##### Specs Time-Sorted
Here's the information for the date created which should be used to sort the rows for the table above.

Results of the command: 

ls -lt .agdocs/specs/ 

-rw-r--r-- 1 user user  3348 Sep 11 12:10 extra-args-test.md
-rw-r--r-- 1 user user    81 Sep 11 08:32 cli-numlogprobs.md
-rw-r--r-- 1 user user   251 Sep  4 16:26 integration-test.md
-rw-r--r-- 1 user user   169 Sep  3 19:16 type-main-funcs.md
-rw-r--r-- 1 user user   104 Sep  3 18:46 version-cmd.md


##### Commit Logs
Here's the output of the following command, use this to link a solution sha to a task file

git log --oneline --no-merges  --not  -n 36

04d2537 build: v0.2.3
222a1ca specs: v0.2.3
f01571c docs: update dev-summary for 0.2.1 and 0.2.2
b7c73e9 refactor: ruff format
9abdb61 test: add tests for llm_extra_args passthrough
2f85f37 feat: adding llm_extra_args for use in library functions
deac5b5 refactor: llama logging override now wrapped as function
77a030d refactor: cli arguments --chunk-size
cbc0de0 refactor: logging enables info level, repr of output for -v mode.
fe8dbf6 feat: add --num-logprobs argument to CLI
313efe3 fix: cli defaults to chunk_size=2 (aligns with library method defaults)
5b23579 feat: decoder fills in missing auto_accept tokens + debugging trace for decoder
711aea0 test: add sleep + gc fixture to integration test setup
f57aea1 test: refactor previous test, add decoder-only integration test
6203b4a test: add integration test for full encode/decode cycle
ddcd740 fix: add default arg vals
b00dd60 refactor: add type hints and improve docstrings for core functions
80791f9 feat: add --version flag and dynamic version loading
1505e99 build: bump version v0.2.2
</pre>

<h3>Patch</h3>

<pre>
commit 46468bd13305fb6d77a05342134a81521518c64f
Author: agro <agro-committer@users.noreply.github.com>
Date:   Tue Aug 26 15:11:50 2025 -0400

    feat: impl devsummary-task-a with claude (agro auto-commit)

diff --git a/docs/dev-summary.md b/docs/dev-summary.md
index 3302820..8c33a1b 100644
--- a/docs/dev-summary.md
+++ b/docs/dev-summary.md
@@ -1,13 +1,23 @@
 # Dev Summary
 
-| Taskfile | Summary | Commit | Non-test Diffs | Test Diffs |
-|---|---|---|---|---|
-| [fix-tests.md](/.public-agdocs/specs/fix-tests.md) | Update tests to pass after changes to create_llm_client import and function signature. Tests were failing because create_llm_client was moved from cli.py and the function interface changed to accept llm_path parameter. | [c7cdd56](https://github.com/innocuous-dev/innocuous/commit/c7cdd56) | +0/-0 | +0/-10 |
-| [check-llm.md](/.public-agdocs/specs/check-llm.md) | Add subcommand "check-llm" and exportable function "check_llm" to verify LLM path from CLI/env var, check file existence, and execute simple inference task. Print terse confirmation of each step. | [0355954](https://github.com/innocuous-dev/innocuous/commit/0355954) | +51/-9 | +38/-0 |
-| [modelpath-env.md](/.public-agdocs/specs/modelpath-env.md) | In llm.interface:create_llm_client have model_path load from env var "INNOCUOUS_LLM_PATH". Add optional CLI arg and function args to override env var. | [55cf7ce](https://github.com/innocuous-dev/innocuous/commit/55cf7ce) | +24/-10 | +0/-0 |
-| [devsummary-task-b.md](/.public-agdocs/specs/devsummary-task-b.md) | Update table in docs/dev-summary.md for v0.1.0 with git diff values for code changes columns. Each value represented as "+A/-D" format for additions/deletions from git diff --stat. | [d3321ed](https://github.com/innocuous-dev/innocuous/commit/d3321ed) | +0/-0 | +0/-0 |
-| [devsummary-task-a.md](/.public-agdocs/specs/devsummary-task-a.md) | Add updated taskfiles to markdown table in docs/dev-summary.md for v0.1.0 with filename, summary, and GitHub SHA links. Sort by date descending and include only specs/* files. | [9f91a82](https://github.com/innocuous-dev/innocuous/commit/9f91a82) | +0/-0 | +0/-0 |
-| [cli-add.md](/.public-agdocs/specs/cli-add.md) | Add CLI interface for stego-llm package with script "innocuous" having encode/decode subcommands. Include optional flags for verbosity, chunk size, and initial prompt options. Create tests for functionality. | [0cb642f](https://github.com/innocuous-dev/innocuous/commit/0cb642f) | +101/-0 | +139/-0 |
+## v0.2.0
+
+| Taskfile | Summary | Commit |
+|---|---|---|
+| [devsummary-task-a.md](/.public-agdocs/specs/devsummary-task-a.md) | Add updated taskfiles to markdown table in docs/dev-summary.md for v0.1.0 with filename, summary, and GitHub SHA links. Sort by date descending and include only specs/* files. | [9f91a82](https://github.com/sutt/innocuous/commit/9f91a82) |
+| [update-examples.md](/.public-agdocs/specs/update-examples.md) | Updates scripts in examples/ directory to reflect change about model_path needing to be passed in explicitly. Includes diffs for __init__.py, cli.py, core modules, and llm interface changes. | [e7b8d5b](https://github.com/sutt/innocuous/commit/e7b8d5b) |
+| [fix-tests.md](/.public-agdocs/specs/fix-tests.md) | Update tests to pass after changes to create_llm_client import and function signature. Tests were failing because create_llm_client was moved from cli.py and the function interface changed to accept llm_path parameter. | [c7cdd56](https://github.com/sutt/innocuous/commit/c7cdd56) |
+| [check-llm.md](/.public-agdocs/specs/check-llm.md) | Add subcommand "check-llm" and exportable function "check_llm" to verify LLM path from CLI/env var, check file existence, and execute simple inference task. Print terse confirmation of each step. | [0355954](https://github.com/sutt/innocuous/commit/0355954) |
+| [modelpath-env.md](/.public-agdocs/specs/modelpath-env.md) | In llm.interface:create_llm_client have model_path load from env var "INNOCUOUS_LLM_PATH". Add optional CLI arg and function args to override env var. | [55cf7ce](https://github.com/sutt/innocuous/commit/55cf7ce) |
+| [devsummary-task-b.md](/.public-agdocs/specs/devsummary-task-b.md) | Update table in docs/dev-summary.md for v0.1.0 with git diff values for code changes columns. Each value represented as "+A/-D" format for additions/deletions from git diff --stat. | [d3321ed](https://github.com/sutt/innocuous/commit/d3321ed) |
+| [cli-add.md](/.public-agdocs/specs/cli-add.md) | Add CLI interface for stego-llm package with script "innocuous" having encode/decode subcommands. Include optional flags for verbosity, chunk size, and initial prompt options. Create tests for functionality. | [0cb642f](https://github.com/sutt/innocuous/commit/0cb642f) |
+
+---
+
+## v0.1.0
+
+| Taskfile | Summary | Commit |
+|---|---|---|
+| [prepost-filter-decode.md](/.public-agdocs/specs/prepost-filter-decode.md) | Apply refactor of filter_tok logic to pre_accept_filter + post_accept_filter functions in src/main:main_decode. Allow main_decode to take into account same logic so decoded data matches input. Functions will be extended with additional details. | [960c697](https://github.com/sutt/innocuous/commit/960c697) |
+| [decode-accept-1.md](/.public-agdocs/specs/decode-accept-1.md) | Apply the accept_tok logic that was added to main_encode to main_decode. Use partial diff showing function usage. Allow main_decode to take into account same logic so decoded data matches input. Accept_tok will be extended with additional details. | [79a4c67](https://github.com/sutt/innocuous/commit/79a4c67) |
+| [decode-branch.md](/.public-agdocs/specs/decode-branch.md) | Refactor decode_main function to handle situation where remaining_text may .startswith match with multiple eligible tokens. Need branching to check maxsize of first 2**chunk_size tokens after tok_filter. Apply hacky solution for now. | [cdabc98](https://github.com/sutt/innocuous/commit/cdabc98) |
+| [decode1.md](/.public-agdocs/specs/decode1.md) | In src/main.py implement main_decode | [d4dd55e](https://github.com/sutt/innocuous/commit/d4dd55e) |
 
 ---
 
</pre>
</details>

---

## v0.2.0

#### `update-examples.md`
- **Spec Summary:** *Updates scripts in examples/ directory to reflect change about model_path needing to be passed in explicitly. Includes diffs for __init__.py, cli.py, core modules, and llm interface changes.*
- **Commit Message:** *feat: add configurable LLM path and check-llm command*
- **Task Notes:** Time-saving use-case of handling downstream breaking changes from a refactor.
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-0
- **Spec:** update-examples.md | **Patch Sha:** e7b8d5b
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
Updates the scripts in the examples/ directory to reflect the change about model_path needing to be passed in explicitly.

diff --git a/stego_llm/__init__.py b/stego_llm/__init__.py
index debb3ff..739b68f 100644
--- a/stego_llm/__init__.py
+++ b/stego_llm/__init__.py
@@ -5,6 +5,7 @@ A library for embedding and extracting hidden messages in LLM-generated text.
 """
 
 from .core import main_encode, main_decode
+from .llm import check_llm
 
-__all__ = ["main_encode", "main_decode"]
+__all__ = ["main_encode", "main_decode", "check_llm"]
 __version__ = "0.1.0"
diff --git a/stego_llm/cli.py b/stego_llm/cli.py
index 7f3653f..e97194c 100644
--- a/stego_llm/cli.py
+++ b/stego_llm/cli.py
@@ -4,7 +4,7 @@ import sys
 from pathlib import Path
 
 from stego_llm.core import main_decode, main_encode
-from stego_llm.llm import create_llm_client
+from stego_llm.llm import check_llm
 
 logger = logging.getLogger(__name__)
 
@@ -15,6 +15,7 @@ def main():
     parser.add_argument(
         "-v", "--verbose", action="count", default=0, help="Increase verbosity"
     )
+    parser.add_argument("--llm-path", type=Path, help="Path to LLM GGUF file")
     parser.add_argument(
         "--chunk_size", type=int, default=3, help="Chunk size for encoding/decoding"
     )
@@ -43,6 +44,9 @@ def main():
         "--file", type=Path, help="Path to file with message to decode"
     )
 
+    # Check LLM command
+    subparsers.add_parser("check-llm", help="Check LLM configuration")
+
     args = parser.parse_args()
 
     log_level = logging.WARNING
@@ -75,13 +79,12 @@ def main():
         elif args.btc_addr:
             message_bytes = args.btc_addr.encode("utf-8")
 
-        llm = create_llm_client()
         encoded_message = main_encode(
-            llm=llm,
             initial_prompt=initial_prompt,
             msg=message_bytes,
             chunk_size=args.chunk_size,
             num_logprobs=num_logprobs,
+            llm_path=args.llm_path,
         )
         print(encoded_message)
 
@@ -92,16 +95,18 @@ def main():
         elif args.file:
             encoded_text = args.file.read_text()
 
-        llm = create_llm_client()
         decoded_bytes = main_decode(
-            llm=llm,
             encoded_prompt=encoded_text,
             initial_prompt=initial_prompt,
             chunk_size=args.chunk_size,
             num_logprobs=num_logprobs,
+            llm_path=args.llm_path,
         )
         print(repr(decoded_bytes))
 
+    elif args.command == "check-llm":
+        check_llm(llm_path=args.llm_path, verbose=args.verbose >= 2)
+
 
 if __name__ == "__main__":
     main()
diff --git a/stego_llm/core/decoder.py b/stego_llm/core/decoder.py
index a8f6045..5b20748 100644
--- a/stego_llm/core/decoder.py
+++ b/stego_llm/core/decoder.py
@@ -5,7 +5,11 @@ from stego_llm.steganography import (
     pre_selection_filter,
     post_selection_filter,
 )
-from stego_llm.llm import get_token_probabilities, logits_to_probabilities
+from stego_llm.llm import (
+    create_llm_client,
+    get_token_probabilities,
+    logits_to_probabilities,
+)
 from .trace import _trace_decoding_step
 
 
@@ -13,13 +17,14 @@ logger = logging.getLogger(__name__)
 
 
 def main_decode(
-    llm,
     encoded_prompt,
     initial_prompt,
     chunk_size,
     num_logprobs,
+    llm_path=None,
 ):
     """Main decoding function for steganographic message extraction."""
+    llm = create_llm_client(model_path=llm_path)
     message_carrying_text = encoded_prompt[len(initial_prompt) :]
     memo = {}
 
diff --git a/stego_llm/core/encoder.py b/stego_llm/core/encoder.py
index 3cf5a44..4b6e5ea 100644
--- a/stego_llm/core/encoder.py
+++ b/stego_llm/core/encoder.py
@@ -5,7 +5,11 @@ from stego_llm.steganography import (
     pre_selection_filter,
     post_selection_filter,
 )
-from stego_llm.llm import get_token_probabilities, logits_to_probabilities
+from stego_llm.llm import (
+    create_llm_client,
+    get_token_probabilities,
+    logits_to_probabilities,
+)
 from .trace import _trace_encoding_step
 
 
@@ -13,13 +17,14 @@ logger = logging.getLogger(__name__)
 
 
 def main_encode(
-    llm,
     initial_prompt,
     msg,
     chunk_size,
     num_logprobs,
+    llm_path=None,
 ):
     """Main encoding function for steganographic text generation."""
+    llm = create_llm_client(model_path=llm_path)
     enc_ints = message_to_chunks(msg, chunk_size=chunk_size)
     current_prompt = initial_prompt
 
diff --git a/stego_llm/llm/__init__.py b/stego_llm/llm/__init__.py
index 428debf..4e370e4 100644
--- a/stego_llm/llm/__init__.py
+++ b/stego_llm/llm/__init__.py
@@ -1,4 +1,4 @@
-from .interface import create_llm_client, get_token_probabilities
+from .interface import create_llm_client, get_token_probabilities, check_llm
 from .utilities import logits_to_probabilities, to_json
 
 __all__ = [
@@ -6,4 +6,5 @@ __all__ = [
     "get_token_probabilities",
     "logits_to_probabilities",
     "to_json",
+    "check_llm",
 ]
diff --git a/stego_llm/llm/interface.py b/stego_llm/llm/interface.py
index 81a28a0..5a9dc2f 100644
--- a/stego_llm/llm/interface.py
+++ b/stego_llm/llm/interface.py
@@ -1,4 +1,5 @@
 import json
+import os
 import numpy as np
 from llama_cpp import Llama
 from .utilities import suppress_stderr, logits_to_probabilities, to_json
@@ -6,9 +7,13 @@ from .utilities import suppress_stderr, logits_to_probabilities, to_json
 
 @suppress_stderr
 def create_llm_client(
-    model_path="/home/user/dev/innocuous/data/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
+    model_path=None,
 ):
     """Initialize and return a Llama LLM client."""
+    if model_path is None:
+        model_path = os.environ.get("INNOCUOUS_LLM_PATH")
+    if model_path is None:
+        raise ("Neither INNOCUOUS_LLM_PATH nor --llm-path supplied. Exiting.")
     return Llama(
         model_path=model_path,
         logits_all=True,
@@ -28,10 +33,43 @@ def get_token_probabilities(llm, prompt, num_output=10):
     return top_logprobs
 
 
-def demo():
-    """Demo function showing basic LLM usage."""
-    # TODO - add this cli status check command
-    llm = create_llm_client()
-    top_logprobs = get_token_probabilities(llm)
-    top_logprobs = logits_to_probabilities(top_logprobs)
-    print(to_json(top_logprobs))
+def check_llm(llm_path=None, verbose=False):
+    """Check LLM path and perform a simple inference task."""
+    model_path = llm_path
+    if model_path is None:
+        print("Checking for INNOCUOUS_LLM_PATH environment variable...")
+        model_path = os.environ.get("INNOCUOUS_LLM_PATH")
+    else:
+        print(f"Using LLM path from argument: {llm_path}")
+
+    if model_path is None:
+        print("LLM path not found. Please supply --llm-path or set INNOCUOUS_LLM_PATH.")
+        return False
+    print(f"LLM path set to: {model_path}")
+
+    if not os.path.exists(model_path):
+        print(f"File not found at: {model_path}")
+        return False
+    print(f"LLM file found at: {model_path}")
+
+    try:
+        print("Attempting to load LLM...")
+        llm = create_llm_client(model_path=model_path)
+        print("LLM loaded successfully.")
+    except Exception as e:
+        print(f"Failed to load LLM: {e}")
+        return False
+
+    try:
+        print("Performing simple inference task...")
+        top_logprobs = get_token_probabilities(llm, "The king")
+        print("Inference task successful.")
+        if verbose:
+            print("Top log probabilities:")
+            top_logprobs = logits_to_probabilities(top_logprobs)
+            print(to_json(top_logprobs))
+    except Exception as e:
+        print(f"Inference task failed: {e}")
+        return False
+
+    return True
</pre>

<h3>Patch</h3>

<pre>
commit e7b8d5b3d0b5012a8243833850a213451e0381c2
Author: sutt <wsutton17@gmail.com>
Date:   Mon Aug 25 21:34:14 2025 -0400

    feat: add configurable LLM path and check-llm command

diff --git a/examples/bitcoin_address.py b/examples/bitcoin_address.py
index 802b901..a780811 100644
--- a/examples/bitcoin_address.py
+++ b/examples/bitcoin_address.py
@@ -1,11 +1,6 @@
-import os
-import psutil
-
 from stego_llm.crypto.bitcoin import get_p2pkh_addr_from_int
 from stego_llm.core import main_decode, main_encode
-from stego_llm.llm import create_llm_client
 
-process = psutil.Process(os.getpid())
 
 # Set the number of bits to encode per token
 CHUNK_SIZE = 2
@@ -13,21 +8,12 @@ CHUNK_SIZE = 2
 # Set the initial prompt
 INITIAL_PROMPT = "This is a test of the emergency broadcast system."
 
-
-def debug_memory():
-    """Debug memory usage."""
-    print(f"Memory usage: {process.memory_info().rss / 1024 / 1024} MB")
-
-
 if __name__ == "__main__":
-    llm = create_llm_client()
-    debug_memory()
     # Generate a random 256-bit integer
     private_key = 18594792834330697211246363334233653332223588226437428290993459238478563432123
 
     encoded_text = main_encode(
-        llm=llm,
         initial_prompt=INITIAL_PROMPT,
         msg=private_key.to_bytes(32, "big"),
         chunk_size=CHUNK_SIZE,
@@ -35,10 +21,8 @@ if __name__ == "__main__":
 
     print(f"Encoded text: {encoded_text}")
 
-    debug_memory()
     # Decode the private key from the encoded text
     decoded_private_key_bytes = main_decode(
-        llm=llm,
         encoded_prompt=encoded_text,
         initial_prompt=INITIAL_PROMPT,
         chunk_size=CHUNK_SIZE,
diff --git a/examples/custom_prompts.py b/examples/custom_prompts.py
index 228811c..870115c 100644
--- a/examples/custom_prompts.py
+++ b/examples/custom_prompts.py
@@ -1,7 +1,6 @@
 from stego_llm.core import main_decode, main_encode
-from stego_llm.llm import create_llm_client
 
-llm = create_llm_client()
+
 # Set the number of bits to encode per token
 CHUNK_SIZE = 2
 
@@ -10,7 +9,6 @@ MESSAGE = b"this is a custom prompt"
 
 # Encode the private key into the text
 encoded_text = main_encode(
-    llm=llm,
     initial_prompt=INITIAL_PROMPT,
     msg=MESSAGE,
     chunk_size=CHUNK_SIZE,
@@ -19,7 +17,6 @@
 print(f"Encoded text: {encoded_text}")
 
 decoded_bytes = main_decode(
-    llm=llm,
     encoded_prompt=encoded_text,
     initial_prompt=INITIAL_PROMPT,
     chunk_size=CHUNK_SIZE,
diff --git a/examples/random_data.py b/examples/random_data.py
index 228811c..870115c 100644
--- a/examples/random_data.py
+++ b/examples/random_data.py
@@ -1,7 +1,6 @@
 from stego_llm.core import main_decode, main_encode
-from stego_llm.llm import create_llm_client
 
-llm = create_llm_client()
+
 # Set the number of bits to encode per token
 CHUNK_SIZE = 2
 
@@ -10,7 +9,6 @@ MESSAGE = b"this is a custom prompt"
 
 # Encode the private key into the text
 encoded_text = main_encode(
-    llm=llm,
     initial_prompt=INITIAL_PROMPT,
     msg=MESSAGE,
     chunk_size=CHUNK_SIZE,
@@ -19,7 +17,6 @@
 print(f"Encoded text: {encoded_text}")
 
 decoded_bytes = main_decode(
-    llm=llm,
     encoded_prompt=encoded_text,
     initial_prompt=INITIAL_PROMPT,
     chunk_size=CHUNK_SIZE,
</pre>
</details>

#### `fix-tests.md`
- **Spec Summary:** *Update tests to pass after changes to create_llm_client import and function signature. Tests were failing because create_llm_client was moved from cli.py and the function interface changed to accept llm_path parameter.*
- **Commit Message:** *test: remove mock for moved create_llm_client function*
- **Task Notes:** Spec uses the dump stdout + git diff data, and generation solves it.
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-10
- **Spec:** fix-tests.md | **Patch Sha:** c7cdd56
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
Update the tests to pass for the following failures. 

The test previously passed before the changes listed below.

============================= test session starts ==============================
platform linux -- Python 3.12.11, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/user/dev/innocuous/demo-llama
configfile: pyproject.toml
testpaths: tests
plugins: mock-3.14.1
collected 21 items

tests/test_cli.py FFFFFFFFFFFF                                           [ 57%]
tests/test_simple.py .........                                           [100%]

=================================== FAILURES ===================================
_______________________________ test_encode_text _______________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f69993541a0>

    def test_encode_text(mocker):
        """Test encode command with --text."""
        mocker.patch("sys.argv", ["innocuous", "encode", "--text", "hello"])
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
>       mock_create_llm = mocker.patch("stego_llm.cli.create_llm_client")
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/test_cli.py:12: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6984ed7830>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
______________________________ test_encode_bytes _______________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6985559490>

    def test_encode_bytes(mocker):
        """Test encode command with --bytes."""
        mocker.patch(
            "sys.argv", ["innocuous", "encode", "--bytes", "68656c6c6f"]
        )  # "hello" in hex
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:28: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f699931d6a0>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_____________________________ test_encode_btc_addr _____________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f05d60>

    def test_encode_btc_addr(mocker):
        """Test encode command with --btc-addr."""
        addr = "bc1q..."
        mocker.patch("sys.argv", ["innocuous", "encode", "--btc-addr", addr])
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:42: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f698555b530>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_____________________________ test_decode_message ______________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f07890>

    def test_decode_message(mocker):
        """Test decode command with --message."""
        mocker.patch(
            "sys.argv", ["innocuous", "decode", "--message", "some encoded message"]
        )
        mock_main_decode = mocker.patch(
            "stego_llm.cli.main_decode", return_value=b"decoded"
        )
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:59: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f698555b170>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________________ test_decode_file _______________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f06f60>
tmp_path = PosixPath('/tmp/pytest-of-user/pytest-8/test_decode_file0')

    def test_decode_file(mocker, tmp_path):
        """Test decode command with --file."""
        p = tmp_path / "message.txt"
        p.write_text("file encoded message")
        mocker.patch("sys.argv", ["innocuous", "decode", "--file", str(p)])
        mock_main_decode = mocker.patch(
            "stego_llm.cli.main_decode", return_value=b"decoded"
        )
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:76: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6985765b80>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
___________________________ test_initial_prompt_text ___________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2a600>

    def test_initial_prompt_text(mocker):
        """Test --initial-prompt-text flag."""
        mocker.patch(
            "sys.argv",
            ["innocuous", "--initial-prompt-text", "my prompt", "encode", "--text", "t"],
        )
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:92: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f699bdcc470>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
___________________________ test_initial_prompt_file ___________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2d8b0>
tmp_path = PosixPath('/tmp/pytest-of-user/pytest-8/test_initial_prompt_file0')

    def test_initial_prompt_file(mocker, tmp_path):
        """Test --initial-prompt-file flag."""
        p = tmp_path / "prompt.txt"
        p.write_text("prompt from file")
        mocker.patch(
            "sys.argv",
            ["innocuous", "--initial-prompt-file", str(p), "encode", "--text", "t"],
        )
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:110: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f698555b710>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________________ test_chunk_size ________________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2df10>

    def test_chunk_size(mocker):
        """Test --chunk_size flag."""
        mocker.patch(
            "sys.argv", ["innocuous", "--chunk_size", "4", "encode", "--text", "t"]
        )
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:125: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6984f31970>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________ test_verbosity[verbose_arg0-30] ________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2d610>
verbose_arg = [], expected_level = 30

    @pytest.mark.parametrize(
        "verbose_arg, expected_level",
        [
            ([], logging.WARNING),
            (["-v"], logging.INFO),
            (["-vv"], logging.DEBUG),
            (["-vvv"], logging.DEBUG),
        ],
    )
    def test_verbosity(mocker, verbose_arg, expected_level):
        """Test verbosity flags."""
        argv = ["innocuous"] + verbose_arg + ["encode", "--text", "t"]
        mocker.patch("sys.argv", argv)
        mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6984f2c440>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________ test_verbosity[verbose_arg1-20] ________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2e9c0>
verbose_arg = ['-v'], expected_level = 20

    @pytest.mark.parametrize(
        "verbose_arg, expected_level",
        [
            ([], logging.WARNING),
            (["-v"], logging.INFO),
            (["-vv"], logging.DEBUG),
            (["-vvv"], logging.DEBUG),
        ],
    )
    def test_verbosity(mocker, verbose_arg, expected_level):
        """Test verbosity flags."""
        argv = ["innocuous"] + verbose_arg + ["encode", "--text", "t"]
        mocker.patch("sys.argv", argv)
        mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f699be35550>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________ test_verbosity[verbose_arg2-10] ________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2b6b0>
verbose_arg = ['-vv'], expected_level = 10

    @pytest.mark.parametrize(
        "verbose_arg, expected_level",
        [
            ([], logging.WARNING),
            (["-v"], logging.INFO),
            (["-vv"], logging.DEBUG),
            (["-vvv"], logging.DEBUG),
        ],
    )
    def test_verbosity(mocker, verbose_arg, expected_level):
        """Test verbosity flags."""
        argv = ["innocuous"] + verbose_arg + ["encode", "--text", "t"]
        mocker.patch("sys.argv", argv)
        mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6984f06f30>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________ test_verbosity[verbose_arg3-10] ________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f33710>
verbose_arg = ['-vvv'], expected_level = 10

    @pytest.mark.parametrize(
        "verbose_arg, expected_level",
        [
            ([], logging.WARNING),
            (["-v"], logging.INFO),
            (["-vv"], logging.DEBUG),
            (["-vvv"], logging.DEBUG),
        ],
    )
    def test_verbosity(mocker, verbose_arg, expected_level):
        """Test verbosity flags."""
        argv = ["innocuous"] + verbose_arg + ["encode", "--text", "t"]
        mocker.patch("sys.argv", argv)
        mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6984f8d910>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
=========================== short test summary info ============================
FAILED tests/test_cli.py::test_encode_text - AttributeError: <module 'stego_l...
FAILED tests/test_cli.py::test_encode_bytes - AttributeError: <module 'stego_...
FAILED tests/test_cli.py::test_encode_btc_addr - AttributeError: <module 'ste...
FAILED tests/test_cli.py::test_decode_message - AttributeError: <module 'steg...
FAILED tests/test_cli.py::test_decode_file - AttributeError: <module 'stego_l...
FAILED tests/test_cli.py::test_initial_prompt_text - AttributeError: <module ...
FAILED tests/test_cli.py::test_initial_prompt_file - AttributeError: <module ...
FAILED tests/test_cli.py::test_chunk_size - AttributeError: <module 'stego_ll...
FAILED tests/test_cli.py::test_verbosity[verbose_arg0-30] - AttributeError: <...
FAILED tests/test_cli.py::test_verbosity[verbose_arg1-20] - AttributeError: <...
FAILED tests/test_cli.py::test_verbosity[verbose_arg2-10] - AttributeError: <...
FAILED tests/test_cli.py::test_verbosity[verbose_arg3-10] - AttributeError: <...
========================= 12 failed, 9 passed in 0.93s =========================

Changes that caused the test failure.


commit 55cf7ce3a3b6910826b0c267cc517fad792c08aa
Author: sutt <wsutton17@gmail.com>
Date:   Mon Aug 25 20:39:12 2025 -0400

    feat: allow specifying LLM path via CLI arg or env var

diff --git a/stego_llm/cli.py b/stego_llm/cli.py
index 7f3653f..16569bf 100644
--- a/stego_llm/cli.py
+++ b/stego_llm/cli.py
@@ -4,7 +4,6 @@ import sys
 from pathlib import Path
 
 from stego_llm.core import main_decode, main_encode
-from stego_llm.llm import create_llm_client
 
 logger = logging.getLogger(__name__)
 
@@ -15,6 +14,7 @@ def main():
     parser.add_argument(
         "-v", "--verbose", action="count", default=0, help="Increase verbosity"
     )
+    parser.add_argument("--llm-path", type=Path, help="Path to LLM GGUF file")
     parser.add_argument(
         "--chunk_size", type=int, default=3, help="Chunk size for encoding/decoding"
     )
@@ -75,13 +75,12 @@ def main():
         elif args.btc_addr:
             message_bytes = args.btc_addr.encode("utf-8")
 
-        llm = create_llm_client()
         encoded_message = main_encode(
-            llm=llm,
             initial_prompt=initial_prompt,
             msg=message_bytes,
             chunk_size=args.chunk_size,
             num_logprobs=num_logprobs,
+            llm_path=args.llm_path,
         )
         print(encoded_message)
 
@@ -92,13 +91,12 @@ def main():
         elif args.file:
             encoded_text = args.file.read_text()
 
-        llm = create_llm_client()
         decoded_bytes = main_decode(
-            llm=llm,
             encoded_prompt=encoded_text,
             initial_prompt=initial_prompt,
             chunk_size=args.chunk_size,
             num_logprobs=num_logprobs,
+            llm_path=args.llm_path,
         )
         print(repr(decoded_bytes))
 
diff --git a/stego_llm/core/decoder.py b/stego_llm/core/decoder.py
index a8f6045..5b20748 100644
--- a/stego_llm/core/decoder.py
+++ b/stego_llm/core/decoder.py
@@ -5,7 +5,11 @@ from stego_llm.steganography import (
     pre_selection_filter,
     post_selection_filter,
 )
-from stego_llm.llm import get_token_probabilities, logits_to_probabilities
+from stego_llm.llm import (
+    create_llm_client,
+    get_token_probabilities,
+    logits_to_probabilities,
+)
 from .trace import _trace_decoding_step
 
 
@@ -13,13 +17,14 @@ logger = logging.getLogger(__name__)
 
 
 def main_decode(
-    llm,
     encoded_prompt,
     initial_prompt,
     chunk_size,
     num_logprobs,
+    llm_path=None,
 ):
     """Main decoding function for steganographic message extraction."""
+    llm = create_llm_client(model_path=llm_path)
     message_carrying_text = encoded_prompt[len(initial_prompt) :]
     memo = {}
 
diff --git a/stego_llm/core/encoder.py b/stego_llm/core/encoder.py
index 3cf5a44..4b6e5ea 100644
--- a/stego_llm/core/encoder.py
+++ b/stego_llm/core/encoder.py
@@ -5,7 +5,11 @@ from stego_llm.steganography import (
     pre_selection_filter,
     post_selection_filter,
 )
-from stego_llm.llm import get_token_probabilities, logits_to_probabilities
+from stego_llm.llm import (
+    create_llm_client,
+    get_token_probabilities,
+    logits_to_probabilities,
+)
 from .trace import _trace_encoding_step
 
 
@@ -13,13 +17,14 @@ logger = logging.getLogger(__name__)
 
 
 def main_encode(
-    llm,
     initial_prompt,
     msg,
     chunk_size,
     num_logprobs,
+    llm_path=None,
 ):
     """Main encoding function for steganographic text generation."""
+    llm = create_llm_client(model_path=llm_path)
     enc_ints = message_to_chunks(msg, chunk_size=chunk_size)
     current_prompt = initial_prompt
 
diff --git a/stego_llm/llm/interface.py b/stego_llm/llm/interface.py
index 81a28a0..31e2828 100644
--- a/stego_llm/llm/interface.py
+++ b/stego_llm/llm/interface.py
@@ -1,4 +1,5 @@
 import json
+import os
 import numpy as np
 from llama_cpp import Llama
 from .utilities import suppress_stderr, logits_to_probabilities, to_json
@@ -6,9 +7,14 @@ from .utilities import suppress_stderr, logits_to_probabilities, to_json
 
 @suppress_stderr
 def create_llm_client(
-    model_path="/home/user/dev/innocuous/data/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
+    model_path=None,
 ):
     """Initialize and return a Llama LLM client."""
+    if model_path is None:
+        model_path = os.environ.get(
+            "INNOCUOUS_LLM_PATH",
+            "/home/user/dev/innocuous/data/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
+        )
     return Llama(
         model_path=model_path,
         logits_all=True,
</pre>

<h3>Patch</h3>

<pre>
commit c7cdd56fe1a1908cb22591e1fa8acf7f56575257
Author: sutt <wsutton17@gmail.com>
Date:   Mon Aug 25 21:16:33 2025 -0400

    test: remove mock for moved create_llm_client function

diff --git a/tests/test_cli.py b/tests/test_cli.py
index 19d3406..6b870c8 100644
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -9,12 +9,10 @@ def test_encode_text(mocker):
     """Test encode command with --text."""
     mocker.patch("sys.argv", ["innocuous", "encode", "--text", "hello"])
     mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
-    mock_create_llm = mocker.patch("stego_llm.cli.create_llm_client")
     mocker.patch("builtins.print")
 
     cli.main()
 
-    mock_create_llm.assert_called_once()
     mock_main_encode.assert_called_once()
     assert mock_main_encode.call_args.kwargs["msg"] == b"hello"
 
@@ -25,7 +23,6 @@ def test_encode_bytes(mocker):
         "sys.argv", ["innocuous", "encode", "--bytes", "68656c6c6f"]
     )  # "hello" in hex
     mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
-    mocker.patch("stego_llm.cli.create_llm_client")
     mocker.patch("builtins.print")
 
     cli.main()
@@ -39,7 +36,6 @@ def test_encode_btc_addr(mocker):
     addr = "bc1q..."
     mocker.patch("sys.argv", ["innocuous", "encode", "--btc-addr", addr])
     mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
-    mocker.patch("stego_llm.cli.create_llm_client")
     mocker.patch("builtins.print")
 
     cli.main()
@@ -56,7 +52,6 @@ def test_decode_message(mocker):
     mock_main_decode = mocker.patch(
         "stego_llm.cli.main_decode", return_value=b"decoded"
     )
-    mocker.patch("stego_llm.cli.create_llm_client")
     mocker.patch("builtins.print")
 
     cli.main()
@@ -73,7 +68,6 @@ def test_decode_file(mocker, tmp_path):
     mock_main_decode = mocker.patch(
         "stego_llm.cli.main_decode", return_value=b"decoded"
     )
-    mocker.patch("stego_llm.cli.create_llm_client")
     mocker.patch("builtins.print")
 
     cli.main()
@@ -89,7 +83,6 @@ def test_initial_prompt_text(mocker):
         ["innocuous", "--initial-prompt-text", "my prompt", "encode", "--text", "t"],
     )
     mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
-    mocker.patch("stego_llm.cli.create_llm_client")
     mocker.patch("builtins.print")
 
     cli.main()
@@ -107,7 +100,6 @@ def test_initial_prompt_file(mocker, tmp_path):
         ["innocuous", "--initial-prompt-file", str(p), "encode", "--text", "t"],
     )
     mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
-    mocker.patch("stego_llm.cli.create_llm_client")
     mocker.patch("builtins.print")
 
     cli.main()
@@ -122,7 +114,6 @@ def test_chunk_size(mocker):
         "sys.argv", ["innocuous", "--chunk_size", "4", "encode", "--text", "t"]
     )
     mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
-    mocker.patch("stego_llm.cli.create_llm_client")
     mocker.patch("builtins.print")
 
     cli.main()
@@ -145,7 +136,6 @@ def test_verbosity(mocker, verbose_arg, expected_level):
     argv = ["innocuous"] + verbose_arg + ["encode", "--text", "t"]
     mocker.patch("sys.argv", argv)
     mocker.patch("stego_llm.cli.main_encode")
-    mocker.patch("stego_llm.cli.create_llm_client")
     mock_basic_config = mocker.patch("logging.basicConfig")
     mocker.patch("builtins.print")
 
</pre>
</details>

#### `check-llm.md`
- **Spec Summary:** *Add subcommand "check-llm" and exportable function "check_llm" to verify LLM path from CLI/env var, check file existence, and execute simple inference task. Print terse confirmation of each step.*
- **Commit Message:** *feat: add check-llm subcommand to validate LLM configuration*
- **Task Notes:** Generation followed multiple separate instructions well.
- **Src Diffs:** +51/-9 | **Test Diffs:** +38/-0
- **Spec:** check-llm.md | **Patch Sha:** 0355954
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
add a subcommand to the script "check-llm"
add an exportable function "check_llm"
running this command or function should:
check if llm_path is supplied either via cli or env var,
if so, it checks if the file exists
and if so, attempts to execute a simple inference task with the llm, you can use the llm.interface:demo function for this with the nec modifications to use env/cli arg to pass to create_llm_client. Don't print the logprobs by default but only in the case verbose (-vv) is invoked.

Printout a terse confirmation of each step.

Add some tests for loading llm-path from cli/env and running this subcommand.
</pre>

<h3>Patch</h3>

<pre>
commit 0355954117ebacdbc0395cffb531f59f9b553045
Author: sutt <wsutton17@gmail.com>
Date:   Mon Aug 25 21:27:09 2025 -0400

    feat: add check-llm subcommand to validate LLM configuration

diff --git a/stego_llm/__init__.py b/stego_llm/__init__.py
index debb3ff..739b68f 100644
--- a/stego_llm/__init__.py
+++ b/stego_llm/__init__.py
@@ -5,6 +5,7 @@ A library for embedding and extracting hidden messages in LLM-generated text.
 """
 
 from .core import main_encode, main_decode
+from .llm import check_llm
 
-__all__ = ["main_encode", "main_decode"]
+__all__ = ["main_encode", "main_decode", "check_llm"]
 __version__ = "0.1.0"
diff --git a/stego_llm/cli.py b/stego_llm/cli.py
index 16569bf..e97194c 100644
--- a/stego_llm/cli.py
+++ b/stego_llm/cli.py
@@ -4,6 +4,7 @@ import sys
 from pathlib import Path
 
 from stego_llm.core import main_decode, main_encode
+from stego_llm.llm import check_llm
 
 logger = logging.getLogger(__name__)
 
@@ -43,6 +44,9 @@ def main():
         "--file", type=Path, help="Path to file with message to decode"
     )
 
+    # Check LLM command
+    subparsers.add_parser("check-llm", help="Check LLM configuration")
+
     args = parser.parse_args()
 
     log_level = logging.WARNING
@@ -100,6 +104,9 @@ def main():
         )
         print(repr(decoded_bytes))
 
+    elif args.command == "check-llm":
+        check_llm(llm_path=args.llm_path, verbose=args.verbose >= 2)
+
 
 if __name__ == "__main__":
     main()
diff --git a/stego_llm/llm/__init__.py b/stego_llm/llm/__init__.py
index 428debf..4e370e4 100644
--- a/stego_llm/llm/__init__.py
+++ b/stego_llm/llm/__init__.py
@@ -1,4 +1,4 @@
-from .interface import create_llm_client, get_token_probabilities
+from .interface import create_llm_client, get_token_probabilities, check_llm
 from .utilities import logits_to_probabilities, to_json
 
 __all__ = [
@@ -6,4 +6,5 @@ __all__ = [
     "get_token_probabilities",
     "logits_to_probabilities",
     "to_json",
+    "check_llm",
 ]
diff --git a/stego_llm/llm/interface.py b/stego_llm/llm/interface.py
index e81d084..5a9dc2f 100644
--- a/stego_llm/llm/interface.py
+++ b/stego_llm/llm/interface.py
@@ -33,10 +33,43 @@ def get_token_probabilities(llm, prompt, num_output=10):
     return top_logprobs
 
 
-def demo():
-    """Demo function showing basic LLM usage."""
-    # TODO - add this cli status check command
-    llm = create_llm_client()
-    top_logprobs = get_token_probabilities(llm)
-    top_logprobs = logits_to_probabilities(top_logprobs)
-    print(to_json(top_logprobs))
+def check_llm(llm_path=None, verbose=False):
+    """Check LLM path and perform a simple inference task."""
+    model_path = llm_path
+    if model_path is None:
+        print("Checking for INNOCUOUS_LLM_PATH environment variable...")
+        model_path = os.environ.get("INNOCUOUS_LLM_PATH")
+    else:
+        print(f"Using LLM path from argument: {llm_path}")
+
+    if model_path is None:
+        print("LLM path not found. Please supply --llm-path or set INNOCUOUS_LLM_PATH.")
+        return False
+    print(f"LLM path set to: {model_path}")
+
+    if not os.path.exists(model_path):
+        print(f"File not found at: {model_path}")
+        return False
+    print(f"LLM file found at: {model_path}")
+
+    try:
+        print("Attempting to load LLM...")
+        llm = create_llm_client(model_path=model_path)
+        print("LLM loaded successfully.")
+    except Exception as e:
+        print(f"Failed to load LLM: {e}")
+        return False
+
+    try:
+        print("Performing simple inference task...")
+        top_logprobs = get_token_probabilities(llm, "The king")
+        print("Inference task successful.")
+        if verbose:
+            print("Top log probabilities:")
+            top_logprobs = logits_to_probabilities(top_logprobs)
+            print(to_json(top_logprobs))
+    except Exception as e:
+        print(f"Inference task failed: {e}")
+        return False
+
+    return True
diff --git a/tests/test_cli.py b/tests/test_cli.py
index 6b870c8..e3fd5dd 100644
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -143,3 +143,41 @@ def test_verbosity(mocker, verbose_arg, expected_level):
 
     mock_basic_config.assert_called_once()
     assert mock_basic_config.call_args.kwargs["level"] == expected_level
+
+
+def test_check_llm_path(mocker):
+    """Test check-llm command with --llm-path."""
+    mocker.patch("sys.argv", ["innocuous", "--llm-path", "fake.gguf", "check-llm"])
+    mock_check_llm = mocker.patch("stego_llm.cli.check_llm")
+
+    cli.main()
+
+    mock_check_llm.assert_called_once()
+    assert mock_check_llm.call_args.kwargs["llm_path"] is not None
+    assert str(mock_check_llm.call_args.kwargs["llm_path"]) == "fake.gguf"
+    assert not mock_check_llm.call_args.kwargs["verbose"]
+
+
+def test_check_llm_env(mocker):
+    """Test check-llm command with env var."""
+    mocker.patch.dict("os.environ", {"INNOCUOUS_LLM_PATH": "fake.gguf"})
+    mocker.patch("sys.argv", ["innocuous", "check-llm"])
+    mock_check_llm = mocker.patch("stego_llm.cli.check_llm")
+
+    cli.main()
+
+    mock_check_llm.assert_called_once()
+    assert mock_check_llm.call_args.kwargs["llm_path"] is None
+    assert not mock_check_llm.call_args.kwargs["verbose"]
+
+
+def test_check_llm_verbose(mocker):
+    """Test check-llm command with verbosity."""
+    mocker.patch("sys.argv", ["innocuous", "-vv", "check-llm"])
+    mock_check_llm = mocker.patch("stego_llm.cli.check_llm")
+
+    cli.main()
+
+    mock_check_llm.assert_called_once()
+    assert mock_check_llm.call_args.kwargs["llm_path"] is None
+    assert mock_check_llm.call_args.kwargs["verbose"]
</pre>
</details>

#### `modelpath-env.md`
- **Spec Summary:** *In llm.interface:create_llm_client have model_path load from env var "INNOCUOUS_LLM_PATH". Add optional CLI arg and function args to override env var.*
- **Commit Message:** *feat: allow specifying LLM path via CLI arg or env var*
- **Task Notes:** Two small mistakes in the genration as seen in the subsequent commit.
- **Src Diffs:** +24/-10 | **Test Diffs:** +0/-0
- **Spec:** modelpath-env.md | **Patch Sha:** 55cf7ce
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
in llm.interface:create_llm_client
have the model_path arg load from an env var "INNOCUOUS_LLM_PATH"
- on the cli add an optional arg to pass the 
- add an optional arg "llm_path" to main_decode and main_encode 
- the cli arg and function arg should override the env var if both are present
</pre>

<h3>Patch</h3>

<pre>
commit 55cf7ce3a3b6910826b0c267cc517fad792c08aa
Author: sutt <wsutton17@gmail.com>
Date:   Mon Aug 25 20:39:12 2025 -0400

    feat: allow specifying LLM path via CLI arg or env var

diff --git a/stego_llm/cli.py b/stego_llm/cli.py
index 7f3653f..16569bf 100644
--- a/stego_llm/cli.py
+++ b/stego_llm/cli.py
@@ -4,7 +4,6 @@ import sys
 from pathlib import Path
 
 from stego_llm.core import main_decode, main_encode
-from stego_llm.llm import create_llm_client
 
 logger = logging.getLogger(__name__)
 
@@ -15,6 +14,7 @@ def main():
     parser.add_argument(
         "-v", "--verbose", action="count", default=0, help="Increase verbosity"
     )
+    parser.add_argument("--llm-path", type=Path, help="Path to LLM GGUF file")
     parser.add_argument(
         "--chunk_size", type=int, default=3, help="Chunk size for encoding/decoding"
     )
@@ -75,13 +75,12 @@ def main():
         elif args.btc_addr:
             message_bytes = args.btc_addr.encode("utf-8")
 
-        llm = create_llm_client()
         encoded_message = main_encode(
-            llm=llm,
             initial_prompt=initial_prompt,
             msg=message_bytes,
             chunk_size=args.chunk_size,
             num_logprobs=num_logprobs,
+            llm_path=args.llm_path,
         )
         print(encoded_message)
 
@@ -92,13 +91,12 @@ def main():
         elif args.file:
             encoded_text = args.file.read_text()
 
-        llm = create_llm_client()
         decoded_bytes = main_decode(
-            llm=llm,
             encoded_prompt=encoded_text,
             initial_prompt=initial_prompt,
             chunk_size=args.chunk_size,
             num_logprobs=num_logprobs,
+            llm_path=args.llm_path,
         )
         print(repr(decoded_bytes))
 
diff --git a/stego_llm/core/decoder.py b/stego_llm/core/decoder.py
index a8f6045..5b20748 100644
--- a/stego_llm/core/decoder.py
+++ b/stego_llm/core/decoder.py
@@ -5,7 +5,11 @@ from stego_llm.steganography import (
     pre_selection_filter,
     post_selection_filter,
 )
-from stego_llm.llm import get_token_probabilities, logits_to_probabilities
+from stego_llm.llm import (
+    create_llm_client,
+    get_token_probabilities,
+    logits_to_probabilities,
+)
 from .trace import _trace_decoding_step
 
 
@@ -13,13 +17,14 @@ logger = logging.getLogger(__name__)
 
 
 def main_decode(
-    llm,
     encoded_prompt,
     initial_prompt,
     chunk_size,
     num_logprobs,
+    llm_path=None,
 ):
     """Main decoding function for steganographic message extraction."""
+    llm = create_llm_client(model_path=llm_path)
     message_carrying_text = encoded_prompt[len(initial_prompt) :]
     memo = {}
 
diff --git a/stego_llm/core/encoder.py b/stego_llm/core/encoder.py
index 3cf5a44..4b6e5ea 100644
--- a/stego_llm/core/encoder.py
+++ b/stego_llm/core/encoder.py
@@ -5,7 +5,11 @@ from stego_llm.steganography import (
     pre_selection_filter,
     post_selection_filter,
 )
-from stego_llm.llm import get_token_probabilities, logits_to_probabilities
+from stego_llm.llm import (
+    create_llm_client,
+    get_token_probabilities,
+    logits_to_probabilities,
+)
 from .trace import _trace_encoding_step
 
 
@@ -13,13 +17,14 @@ logger = logging.getLogger(__name__)
 
 
 def main_encode(
-    llm,
     initial_prompt,
     msg,
     chunk_size,
     num_logprobs,
+    llm_path=None,
 ):
     """Main encoding function for steganographic text generation."""
+    llm = create_llm_client(model_path=llm_path)
     enc_ints = message_to_chunks(msg, chunk_size=chunk_size)
     current_prompt = initial_prompt
 
diff --git a/stego_llm/llm/interface.py b/stego_llm/llm/interface.py
index 81a28a0..31e2828 100644
--- a/stego_llm/llm/interface.py
+++ b/stego_llm/llm/interface.py
@@ -1,4 +1,5 @@
 import json
+import os
 import numpy as np
 from llama_cpp import Llama
 from .utilities import suppress_stderr, logits_to_probabilities, to_json
@@ -6,9 +7,14 @@ from .utilities import suppress_stderr, logits_to_probabilities, to_json
 
 @suppress_stderr
 def create_llm_client(
-    model_path="/home/user/dev/innocuous/data/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
+    model_path=None,
 ):
     """Initialize and return a Llama LLM client."""
+    if model_path is None:
+        model_path = os.environ.get(
+            "INNOCUOUS_LLM_PATH",
+            "/home/user/dev/innocuous/data/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
+        )
     return Llama(
         model_path=model_path,
         logits_all=True,
</pre>
</details>

#### `devsummary-task-b.md`
- **Spec Summary:** *Update table in docs/dev-summary.md for v0.1.0 with git diff values for code changes columns. Each value represented as "+A/-D" format for additions/deletions from git diff --stat.*
- **Commit Message:** *feat: impl devsummary-task-b with claude (agro auto-commit)*
- **Task Notes:** Modfied this script to be a little more complicated and factor in multiple slices of repo
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-0
- **Spec:** devsummary-task-b.md | **Patch Sha:** d3321ed
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
### Script Vars
Utilize these variables below for the task as you read it and process it. The script var will be denoted with $my_script_var when utilized and should be read the value corresponding.

- target_doc: docs/dev-summary.md 
- version_to_update: v0.2.3
- diffs_main_directory: stego_llm
- diffs_on_other_directories: tests

### Steps to Update & Execute this Spec
This section should be ignored by the AI agent; it's for the developer's reference to edit this file for:
Updating:
- Update the variables in script vars:
    - the diffs vars are helpful for different repo setups
Executing:
- Claude excels at this task.
- Enable the `Bash(git:*)` permissions for the claude agent.

### Task
These are the instructions for your task. Remember to insert the script vars from above when seeing a variable preseeded by $.
update the table in $target_doc:
- update the table for $version_to_update
- add values for all (or some of) the "code changes" / "diffs" columns:
    - use the column name to understand which slices of the codebase should be considered for the diffs.
    - these code diffs should only apply to the particular git commit referenced in that row of the table (it should not be the total diffs over the whole version)
    - for the first diff column, use the diffs from within directory $diff_main_directory
    - for the second diff column, use the the diffs from within directory $diff_on_other_directories
- each value should be represented as "+A/-D" where A is the number of additions and -D is deletion or modifications from a git diff / git diff --stat,
    - e.g. "+23/-12", or "+5/-0"

Use git commands to investigate these commit shas and run git diffs that will allows you to fill in the full table.

Rules used to build the table previously:
- only include specs/* files for rows
- sort by date order desc (the date information will supplied at the end)

Reference for commit sha's in the table
```
04d2537 build: v0.2.3
222a1ca specs: v0.2.3
f01571c docs: update dev-summary for 0.2.1 and 0.2.2
b7c73e9 refactor: ruff format
9abdb61 test: add tests for llm_extra_args passthrough
2f85f37 feat: adding llm_extra_args for use in library functions
deac5b5 refactor: llama logging override now wrapped as function
77a030d refactor: cli arguments --chunk-size
cbc0de0 refactor: logging enables info level, repr of output for -v mode.
fe8dbf6 feat: add --num-logprobs argument to CLI
313efe3 fix: cli defaults to chunk_size=2 (aligns with library method defaults)
5b23579 feat: decoder fills in missing auto_accept tokens + debugging trace for decoder
711aea0 test: add sleep + gc fixture to integration test setup
f57aea1 test: refactor previous test, add decoder-only integration test
6203b4a test: add integration test for full encode/decode cycle
ddcd740 fix: add default arg vals
b00dd60 refactor: add type hints and improve docstrings for core functions
80791f9 feat: add --version flag and dynamic version loading
1505e99 build: bump version v0.2.2
```
</pre>

<h3>Patch</h3>

<pre>
commit d3321ed199215c9833251a3a0b53b8a84145105a
Author: sutt <wsutton17@gmail.com>
Date:   Mon Aug 25 15:12:20 2025 -0400

    feat: impl devsummary-task-b with claude (agro auto-commit)

diff --git a/docs/dev-summary.md b/docs/dev-summary.md
index 4a3c93a..1333c00 100644
--- a/docs/dev-summary.md
+++ b/docs/dev-summary.md
@@ -18,10 +18,10 @@
 | Taskfile | Summary | Commit | Non-test Diffs |
 |---|---|---|---|
-| [prepost-filter-decode.md](/.public-agdocs/specs/prepost-filter-decode.md) | Apply refactor of filter_tok logic to pre_accept_filter + post_accept_filter functions in src/main:main_decode. Allow main_decode to take into account same logic so decoded data matches input. Functions will be extended with additional details. | [960c697](https://github.com/sutt/innocuous/commit/960c697) | |
-| [decode-accept-1.md](/.public-agdocs/specs/decode-accept-1.md) | Apply the accept_tok logic that was added to main_encode to main_decode. Use partial diff showing function usage. Allow main_decode to take into account same logic so decoded data matches input. Accept_tok will be extended with additional details. | [79a4c67](https://github.com/sutt/innocuous/commit/79a4c67) | |
-| [decode-branch.md](/.public-agdocs/specs/decode-branch.md) | Refactor decode_main function to handle situation where remaining_text may .startswith match with multiple eligible tokens. Need branching to check maxsize of first 2**chunk_size tokens after tok_filter. Apply hacky solution for now. | [cdabc98](https://github.com/sutt/innocuous/commit/cdabc98) | |
-| [decode1.md](/.public-agdocs/specs/decode1.md) | In src/main.py implement main_decode | [d4dd55e](https://github.com/sutt/innocuous/commit/d4dd55e) | |
+| [prepost-filter-decode.md](/.public-agdocs/specs/prepost-filter-decode.md) | Apply refactor of filter_tok logic to pre_accept_filter + post_accept_filter functions in src/main:main_decode. Allow main_decode to take into account same logic so decoded data matches input. Functions will be extended with additional details. | [960c697](https://github.com/sutt/innocuous/commit/960c697) | +2/-0 |
+| [decode-accept-1.md](/.public-agdocs/specs/decode-accept-1.md) | Apply the accept_tok logic that was added to main_encode to main_decode. Use partial diff showing function usage. Allow main_decode to take into account same logic so decoded data matches input. Accept_tok will be extended with additional details. | [79a4c67](https://github.com/sutt/innocuous/commit/79a4c67) | +14/-0 |
+| [decode-branch.md](/.public-agdocs/specs/decode-branch.md) | Refactor decode_main function to handle situation where remaining_text may .startswith match with multiple eligible tokens. Need branching to check maxsize of first 2**chunk_size tokens after tok_filter. Apply hacky solution for now. | [cdabc98](https://github.com/sutt/innocuous/commit/cdabc98) | +48/-25 |
+| [decode1.md](/.public-agdocs/specs/decode1.md) | In src/main.py implement main_decode | [d4dd55e](https://github.com/sutt/innocuous/commit/d4dd55e) | +43/-4 |
 
 ---
 
</pre>
</details>

#### `devsummary-task-a.md`
- **Spec Summary:** *Add updated taskfiles to markdown table in docs/dev-summary.md for v0.1.0 with filename, summary, and GitHub SHA links. Sort by date descending and include only specs/* files.*
- **Commit Message:** *feat: impl devsummary-task-a with claude (agro auto-commit)*
- **Task Notes:** Modified this script to be re-useable for each new version.
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-0
- **Spec:** devsummary-task-a.md | **Patch Sha:** 9f91a82
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
### Script Vars
Utilize these variables below for the task as you read it and process it. The script var will be denoted with $my_script_var when utilized and should be read the value corresponding.

- target_doc: docs/dev-summary.md 
- version_to_update: v0.2.3
- max_summary_chars: 250
- repo_url: github.com/sutt/innocuous

### Steps to Update & Execute this Spec
This section should be ignored by the AI agent; it's for the developer's reference to edit this file for:
Updating:
- Update the variables in script vars
- Run the 3 reference commands and add output to the sections "Command Outputs".
Executing:
- Claude often excels at this task
- Descriptive commit messages are helpful; multiple commit messages with same verbiage can confuse it.

### Command Reference:
These commands you should not run or pay attention to any of these. They are simply are reference for the developer:
> git diff --stat v0.2.2 v0.2.3 -- .public-agdocs/specs
> ls -lt .agdocs/specs/ 
> git log --oneline --no-merges  --not  -n 36

### Task
These are the instructions for your task. Remember to insert the script vars from above when seeing avariable preseeded by $.

Add the updated taskfiles to a markdown table in $target_doc 
for $version_to_update with a row containing:
- just the filename and have it be linked with relative path notation to where it resides in .public-agdocs
- a summary of the files contents (max $max_summary_chars chars)
- add a field that links to a 6-char git sha entry  on the github repo: $repo_url. Do your best guess to find the corresponding commit (available with commit message below). If your guess is too uncertain, or it appears there is no commit for it, place an n/a for this entry.

Rules for the table:
- only include specs/* files for rows
- sort by date order desc (the date information will supplied at the end)
- don't update the rightmost three columns ("diffs" + "notes"). These values will be supplied in a later task.

#### Command Outputs

##### Spec Changes
Here's the result for the following command:

git diff --stat v0.2.2 v0.2.3 -- .public-agdocs/specs

 .public-agdocs/specs/cli-numlogprobs.md   |  1 +
 .public-agdocs/specs/extra-args-test.md   | 92 +++++++++++++++++++++++++++++++
 .public-agdocs/specs/integration-test.md  |  3 +
 .public-agdocs/specs/type-main-funcs.md   |  6 ++
 .public-agdocs/specs/version-cmd.md       |  1 +
 7 files changed, 175 insertions(+), 84 deletions(-)



##### Specs Time-Sorted
Here's the information for the date created which should be used to sort the rows for the table above.

Results of the command: 

ls -lt .agdocs/specs/ 

-rw-r--r-- 1 user user  3348 Sep 11 12:10 extra-args-test.md
-rw-r--r-- 1 user user    81 Sep 11 08:32 cli-numlogprobs.md
-rw-r--r-- 1 user user   251 Sep  4 16:26 integration-test.md
-rw-r--r-- 1 user user   169 Sep  3 19:16 type-main-funcs.md
-rw-r--r-- 1 user user   104 Sep  3 18:46 version-cmd.md


##### Commit Logs
Here's the output of the following command, use this to link a solution sha to a task file

git log --oneline --no-merges  --not  -n 36

04d2537 build: v0.2.3
222a1ca specs: v0.2.3
f01571c docs: update dev-summary for 0.2.1 and 0.2.2
b7c73e9 refactor: ruff format
9abdb61 test: add tests for llm_extra_args passthrough
2f85f37 feat: adding llm_extra_args for use in library functions
deac5b5 refactor: llama logging override now wrapped as function
77a030d refactor: cli arguments --chunk-size
cbc0de0 refactor: logging enables info level, repr of output for -v mode.
fe8dbf6 feat: add --num-logprobs argument to CLI
313efe3 fix: cli defaults to chunk_size=2 (aligns with library method defaults)
5b23579 feat: decoder fills in missing auto_accept tokens + debugging trace for decoder
711aea0 test: add sleep + gc fixture to integration test setup
f57aea1 test: refactor previous test, add decoder-only integration test
6203b4a test: add integration test for full encode/decode cycle
ddcd740 fix: add default arg vals
b00dd60 refactor: add type hints and improve docstrings for core functions
80791f9 feat: add --version flag and dynamic version loading
1505e99 build: bump version v0.2.2
</pre>

<h3>Patch</h3>

<pre>
commit 9f91a8233b68b6519f1a5b3833233a7f78f0a18f
Author: sutt <wsutton17@gmail.com>
Date:   Mon Aug 25 15:12:09 2025 -0400

    feat: impl devsummary-task-a with claude (agro auto-commit)

diff --git a/docs/dev-summary.md b/docs/dev-summary.md
index 1333c00..4a3c93a 100644
--- a/docs/dev-summary.md
+++ b/docs/dev-summary.md
@@ -18,10 +18,10 @@
 | Taskfile | Summary | Commit | Non-test Diffs |
 |---|---|---|---|
-| [prepost-filter-decode.md](/.public-agdocs/specs/prepost-filter-decode.md) | Apply refactor of filter_tok logic to pre_accept_filter + post_accept_filter functions in src/main:main_decode. Allow main_decode to take into account same logic so decoded data matches input. Functions will be extended with additional details. | [960c697](https://github.com/sutt/innocuous/commit/960c697) | +2/-0 |
-| [decode-accept-1.md](/.public-agdocs/specs/decode-accept-1.md) | Apply the accept_tok logic that was added to main_encode to main_decode. Use partial diff showing function usage. Allow main_decode to take into account same logic so decoded data matches input. Accept_tok will be extended with additional details. | [79a4c67](https://github.com/sutt/innocuous/commit/79a4c67) | +14/-0 |
-| [decode-branch.md](/.public-agdocs/specs/decode-branch.md) | Refactor decode_main function to handle situation where remaining_text may .startswith match with multiple eligible tokens. Need branching to check maxsize of first 2**chunk_size tokens after tok_filter. Apply hacky solution for now. | [cdabc98](https://github.com/sutt/innocuous/commit/cdabc98) | +48/-25 |
-| [decode1.md](/.public-agdocs/specs/decode1.md) | In src/main.py implement main_decode | [d4dd55e](https://github.com/sutt/innocuous/commit/d4dd55e) | +43/-4 |
+| [prepost-filter-decode.md](/.public-agdocs/specs/prepost-filter-decode.md) | Apply refactor of filter_tok logic to pre_accept_filter + post_accept_filter functions in src/main:main_decode. Allow main_decode to take into account same logic so decoded data matches input. Functions will be extended with additional details. | [960c697](https://github.com/sutt/innocuous/commit/960c697) |
+| [decode-accept-1.md](/.public-agdocs/specs/decode-accept-1.md) | Apply the accept_tok logic that was added to main_encode to main_decode. Use partial diff showing function usage. Allow main_decode to take into account same logic so decoded data matches input. Accept_tok will be extended with additional details. | [79a4c67](https://github.com/sutt/innocuous/commit/79a4c67) |
+| [decode-branch.md](/.public-agdocs/specs/decode-branch.md) | Refactor decode_main function to handle situation where remaining_text may .startswith match with multiple eligible tokens. Need branching to check maxsize of first 2**chunk_size tokens after tok_filter. Apply hacky solution for now. | [cdabc98](https://github.com/sutt/innocuous/commit/cdabc98) |
+| [decode1.md](/.public-agdocs/specs/decode1.md) | In src/main.py implement main_decode | [d4dd55e](https://github.com/sutt/innocuous/commit/d4dd55e) |
 
 ---
 
</pre>
</details>

#### `cli-add.md`
- **Spec Summary:** *Add CLI interface for stego-llm package with script "innocuous" having encode/decode subcommands. Include optional flags for verbosity, chunk size, and initial prompt options. Create tests for functionality.*
- **Commit Message:** *feat: add innocuous command-line interface*
- **Task Notes:** Highly detailed and well formatted spec, generation works quite well, adds generous amount of tests with mocking.
- **Src Diffs:** +101/-0 | **Test Diffs:** +139/-0
- **Spec:** cli-add.md | **Patch Sha:** 0cb642f
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
add a cli interface for the stego-llm package and add a script which installs with the package which calls this cli.
- the script name should be "innocuous" 
- the script will have two main subcommands: "encode" and "decode"
> innocuous [optional-flags] [encode] [decode]
optional flags: 
-v, -vv
--chunk_size <CHUNK_SIZE> (int)
--initial-prompt-text <PROMPT> (str) 
--initial-prompt-file <path/to/promptfile> (str or path) this will attempt to read the content of the path to the file and pass as initial_prompt

The encode subcommand takes arguments:
> innocuous encode <flag>
--text <ASCII_TEXT> (str)
--bytes <BYTE_DATA> (str) This will be quoted text of form '\x99\xff' or hexidecimal '0f1e6f' which in converted to byte form
--btc-addr <BTC_ADDR> (str)
It will print the resulting encoded message from main_decode to stdout.
The above flags are mutually exclusive, and one is required.

The decode subcommand takes as arguments:
> innocuous decode <flag>
--message <MESSAGE> (str)
--file <path/to/file> (str or path) this will attempt to read the content of the path to the file, convert the contents to bytes and run main_decode.
This will print the decoded message from the input message of file to stdout.

Create several tests for this functionality in the tests/ directory in a separate file from existing ones.
</pre>

<h3>Patch</h3>

<pre>
commit 0cb642f301415deea295a5f7c94e68d1f1014a23
Author: sutt <wsutton17@gmail.com>
Date:   Mon Aug 25 15:12:31 2025 -0400

    feat: add innocuous command-line interface

diff --git a/pyproject.toml b/pyproject.toml
index 2315a24..12041a3 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -39,10 +39,15 @@ classifiers = [
     "Topic :: Software Development :: Libraries :: Python Modules",
 ]
 
+[project.scripts]
+innocuous = "stego_llm.cli:main"
+
 [tool.setuptools.packages.find]
 where = ["."]
 include = ["stego_llm*"]
 
 [project.optional-dependencies]
-dev = ["pytest", "black", "ruff", "ipykernel", "jupyter"]
+dev = ["pytest", "black", "ruff", "ipykernel", "jupyter", "pytest-mock"]
 
 [tool.pytest.ini_options]
 testpaths = ["tests"]
diff --git a/stego_llm/cli.py b/stego_llm/cli.py
new file mode 100644
index 0000000..7f3653f
--- /dev/null
+++ b/stego_llm/cli.py
@@ -0,0 +1,101 @@
+import argparse
+import logging
+import sys
+from pathlib import Path
+
+from stego_llm.core import main_decode, main_encode
+from stego_llm.llm import create_llm_client
+
+logger = logging.getLogger(__name__)
+
+
+def main():
+    """CLI entry point."""
+    parser = argparse.ArgumentParser(description="LLM Steganography")
+    parser.add_argument(
+        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
+    )
+    parser.add_argument(
+        "--chunk_size", type=int, default=3, help="Chunk size for encoding/decoding"
+    )
+    prompt_group = parser.add_mutually_exclusive_group()
+    prompt_group.add_argument(
+        "--initial-prompt-text", type=str, help="Initial prompt text"
+    )
+    prompt_group.add_argument(
+        "--initial-prompt-file", type=Path, help="Path to file with initial prompt"
+    )
+
+    subparsers = parser.add_subparsers(dest="command", required=True)
+
+    # Encode command
+    encode_parser = subparsers.add_parser("encode", help="Encode a message")
+    encode_group = encode_parser.add_mutually_exclusive_group(required=True)
+    encode_group.add_argument("--text", type=str, help="Text to encode")
+    encode_group.add_argument("--bytes", type=str, help="Bytes to encode (hex)")
+    encode_group.add_argument("--btc-addr", type=str, help="Bitcoin address to encode")
+
+    # Decode command
+    decode_parser = subparsers.add_parser("decode", help="Decode a message")
+    decode_group = decode_parser.add_mutually_exclusive_group(required=True)
+    decode_group.add_argument("--message", type=str, help="Message to decode")
+    decode_group.add_argument(
+        "--file", type=Path, help="Path to file with message to decode"
+    )
+
+    args = parser.parse_args()
+
+    log_level = logging.WARNING
+    if args.verbose == 1:
+        log_level = logging.INFO
+    elif args.verbose >= 2:
+        log_level = logging.DEBUG
+    logging.basicConfig(level=log_level)
+
+    initial_prompt = None
+    if args.initial_prompt_text:
+        initial_prompt = args.initial_prompt_text
+    elif args.initial_prompt_file:
+        initial_prompt = args.initial_prompt_file.read_text()
+
+    # Hardcoded for now
+    num_logprobs = 100
+    if initial_prompt is None:
+        initial_prompt = "Below is an iambic penatameter poem. Complete it:\nThe king"
+
+    if args.command == "encode":
+        message_bytes = b""
+        if args.text:
+            message_bytes = args.text.encode("utf-8")
+        elif args.bytes:
+            message_bytes = bytes.fromhex(args.bytes)
+        elif args.btc_addr:
+            message_bytes = args.btc_addr.encode("utf-8")
+
+        llm = create_llm_client()
+        encoded_message = main_encode(
+            llm=llm,
+            initial_prompt=initial_prompt,
+            msg=message_bytes,
+            chunk_size=args.chunk_size,
+            num_logprobs=num_logprobs,
+        )
+        print(encoded_message)
+
+    elif args.command == "decode":
+        encoded_text = ""
+        if args.message:
+            encoded_text = args.message
+        elif args.file:
+            encoded_text = args.file.read_text()
+
+        llm = create_llm_client()
+        decoded_bytes = main_decode(
+            llm=llm,
+            encoded_prompt=encoded_text,
+            initial_prompt=initial_prompt,
+            chunk_size=args.chunk_size,
+            num_logprobs=num_logprobs,
+        )
+        print(repr(decoded_bytes))
+
+
+if __name__ == "__main__":
+    main()
diff --git a/tests/test_cli.py b/tests/test_cli.py
new file mode 100644
index 0000000..19d3406
--- /dev/null
+++ b/tests/test_cli.py
@@ -0,0 +1,153 @@
+import logging
+from stego_llm import cli
+
+
+def test_encode_text(mocker):
+    """Test encode command with --text."""
+    mocker.patch("sys.argv", ["innocuous", "encode", "--text", "hello"])
+    mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
+    mock_create_llm = mocker.patch("stego_llm.cli.create_llm_client")
+    mocker.patch("builtins.print")
+
+    cli.main()
+
+    mock_create_llm.assert_called_once()
+    mock_main_encode.assert_called_once()
+    assert mock_main_encode.call_args.kwargs["msg"] == b"hello"
+
+
+def test_encode_bytes(mocker):
+    """Test encode command with --bytes."""
+    mocker.patch(
+        "sys.argv", ["innocuous", "encode", "--bytes", "68656c6c6f"]
+    )  # "hello" in hex
+    mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
+    mocker.patch("stego_llm.cli.create_llm_client")
+    mocker.patch("builtins.print")
+
+    cli.main()
+
+    mock_main_encode.assert_called_once()
+    assert mock_main_encode.call_args.kwargs["msg"] == b"hello"
+
+
+def test_encode_btc_addr(mocker):
+    """Test encode command with --btc-addr."""
+    addr = "bc1q..."
+    mocker.patch("sys.argv", ["innocuous", "encode", "--btc-addr", addr])
+    mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
+    mocker.patch("stego_llm.cli.create_llm_client")
+    mocker.patch("builtins.print")
+
+    cli.main()
+
+    mock_main_encode.assert_called_once()
+    assert mock_main_encode.call_args.kwargs["msg"] == addr.encode("utf-8")
+
+
+def test_decode_message(mocker):
+    """Test decode command with --message."""
+    mocker.patch(
+        "sys.argv", ["innocuous", "decode", "--message", "some encoded message"]
+    )
+    mock_main_decode = mocker.patch(
+        "stego_llm.cli.main_decode", return_value=b"decoded"
+    )
+    mocker.patch("stego_llm.cli.create_llm_client")
+    mocker.patch("builtins.print")
+
+    cli.main()
+
+    mock_main_decode.assert_called_once()
+    assert (
+        mock_main_decode.call_args.kwargs["encoded_prompt"] == "some encoded message"
+    )
+
+
+def test_decode_file(mocker, tmp_path):
+    """Test decode command with --file."""
+    p = tmp_path / "message.txt"
+    p.write_text("file encoded message")
+    mocker.patch("sys.argv", ["innocuous", "decode", "--file", str(p)])
+    mock_main_decode = mocker.patch(
+        "stego_llm.cli.main_decode", return_value=b"decoded"
+    )
+    mocker.patch("stego_llm.cli.create_llm_client")
+    mocker.patch("builtins.print")
+
+    cli.main()
+
+    mock_main_decode.assert_called_once()
+    assert (
+        mock_main_decode.call_args.kwargs["encoded_prompt"] == "file encoded message"
+    )
+
+
+def test_initial_prompt_text(mocker):
+    """Test --initial-prompt-text flag."""
+    mocker.patch(
+        "sys.argv",
+        ["innocuous", "--initial-prompt-text", "my prompt", "encode", "--text", "t"],
+    )
+    mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
+    mocker.patch("stego_llm.cli.create_llm_client")
+    mocker.patch("builtins.print")
+
+    cli.main()
+
+    mock_main_encode.assert_called_once()
+    assert mock_main_encode.call_args.kwargs["initial_prompt"] == "my prompt"
+
+
+def test_initial_prompt_file(mocker, tmp_path):
+    """Test --initial-prompt-file flag."""
+    p = tmp_path / "prompt.txt"
+    p.write_text("prompt from file")
+    mocker.patch(
+        "sys.argv",
+        ["innocuous", "--initial-prompt-file", str(p), "encode", "--text", "t"],
+    )
+    mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
+    mocker.patch("stego_llm.cli.create_llm_client")
+    mocker.patch("builtins.print")
+
+    cli.main()
+
+    mock_main_encode.assert_called_once()
+    assert mock_main_encode.call_args.kwargs["initial_prompt"] == "prompt from file"
+
+
+def test_chunk_size(mocker):
+    """Test --chunk_size flag."""
+    mocker.patch(
+        "sys.argv", ["innocuous", "--chunk_size", "4", "encode", "--text", "t"]
+    )
+    mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
+    mocker.patch("stego_llm.cli.create_llm_client")
+    mocker.patch("builtins.print")
+
+    cli.main()
+
+    mock_main_encode.assert_called_once()
+    assert mock_main_encode.call_args.kwargs["chunk_size"] == 4
+
+
+@mocker.patch(
+    "verbose_arg, expected_level",
+    [
+        ([], logging.WARNING),
+        (["-v"], logging.INFO),
+        (["-vv"], logging.DEBUG),
+        (["-vvv"], logging.DEBUG),
+    ],
+)
+def test_verbosity(mocker, verbose_arg, expected_level):
+    """Test verbosity flags."""
+    argv = ["innocuous"] + verbose_arg + ["encode", "--text", "t"]
+    mocker.patch("sys.argv", argv)
+    mocker.patch("stego_llm.cli.main_encode")
+    mocker.patch("stego_llm.cli.create_llm_client")
+    mock_basic_config = mocker.patch("logging.basicConfig")
+    mocker.patch("builtins.print")
+
+    cli.main()
+
+    mock_basic_config.assert_called_once()
+    assert mock_basic_config.call_args.kwargs["level"] == expected_level
</pre>
</details>

---

## v0.1.0

#### `prepost-filter-decode.md`
- **Spec Summary:** *Apply refactor of filter_tok logic to pre_accept_filter + post_accept_filter functions in src/main:main_decode. Allow main_decode to take into account same logic so decoded data matches input. Functions will be extended with additional details.*
- **Commit Message:** *refactor: apply pre/post accept filters to main_decode*
- **Task Notes:** simpler than anticipated. the fix on top was actually a problem with encoder logic being emulated.
- **Src Diffs:** +2/-0 | **Test Diffs:** n/a
- **Spec:** prepost-filter-decode.md | **Patch Sha:** 960c697
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
in src/main:main_decode
apply the refactor of filter_tok logic to pre_accept_filter + post_accept_filter functions.
below there is a partial diff showing how what this function and is and how it is used. 
Now allow main_decode to take into account that same logic so the decoded data will match the input passed into 
Assume pre_accept_filter + post_accept_filter  will be extended further with additional details and logic so you should not implement the individual logic outside this method but rather simply call it within decode

```diff
diff --git a/src/main.py b/src/main.py
index 74d0d45..b2bf502 100644
--- a/src/main.py
+++ b/src/main.py
@@ -16,6 +16,8 @@ from stego.basic import (
 from stego.utils import (
     filter_tok,
     accept_tok,
+    pre_accept_filter,
+    post_accept_filter,
 )
 from btc.addr_codec import (
     decode_bitcoin_address,
@@ -40,7 +42,6 @@ def main_encode(
 
     current_prompt = initial_prompt
     
-    # for enc_int in enc_ints:
     while len(enc_ints) != 0:
 
         toks = infer_llm(llm, prompt=current_prompt, num_output=num_logprobs)
@@ -49,8 +50,8 @@ def main_encode(
         logger.debug(to_json(toks))
 
         toks = filter_tok(toks)
-
-        logger.debug(f"filter non-alpha: {num_logprobs} -> {len(toks)}")
+        toks = pre_accept_filter(toks)
+        logger.debug(f"pre_accept_filter: {num_logprobs} -> {len(toks)}")
 
         accepted_tok = accept_tok(toks)
         if accepted_tok is not None:
@@ -58,18 +59,20 @@ def main_encode(
             logger.debug(f"accept_tok hit: {repr(accepted_tok)} | continuing...")
             continue
 
-        enc_int = enc_ints.pop(0)
+        _num_toks = len(toks)
+        toks = post_accept_filter(toks)
+        logger.debug(f"post_accept_filter: {_num_toks} -> {len(toks)}")
 
+        enc_int = enc_ints.pop(0)

diff --git a/src/stego/utils.py b/src/stego/utils.py
index bf29c40..17b0659 100644
--- a/src/stego/utils.py
+++ b/src/stego/utils.py
@@ -45,6 +45,23 @@ def acceptance_criteria_2(pairs: List[Tuple[str, float]], thresh=0.7) -> bool:
     if pairs[0][1] >= thresh: return True
     return False
     
+def pre_accept_filter(data: dict) -> dict:
+    """
+        before acceptance logic, allow common punctuation
+    """
+    return {
+        k:v for k,v in data.items()
+        if allowed_2(k)
+    }
+
+def post_accept_filter(data: dict) -> dict:
+    """
+        after acceptance logic, disallow all punctuation
+    """
+    return {
+        k:v for k,v in data.items()
+        if allowed_1(k)
+    }
 
```
</pre>

<h3>Patch</h3>

<pre>
commit 960c69766a98d5d280488330697f8faae3022c46
Author: sutt <wsutton17@gmail.com>
Date:   Sat Aug 23 08:31:06 2025 -0400

    refactor: apply pre/post accept filters to main_decode

diff --git a/src/main.py b/src/main.py
index b2bf502..d550e5c 100644
--- a/src/main.py
+++ b/src/main.py
@@ -94,6 +94,7 @@ def main_decode(
         toks = infer_llm(llm, prompt=current_prompt, num_output=num_logprobs)
         toks = cvt_to_logprobs(toks)
         toks = filter_tok(toks)
+        toks = pre_accept_filter(toks)
 
         accepted_tok = accept_tok(toks)
         if accepted_tok is not None:
@@ -108,6 +109,7 @@ def main_decode(
                 memo[state] = None
                 return None
 
+        toks = post_accept_filter(toks)
         possible_matches = []
         
         num_candidate_toks = 2**chunk_size
</pre>
</details>

#### `decode-accept-1.md`
- **Spec Summary:** *Apply the accept_tok logic that was added to main_encode to main_decode. Use partial diff showing function usage. Allow main_decode to take into account same logic so decoded data matches input. Accept_tok will be extended with additional details.*
- **Commit Message:** *feat: apply accept_tok logic to decoder*
- **Task Notes:** prompt uses the "previous diff pattern". fine solution, nothing too challenging.
- **Src Diffs:** +14/-0 | **Test Diffs:** n/a
- **Spec:** decode-accept-1.md | **Patch Sha:** 79a4c67
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
in src/main:main_decode
apply the accept_tok logic that was added to main_encode
below there is a partial diff showing how what this function and is and how it is used. 
Now allow main_decode to take into account that same logic so the decoded data will match the input passed into 
Assume accept_tok will be extended further with additional details and logic so you should not implement the individual logic outside this method but rather simply call it within decode


```diff
diff --git a/src/main.py b/src/main.py
index 0abf652..bd122e1 100644
--- a/src/main.py
+++ b/src/main.py
@@ -15,6 +15,7 @@ from stego.basic import (
 )
 from stego.utils import (
     filter_tok,
+    accept_tok,
 )
 from btc.addr_codec import (
     decode_bitcoin_address,
@@ -39,7 +40,8 @@ def main_encode(
 
     current_prompt = initial_prompt
     
-    for enc_int in enc_ints:
+    # for enc_int in enc_ints:
+    while len(enc_ints) != 0:
 
         toks = infer_llm(llm, prompt=current_prompt, num_output=num_logprobs)
 
@@ -49,9 +51,17 @@ def main_encode(
 
         logger.debug(f"filter non-alpha: {num_logprobs} -> {len(toks)}")
 
+        accepted_tok = accept_tok(toks)
+        if accepted_tok is not None:
+            current_prompt += accepted_tok
+            logger.debug(f"accept_tok hit: {repr(accepted_tok)} | continuing...")
+            continue
+
+        enc_int = enc_ints.pop(0)
+
         current_tok = list(toks.keys())[enc_int]
 
-        logger.debug(f"enc_int: {enc_int} | token: {current_tok}")
+        logger.debug(f"enc_int: {enc_int} | token: {repr(current_tok)}")
 
         current_prompt += current_tok
 
diff --git a/src/stego/utils.py b/src/stego/utils.py
index 40c364c..84b1e03 100644
--- a/src/stego/utils.py
+++ b/src/stego/utils.py
@@ -1,3 +1,8 @@
+from typing (
+    List,
+    Tuple,
+)
+
 
+def accept_tok(data: dict) -> str | None:
+    """return a token if acceptance is a match; otherwise None"""
+    pairs = [(k,v) for k,v in data.items()]    
+    if acceptance_criteria_1(pairs): return pairs[0][0]
+    # if acceptance_criteria_2(pairs): return 
+    return None
+
+def acceptance_criteria_1(pairs: List[Tuple[str, float]]):
+    if pairs[0][0] == "\n": return True

```
</pre>

<h3>Patch</h3>

<pre>
commit 79a4c671e69eca61ca2e5b4868e2960ff107648d
Author: sutt <wsutton17@gmail.com>
Date:   Thu Aug 21 19:37:42 2025 -0400

    feat: apply accept_tok logic to decoder

diff --git a/src/main.py b/src/main.py
index 11384f1..1a0c93b 100644
--- a/src/main.py
+++ b/src/main.py
@@ -89,8 +89,22 @@ def main_decode(
             return memo[state]
 
         toks = infer_llm(llm, prompt=current_prompt, num_output=num_logprobs)
+        toks = cvt_to_logprobs(toks)
         toks = filter_tok(toks)
 
+        accepted_tok = accept_tok(toks)
+        if accepted_tok is not None:
+            if remaining_text.startswith(accepted_tok):
+                new_prompt = current_prompt + accepted_tok
+                new_remaining = remaining_text[len(accepted_tok):]
+                
+                result = solve(new_prompt, new_remaining)
+                memo[state] = result
+                return result
+            else:
+                memo[state] = None
+                return None
+
         possible_matches = []
         
         num_candidate_toks = 2**chunk_size
</pre>
</details>

#### `decode-branch.md`
- **Spec Summary:** *Refactor decode_main function to handle situation where remaining_text may .startswith match with multiple eligible tokens. Need branching to check maxsize of first 2**chunk_size tokens after tok_filter. Apply hacky solution for now.*
- **Commit Message:** *refactor: use backtracking in decoder to resolve ambiguous token matches*
- **Task Notes:** phenomenal solution; implemented difficult concept in 1-shot. fix was only for an llm library bug the ai-coder couldn't have realized.
- **Src Diffs:** +48/-25 | **Test Diffs:** n/a
- **Spec:** decode-branch.md | **Patch Sha:** cdabc98
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
refactor decode_main function to deal with the following situation:
remaining_text may .startswith match with multiple eligible tokens on that iteration.
for example, if remaining_text = "all above" and tok.keys() is ["a","go", "all"] there are two matches. Imagine that the encoder chose "all" but the decoder, as it is now written will select "a" since it comes first in iteration. Then on the next step or subsequent steps it will encounter an error.
we likely need a way to do branching, and check 
note bene: the maxsize of tokens you need to search is the first 2**chunk_size tokens after the tok_filter step.
note bene: we can apply a hacky solution for now where we don't fully solve it perfectly but try to back-up slighlty and go the other direction. One way to do this could be to go back one or two words (separated by a space) and try again
</pre>

<h3>Patch</h3>

<pre>
commit cdabc988254012812d1a8d01f84f1b53e1a401e2
Author: sutt <wsutton17@gmail.com>
Date:   Thu Aug 21 19:37:29 2025 -0400

    refactor: use backtracking in decoder to resolve ambiguous token matches

diff --git a/src/main.py b/src/main.py
index 1a0c93b..11384f1 100644
--- a/src/main.py
+++ b/src/main.py
@@ -68,38 +68,61 @@ def main_decode(
     llm,
     encoded_prompt,
     initial_prompt,
-    chunk_size
+    chunk_size,
+    num_logprobs,
 ):
 
     message_carrying_text = encoded_prompt[len(initial_prompt):]
+    memo = {}
 
-    decoded_ints = []
-    current_prompt = initial_prompt
-    remaining_text = message_carrying_text
+    def solve(current_prompt, remaining_text):
+        state = (current_prompt, remaining_text)
+        if not remaining_text:
+            return []
+        
+        if state in memo:
+            return memo[state]
 
-    while remaining_text:
         toks = infer_llm(llm, prompt=current_prompt, num_output=num_logprobs)
-        toks = filter_tok(toks)
+        toks = cvt_to_logprobs(toks)
+        toks = filter_tok(toks)
 
-        found_match = False
-        for i, token in enumerate(toks.keys()):
-            if remaining_text.startswith(token):
-                decoded_ints.append(i)
-                current_prompt += token
-                remaining_text = remaining_text[len(token):]
-                found_match = True
-                break
-        
-        if not found_match:
-            raise Exception("Decoding failed: No matching token found.")
+        possible_matches = []
+        
+        num_candidate_toks = 2**chunk_size
+        if len(toks) < num_candidate_toks:
+            logger.warning(f"num toks after filter is {len(toks)}, chunk_size implies {num_candidate_toks}")
+            num_candidate_toks = len(toks)
 
-    decoded_bytes = ints_to_bytes(decoded_ints, chunk_size=chunk_size)
+        for i, token in enumerate(list(toks.keys())[:num_candidate_toks]):
+            if remaining_text.startswith(token):
+                possible_matches.append((i, token))
+
+        if not possible_matches:
+            memo[state] = None
+            return None
+
+        # sort by longest match
+        possible_matches.sort(key=lambda x: len(x[1]), reverse=True)
+
+        for i, token in possible_matches:
+            new_prompt = current_prompt + token
+            new_remaining = remaining_text[len(token):]
+            
+            result = solve(new_prompt, new_remaining)
+            
+            if result is not None:
+                memo[state] = [i] + result
+                return [i] + result
+
+        memo[state] = None
+        return None
+
+    decoded_ints = solve(initial_prompt, message_carrying_text)
+    if decoded_ints is None:
+        raise Exception("Decoding failed.")
+    
+    decoded_bytes = ints_to_bytes(decoded_ints, chunk_size=chunk_size)    
     return decoded_bytes
 
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-..
\ No newline at end of file
</pre>
</details>

#### `decode1.md`
- **Spec Summary:** *In src/main.py implement main_decode*
- **Commit Message:** *feat: add main_decode and full encode/decode cycle*
- **Task Notes:** prompts is very terse, and ai-generation understands intent prefectly, get a little liberal with modifying other existing methods but in a helpful way.
- **Src Diffs:** +43/-4 | **Test Diffs:** n/a
- **Spec:** decode1.md | **Patch Sha:** d4dd55e
<details>
<summary>full details</summary> 
<h3>Spec</h3>

<pre>
in src/main.py implement main_decode
</pre>

<h3>Patch</h3>

<pre>
commit d4dd55e88717231e76a01605e7a57b184a1e318e
Author: sutt <wsutton17@gmail.com>
Date:   Thu Aug 21 19:37:17 2025 -0400

    feat: add main_decode and full encode/decode cycle

diff --git a/src/main.py b/src/main.py
index 431e03c..0abf652 100644
--- a/src/main.py
+++ b/src/main.py
@@ -29,13 +29,14 @@
 
 
 def main_encode(
+    llm,
     initial_prompt,
     msg,
     chunk_size,
     num_logprobs,
 ):
 
-    llm = get_llm()
+    # llm = get_llm()
 
     enc_ints = message_to_chunks(msg, chunk_size=chunk_size)
 
@@ -58,11 +59,50 @@ def main_encode(
 
         current_prompt += current_tok
 
-    return current_prompt
+    return current_prompt, initial_prompt, chunk_size
+
+
+def main_decode(
+    llm,
+    encoded_prompt,
+    initial_prompt,
+    chunk_size
+):
+
+    message_carrying_text = encoded_prompt[len(initial_prompt):]
+
+    decoded_ints = []
+    current_prompt = initial_prompt
+    remaining_text = message_carrying_text
+
+    while remaining_text:
+        toks = infer_llm(llm, prompt=current_prompt, num_output=100)
+        toks = filter_tok(toks)
+
+        found_match = False
+        for i, token in enumerate(toks.keys()):
+            if remaining_text.startswith(token):
+                decoded_ints.append(i)
+                current_prompt += token
+                remaining_text = remaining_text[len(token):]
+                found_match = True
+                break
+        
+        if not found_match:
+            raise Exception("Decoding failed: No matching token found.")
+
+    decoded_bytes = ints_to_bytes(decoded_ints, chunk_size=chunk_size)
+    return decoded_bytes
 
 
 if __name__ == "__main__":
 
-    main_encode(
-        initial_prompt="the king", msg=b"this is a test", chunk_size=2, num_logprobs=100
-    )
+    llm = get_llm()
+    encoded_prompt, initial_prompt, chunk_size = main_encode(
+        llm=llm, initial_prompt="the king", msg=b"this is a test", chunk_size=2, num_logprobs=100
+    )
+    decoded_bytes = main_decode(
+        llm=llm, encoded_prompt=encoded_prompt, initial_prompt=initial_prompt, chunk_size=chunk_size
+    )
+    print(decoded_bytes)
</pre>
</details>

---
