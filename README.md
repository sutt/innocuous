# Innocuous 🔎 

**Encode messages into LLM outputs with the power of steganography.**

A pip installable library for **encode** and **decode** functions with a command line script. Compatible with all [**Llama.cpp LLM's**](https://huggingface.co/models?pipeline_tag=text-generation&apps=llama.cpp).

[![PyPI version](https://img.shields.io/pypi/v/innocuous)](https://pypi.org/project/innocuous/)

**Install:** `pip install innocuous` and see [Quickstart](#quickstart) section for more info.

---

**Example of Innocuous in action:** Consider the following passage. We'll pass the text (along with the original prompt) into decoder in the innocuous library to reveal a message within it.

> _Amidst the ancient forest, dwelt a wondrous Wizard renowned for his arcane might. One day, he unearthed true power not in enchantments, but in wellaimed words. Fearing misuse, he penned this power three ways in his magnum opus obscuring it with tedious trifles._
>
>_Time passed, the wizard departed, while countless seekers puzzled over his laborious tome. Until one sage, whose curiosity was matched only by fortitude, finally discovered the cryptic keys tucked deep within these words un_

```python
from stego_llm import main_decode
# copy the above text into cryptic text
cryptic_text = "\nAmidst the ancient forest, dwelt a wondrous Wizard renowned for his arcane might. One day, he unearthed true power not in enchantments, but in wellaimed words. Fearing misuse, he penned this power three ways in his magnum opus obscuring it with tedious trifles.\n\nTime passed, the wizard departed, while countless seekers puzzled over his laborious tome. Until one sage, whose curiosity was matched only by fortitude, finally discovered the cryptic keys tucked deep within these words un"
initial_prompt = "Write a short fable in about 80 words. The story should describe a wise wizard who discovered that true power lies in words of persuasion. Fearing his knowledge would be misused, he condensed this power into three secret words. To protect them, he buried the phrase inside a long, ordinary document so that only future seekers with patience and insight could uncover it. The tale should feel timeless, mysterious, and open-ended, leaving the reader with a sense of hidden wisdom.\n"

recovered_data = main_decode(
    encoded_prompt=(initial_prompt + cryptic_text),
    initial_prompt=initial_prompt,
    chunk_size=3,
    num_logprobs=100,
)
print(recovered_data)
# prints: b'pip install innocuous'
```

**So the hidden message within story of the wizard is "`pip install innocuous`"!** How can this be? Read on to find out, or install the package and start using it yourself...

TODO: Maybe add one more example inside a detail tag where message is "the message could be anything".

---

### Other Examples

Let's encode this _Bitcoin P2PKH address_: **`12Wfw4L3oPJFk2q6osDoZLYAwdFkhvgt4E`** which encodes 20 bytes. 

We're using **Mistral-7b-instruct-Q4** as the underlying LLM.

We'll run the cli script:

```bash
innocuous \
    --initial-prompt-text 'Below is an iambic penatameter poem. Complete it:\nThe king' \
    --check_size 3 \
    encode --btc-addr '12Wfw4L3oPJFk2q6osDoZLYAwdFkhvgt4E' \
```

##### chunk_size: 4
> The king with regal demeanor strode,  
> To face in fierce encounter this foe,  
> Where lies the heart and might and bold,  
> He challenged ere the first star threw low,  
>  
> His foe a savage warrior wailed,  
> And brandished arms that held no shield,  
> But  

##### chunk_size: 3
> The king sat in his golden chair,  
> A scepter in his hand,  
> A queen stood next by his side,  
> Her beauty shone far and wide,  
> And all around their castle stoodThe noblemen whose lives did hinge  
> Awaiting his decrees of war Or peace that day with hope did sing  
> What word shall end this royal verse  
> And grant my pen its rightful due  


**Of course an llm can create any type of content, not just poems about kings; this is just an example of one type generated text.**

For more check the [Showcase](./docs/showcase) section in the docs and the [Example Scripts](./examples).

---

### Use Cases

**Mnemonics:** Alphanumeric codes with aribtrary numbers and letters are difficult to remember. But stories, poems, and songs stay in our memory for years. With Innocuous you can convert data made for machine-to-machine communication into data made for human memory.

**Hidden Messages:** Let's face it, the internet is coming under increasing supervision, centralization, and censorship. You can fight back with Innocuous: communicate URL's and other information that freedom fighters need within seemingly innocuous forum and social media posts.

**UX Enhancements:** If you are a designer, you know that long serial numbers or cyphertexts can intimidate and offend the sensibilities of users. Innocuous can help you make playful text-based encodings that represent the same underlying data.

In a way it's like **Reverse-TinyURL**: _instead of being centralized database, it's decentralized protocol. And instead of making the content shorter and machine-like, it makes it longer and more human-like._

**Examples of things that might be good for encoding:**
- PGP Keys
- URL's in firewalled and censorship regimes
- Cryptocurrency addresses
- Nostr Pubkeys
- _Something else? Check out [contributing](#contributing) section to leave other suggestions._


> ⚠️ **Still a research project; not ready for production use.**

> ☠️ **Not recommended for private key storage.**

### Quickstart

_**Option A: PyPI & Command Line**_

**1. Install the package from [PyPI](https://pypi.org/project/innocuous/) with pip or uv:** 

```bash
pip install innocuous
```

Check that it's installed, run the cli script:

```bash
$ innocuous
# usage: innocuous [-h] [-v] [--llm-path LLM_PATH] ...
#                 {encode,decode,check-llm} ...
```
**2. Download a model weight file**

Download any model weight compatible with [llama-cpp-python](https://github.com/abetlen/llama-cpp-python). A great place to find these freely availble is [HuggingFace](https://huggingface.co/models?pipeline_tag=text-generation&num_parameters=min:0,max:12B&library=gguf&apps=llama.cpp&sort=trending). See the docs on installing models for more info.

A small, quantized, model with less than 10B params should perform well. In most examples, we use [Mistral-7B-instruct-Q4](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF?show_file_info=mistral-7b-instruct-v0.2.Q4_K_M.gguf) (4.1 GB).

**3. Configure path to model weight file**

Tell innocuous where you saved the weights file with either an environmental variables, with a command line arguemnt, of if using it's library functions, passing the path as an argument.

Then run check-llm command to test it's working:

```bash
# if you added the env var
innocuous check-llm

# or if you didn't add env var, pass the llm-path directly in an arg
innocuous --llm-path /path/to/model.gguf check-llm
```

If it works you'll get this output:

```
Checking for INNOCUOUS_LLM_PATH environment variable...
LLM path set to: /home/user/dev/innocuous/data/mistral-7b-instruct-v0.2.Q4_K_M.gguf
LLM file found at: /home/user/dev/innocuous/data/mistral-7b-instruct-v0.2.Q4_K_M.gguf
Attempting to load LLM...
LLM loaded successfully.
Performing simple inference task...
Inference task successful.
```

**4. Run command line script  _(Option A)_**

Run the following command:

```bash
innocuous \
    --initial-prompt-text 'Below is an iambic penatameter poem. Complete it:\nThe king' \
    --check_size 3 \
    encode --text 'hello world' \
```

Run `innocuous -h` of innocuous

**4. Import `encode` & `decode` methods into your own script. _(Option B)_** 

For example:

```python
from stego_llm import main_encode

message_to_encode = "hello world"
initial_prompt = "Write a poem about a puppy:\n"

generated_text = main_encode(
    initial_prompt=initial_prompt,
    encoded_prompt=message_to_encode.encode("utf-8"),
    chunk_size=3, num_logprobs=100,
    llm_path="path/to/model.gguf",  # only nec if `INNOCUOUS_LLM_PATH` not set
)
print(generated_text)
```

> 💡 Import methods in the **innocuous package** as **`from stego_llm import ...`.**

---

**_Repo Install & Example Scripts (second option for Quickstart)_**

**1. Clone the repo and install with pip or uv locally.**
```bash
git clone https://github.com/sutt/innocuous
cd innocuous
pip install .
```

**2. Install model weights as described above and add to env var:**

Create and **.env** file and source it:
```bash
cp .env.example .env
```
Edit the **.env** to point to your weights file absolute path (it doesn't have to be this exact model file):

```bash
export INNOCUOUS_LLM_PATH=/path/to/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```
And source it to add the `INNOCUOUS_LLM_PATH`
```bash
source .env
```

**3. Run the a script or open a notebook in the [examples/](./examples/) directory:**

For example run this script:

```bash
python examples/random_data.py
```
Which will run with full debugging log, which will produce:

```
encoded_msg: b'\x90D\xf3,\xac=\xd0<\xefFh\xe5\xa7\x124\xe0ra\x02\x00'
encode_bits: 1001000001000100111100110010110010101100001111011101000000111100111011110100011001101000111001011010011100010010001101001110000001110010011000010000001000000000
tokens: {
  ",": 0.33548852801322937,
  " sat": 0.14481237530708313,
  " with": 0.09293358027935028,
...
}
pre_accept_filter: 40 -> 35
post_accept_filter: 35 -> 32
enc_int: 0 | token: ' with'
...
decoded_ints: [2, 1, 0, 0, 1, 0, 1, 0, 3, 3, 0, 3, 0, 2, 3, 0, 2, 2, 3, 0, 0, 3, 3, 1, 3, 1, 0, 0, 0, 3, 3, 0, 3, 2, 3, 3, 1, 0, 1, 2, 1, 2, 2, 0, 3, 2, 1, 1, 2, 2, 1, 3, 0, 1, 0, 2, 0, 3, 1, 0, 3, 2, 0, 0, 1, 3, 0, 2, 1, 2, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0]
decode_bits: 1001000001000100111100110010110010101100001111011101000000111100111011110100011001101000111001011010011100010010001101001110000001110010011000010000001000000000
decoded_msg: b'\x90D\xf3,\xac=\xd0<\xefFh\xe5\xa7\x124\xe0ra\x02\x00'
decoded_msg: b'\x90D\xf3,\xac=\xd0<\xefFh\xe5\xa7\x124\xe0ra\x02\x00'

done. it worked!
```

Or checkout the jupyter notebook with example of both encode and decode [here](./examples/simple-example.ipynb).

---

### How it works

LLM's work by predicting the next token. At each step, they assigin a probability to every token in their vocabularly and then select one. But they don't always chose the top token; instead they **randomly sample** from the top tokens based on the probabilities they calculated. 

But what if instead of chosing randomly, you **directed the choice** from the top-N tokens possibilities calculated by the LLM? This concept is known as _steering_ and can be used for a variety of applications. In our case we'll use the **index number** of the probability-ranked tokens to denote an encoded integer.

This encoded integer can be represented in **binary form**, and by concatentating several steps and **concatenating the bits** of the integer at each step, we can construct bytes of data. And bytes of data can represent any form of data. Let's illustrate with an example of one step:

(Maybe this is a mardown table of a code block)

The larger the **N** in the top-N tokens you consider at each step: the **more information encoded** for each word in the output. But likewise, larger N also means you'll often direct the selection of a token the model deems *unlikely*, leading to **less coherent output**. This puts an upper-limit on how much information can be encoded per token while keeping the output text generation seeming natural.

For more information, see the Algorithm Description below and see the docs on encoding algorithms.

### Contributing

Innocuous is very much open-source as all good communication must be: the sender and reciever of information must agree on every detail of how the communication was encoded and decoded. We welcome contributions.

**A list of things that need to be worked on:**
- Use cases & catchy examples.
- Encoding/Decoding strategies:
    - At the level of encoding into top-tokens / log-probs
    - At the level of filtering / steering the tokens
    - And at the level of encoding the desired
- Test coverage & edge cases.
- Support for foreign languages.
- Support for other crypto-currencies addresses.

_Innocuous is built with the help of AI-agent framework [Agro](https://github.com/sutt/agro). Check out the [Dev Summary](./docs/dev-summary.md) to see how the prompts and ai-generation spped up development. And check out the [case-study](https://github.com/sutt/agro/blob/master/docs/case-studies/aba-innocuous-1.md) for a more detailed breakdown of techniques used._ 

