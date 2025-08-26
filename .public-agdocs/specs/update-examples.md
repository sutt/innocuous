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
