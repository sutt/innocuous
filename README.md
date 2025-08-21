# Demo for Innocuous

How to encode / decode byte data for steganography in LLM's.

> ⚠️ **Very much a research repo; not for production use.**

### Initial Results

Let's encode this P2PKH address: **`12Wfw4L3oPJFk2q6osDoZLYAwdFkhvgt4E`**. This is a real address shown [here on mempool](https://mempool.space/address/12Wfw4L3oPJFk2q6osDoZLYAwdFkhvgt4E). This address type encodes 20 bytes.

We're using **Mistral-7b-instruct-Q4** as the underlying LLM.

Running `python src/main.py` with `example_addr()` as the main function. 

##### With `chunk_size=2` it produces the output:

> The king, a man of noble grace, did dwell in state within a towr that loomed above all other loft, where eagles, soaring free in azured heights would cast, in envied sight, a winking glace at him who ruled, and in his hand a golden rod of rule he held alight, with sceptered power to rule and right, and with

##### With `chunk_size=3` it produces the output:

> The king, whose power and pride, were known through the realms of earth to shine, In harness proud as eagle with the morning wind entwin. Now with what grace he did command his people in this wise. Their daily toiling lives for them to thine

We can see in the script we're able to succesfully encode and decode the underlying data of: `b'\x10\x94\xaf\xff\x83\xbf\x02M\xe8\xca\xdc_s\x15\x15o,\x82^\x93'`

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


