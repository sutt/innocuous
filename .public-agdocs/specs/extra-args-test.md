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
 
