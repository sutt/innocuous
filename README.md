# Demo for Innocuous

How to encode / decode byte data for steganography in LLM's.

### Current State
_August 19, 2025_

Run `python simple.py` or `pytest simple.py` for a naive encoding algo.
- See **simple.py** docstrings to understand more.
- Each token carries 3 bits of info with `chunk_size=3`. 

This means it is roughly one limerick long to encode a bitcoin address:
- Bitcoin address: 160 bits
- 160 bits / 3 bits = 54 tokens
- Limerick: 30-45 words
