# Dev Summary
Looks at tasks and associated commit solutions generated each release.

All ai-assistance generated with [Agro](https://github.com/sutt/agro).

## v0.1.0

This was a proof of concept stage. Lots of experimentation and scratch work.

Note: there is no comprehensive tests/ directory so `Tests Diff` will be n/a here.

| Task File | Contents (truncated) | Accepted SHA | Non-test Diffs | Test Diffs | Notes |
|------|-------------|---------|-------------|------------|-----------|
| [prepost-filter-decode.md](.public-agdocs/specs/prepost-filter-decode.md) | Apply refactor of filter_tok logic to pre_accept_filter + post_accept_filter functions in src/main:main_decode. Allow main_decode to take into account same logic so decoded data matches input. Functions will be extended with additional details. | [960c697](https://github.com/sutt/innocuous/commit/960c697) | | n/a | simpler than anticipated. the fix on top was actually a problem with encoder logic being emulated. |
| [decode-accept-1.md](.public-agdocs/specs/decode-accept-1.md) | Apply the accept_tok logic that was added to main_encode to main_decode. Use partial diff showing function usage. Allow main_decode to take into account same logic so decoded data matches input. Accept_tok will be extended with additional details. | [79a4c67](https://github.com/sutt/innocuous/commit/79a4c67) | | n/a | prompt uses the "previous diff pattern". fine solution, nothing too challenging. |
| [decode-branch.md](.public-agdocs/specs/decode-branch.md) | Refactor decode_main function to handle situation where remaining_text may .startswith match with multiple eligible tokens. Need branching to check maxsize of first 2**chunk_size tokens after tok_filter. Apply hacky solution for now. | [cdabc98](https://github.com/sutt/innocuous/commit/cdabc98) | | n/a | phenomenal solution; implemented difficult concept in 1-shot. fix was only for an llm library bug the ai-coder couldn't have realized. |
| [decode1.md](.public-agdocs/specs/decode1.md) | In src/main.py implement main_decode | [d4dd55e](https://github.com/sutt/innocuous/commit/d4dd55e) | | n/a | prompts is very terse, and ai-generation understands intent prefectly, get a little liberal with modifying other existing methods but in a helpful way. |

```
38062ca docs: add dev-summary template
6d8eafd specs: v0.1.0
39478a7 docs: adding v3 examples and script to cvt to md format
00783db fix: manual fix + cleanup test example
960c697 refactor: apply pre/post accept filters to main_decode
3c5bc77 feat: filtering split to pre and post accept logic block
d89307a docs: add examples from new encode scheme, and small cleanup to code
79a4c67 feat: apply accept_tok logic to decoder
eb303f9 feat: adding prob value threshold for accept criteria
4b9a9d0 feat: apply accept_tok + examples to prove it works
46e1d16 refactor: minor cleanups
bc58fab docs: adding agro specs
197f267 docs: add initial results to readme
6257592 docs: add logs of initial results
ecc056b fix: manual fixes to make memo solution to decode work
cdabc98 refactor: use backtracking to resolve ambiguous token matches
02ad3e4 tmp: muster trees
61bde35 tmp: for tree muster
8d12aa1 test: adding a test for ai-gens
c178a5b feat: adding vocab_mistral.txt
c6ccbaa feat: added btc addr module
be31dde refactor: main now does encode decode with same args
d4dd55e feat: implement main_decode and run full encode/decode cycle
9d5dc59 main_encode is working
6ab0b6e app outine in src setup
4d536ac workspace basecamp
a0ff35d docs for simple.py
7cf9ede simple.py is working!
a037dcc almost there with simple.py, about to refactor
715acb8 simple.py: works for some encode/decode combos
270e963 refactor: Convert decimal and random operations to numpy
980663f two.py for gpt demo
aeb69f8 basecamp for encode/decode
1787b0a feat: apply softmax to selections
d654030 prepping for simple script
dbc5295 proj init + hello llama
```