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
+from typing import (
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