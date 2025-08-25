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