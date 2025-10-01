import os, sys, hashlib, json, numpy as np
from pathlib import Path
from llama_cpp import Llama

# run as: uv run examples/align.py
# or: INNOCUOUS_LLM_PATH=/path/to/model.gguf uv run examples/align.py

# control inference flags
# for k in ["OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","VECLIB_MAXIMUM_THREADS","GOTO_NUM_THREADS"]:
#     os.environ.setdefault(k, "1")

# model path setup
model = os.getenv("INNOCUOUS_LLM_PATH") or (sys.argv[1] if len(sys.argv) > 1 else None)
if not model:
    sys.exit("Set INNOCUOUS_LLM_PATH or pass the model path as the first CLI arg.")
model = str(Path(model).expanduser())
if not os.path.exists(model):
    sys.exit(f"Model file not found: {model}")

prompt = sys.argv[2] if len(sys.argv) > 2 else "Tell me a fun fact about otters."

llm = Llama(
    model_path=model,
    # n_threads=1,
    # n_batch=32,
    logits_all=True,
    # seed=0,
    # add_bos_token=True,   # affects __call__, not eval()
    # use_mmap=True,
    # verbose=False,        # optional: quiet the “chat format” banner
)

# IMPORTANT: eval() needs token IDs, not a string
# Since add_bos_token only applies to __call__, we add BOS here explicitly:
tokens = llm.tokenize(prompt.encode("utf-8"), add_bos=True)

# Evaluate the prompt tokens so the *next* token logits are ready
llm.eval(tokens)

# Grab logits for the next-token distribution
logits = np.array(llm.eval_logits, dtype=np.float32)
print("len(logits):", logits.size)
hash_full_logits = hashlib.sha256(logits.tobytes()).hexdigest()


# Use the last step's logits (next-token distribution)
step_logits = logits[-1] if logits.ndim == 2 else logits
print("vocab size:", step_logits.size)

# Top-5 indices sorted by score descending
k = 5
top_idx = np.argpartition(step_logits, -k)[-k:]
top_idx = top_idx[np.argsort(step_logits[top_idx])[::-1]]

def id_to_piece(tid: int) -> str:
    try:
        # Newer builds may have an id->token table:
        return llm.tokenizer().id_to_token[int(tid)]
    except Exception:
        # Always works:
        return llm.detokenize([int(tid)]).decode("utf-8", errors="replace")

top_logit_data = [(id_to_piece(int(i)), float(step_logits[int(i)])) for i in top_idx]

hash_top_logits = hashlib.sha256(step_logits.tobytes()).hexdigest()

# Printout displays
print("top5 logits:")
print(json.dumps(top_logit_data, indent=2))

print("sha256 topp_logits:", hash_top_logits)

print("sha256 full_logits:", hash_full_logits)