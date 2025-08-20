from llama_cpp import Llama
import numpy as np
import json

# Load a model (make sure you have a compatible GGUF model locally)
llm = Llama(model_path="../data/mistral-7b-instruct-v0.2.Q4_K_M.gguf", logits_all=True)

# Run inference with logits enabled
output = llm(
    "The capital of France is", 
    max_tokens=1, 
    logprobs=10,          # request top-k logprobs for tokens
)


# The raw output structure
print(output.keys())  # includes 'choices', 'tokens', 'logits'

print(output['choices'][0]['logprobs'].keys())

top_logprobs = output['choices'][0]['logprobs']['top_logprobs'][0]

x = {k: float(v) for k,v in top_logprobs.items()}

print(json.dumps(x, indent=2))

# llm.logits_to_logprobs()
# llm.sample()
# llm.eval()
# llm.tokenize()

# Example: inspect logits of the last step
# logits = output["logits"][-1]  # logits for the final step
# tokens = output["tokens"][-1]  # the predicted token ID

# print("Predicted token id:", tokens)
# print("Logits shape:", len(logits))

# # To get probabilities:
# probs = np.exp(logits - np.max(logits))  # softmax trick for stability
# probs = probs / probs.sum()

# # Show top 5 candidate tokens
# top_indices = probs.argsort()[-5:][::-1]
# for idx in top_indices:
#     tok_str = llm.tokenizer.decode([idx])
#     print(f"Token {idx:5d} ({tok_str!r}): {probs[idx]:.4f}")
