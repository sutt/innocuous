# Demo for Innocuous

How to encode / decode byte data for steganography in LLM's.

### Current State
_August 19, 2025_

#### `simple.py`

Run `python simple.py` or `pytest simple.py` for a naive encoding algo.
- See **simple.py** docstrings to understand more.
- Each token carries 3 bits of info with `chunk_size=3`. 

This means it is roughly one limerick long to encode a bitcoin address:
- Bitcoin address: 160 bits
- 160 bits / 3 bits = 54 tokens
- Limerick: 30-45 words

#### `working/`

- `one.py`: get logprobs from llama
- `book2.py`: outline the stderr suppress
- `two.py` & `three.py`: copy & pasted solutions from gpt-5 to do encoding based off simulated logprobs values; they didn't work


