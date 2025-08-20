# Demo for Innocuous

How to encode / decode byte data for steganography in LLM's.

### Current State
_August 20, 2025_

#### Move to app in src

Running `python src/app.py`:
```
{
  " Paris": 0.24246281385421753,
  " a": 0.15221050381660461,
  " one": 0.10001478344202042,
  " known": 0.09030069410800934,
  " an": 0.04709842428565025,
  " the": 0.039719972759485245,
  " famous": 0.031470026820898056,
  " home": 0.028114313259720802,
  " also": 0.0232237558811903,
  " not": 0.019625568762421608
}
```


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


