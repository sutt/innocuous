# Dev Summary
Looks at tasks and associated commit solutions generated each release.

All ai-assistance generated with [Agro](https://github.com/sutt/agro).

## v0.2.3

Minor update for handling consistency, small functionality, documentation, and adding integration tests.
- Integration tests take 30+ seconds per test, so they are marked with `slow` marker, run with `pytest -m slow`.
- Integration tests get a fixture to run garbage collection manually to cleanup memory between tests.

One main logic update: decode can now fill-in missing punctuation marks, which is helpful for the mnemonics use-case.

**Interesting design pattern:** manually implemented a new test in [f57aea1](https://github.com/sutt/innocuous/commit/f57aea1) as an XFAIL, then (manually) coded the fix in [5b23579](https://github.com/sutt/innocuous/commit/5b23579) which made the xfail-test pass.

| Task File | Contents (truncated) | Accepted SHA | Diffs | Test Diffs | Notes |
|------|-------------|---------|-------------|------------|-----------|
| [extra-args-test.md](../.public-agdocs/specs/extra-args-test.md) | Add 1-2 tests for llm_extra_args feature. Test that args pass through encode/decode to constructors without real inference. Example usage: llm_extra_args={"n_ctx": 1024}. Mock instantiation/loading. | [9abdb61](https://github.com/sutt/innocuous/commit/9abdb61) | +0/-0 | +29/-0 | Simple task, not best execution.  |
| [cli-numlogprobs.md](../.public-agdocs/specs/cli-numlogprobs.md) | Create optional CLI argument --num-logprobs with default value of 100. | [fe8dbf6](https://github.com/sutt/innocuous/commit/fe8dbf6) | +8/-4 | +0/-0 | Simple. |
| [integration-test.md](../.public-agdocs/specs/integration-test.md) | Add integration test: msg0 -> encode -> decode -> msg1, assert msg0==msg1. Use pytest marker for slow tests. Mock env variable or config for model_path. | [6203b4a](https://github.com/sutt/innocuous/commit/6203b4a) | +0/-0 | +44/-0 | Tricky tests implemented with best practices. |
| [type-main-funcs.md](../.public-agdocs/specs/type-main-funcs.md) | Add type hints for args and return types to decoder.main_decoder and encoder.main_encode in stego_llm.core. Include expanded docstrings. | [b00dd60](https://github.com/sutt/innocuous/commit/b00dd60) | +48/-14 | +0/-0 | Simple but the verbose docstrings are useful to handle with ai. |
| [version-cmd.md](../.public-agdocs/specs/version-cmd.md) | Enable CLI and Python import to display package version from pyproject.toml. | [80791f9](https://github.com/sutt/innocuous/commit/80791f9) | +10/-2 | +0/-0 | Easy, but esoteric. |

```
04d2537 build: v0.2.3
222a1ca specs: v0.2.3
f01571c docs: update dev-summary for 0.2.1 and 0.2.2
b7c73e9 refactor: ruff format
9abdb61 test: add tests for llm_extra_args passthrough
2f85f37 feat: adding llm_extra_args for use in library functions
deac5b5 refactor: llama logging override now wrapped as function
77a030d refactor: cli arguments --chunk-size
cbc0de0 refactor: logging enables info level, repr of output for -v mode.
fe8dbf6 feat: add --num-logprobs argument to CLI
313efe3 fix: cli defaults to chunk_size=2 (aligns with library method defaults)
5b23579 feat: decoder fills in missing auto_accept tokens + debugging trace for decoder
711aea0 test: add sleep + gc fixture to integration test setup
f57aea1 test: refactor previous test, add decoder-only integration test
6203b4a test: add integration test for full encode/decode cycle
ddcd740 fix: add default arg vals
b00dd60 refactor: add type hints and improve docstrings for core functions
80791f9 feat: add --version flag and dynamic version loading
1505e99 build: bump version v0.2.2
```

## v0.2.2

Package build problem, fixed ([e10906f](https://github.com/sutt/innocuous/commit/e10906f)) and released.

```
1505e99 (tag: v0.2.2, origin/master, master) build: bump version v0.2.2
e10906f build: fix hatch build includes
ddc0320 (tag: v0.2.1) build: bump version v0.2.1
```

## v0.2.1

Misc updates to docs and repo structure, prepare for pypi release.

| Task File | Contents (truncated) | Accepted SHA | Src Diffs | Test Diffs | Notes |
|------|-------------|---------|-------------|------------|-----------|
| [devsummary-task-b.md](../.public-agdocs/specs/devsummary-task-b.md) | Update table in docs/dev-summary.md for v0.1.0 with git diff values for code changes columns. Each value represented as "+A/-D" format for additions/deletions from git diff --stat. | [97da5a8](https://github.com/sutt/innocuous/commit/97da5a8) | +0/-0 | +0/-0 |  |
| [devsummary-task-a.md](../.public-agdocs/specs/devsummary-task-a.md) | Add updated taskfiles to markdown table in docs/dev-summary.md for v0.1.0 with filename, summary, and GitHub SHA links. Sort by date descending and include only specs/* files. | [46468bd](https://github.com/sutt/innocuous/commit/46468bd) | +0/-0 | +0/-0 | |

```
ddc0320 (tag: v0.2.1) build: bump version v0.2.1
a7ec924 docs: major update for readme
31502d9 docs: manual fixes and commit notes for dev-summary
97da5a8 feat: impl devsummary-task-b with claude (agro auto-commit)
5e49bd9 docs: manual updates to dev-summary
46468bd feat: impl devsummary-task-a with claude (agro auto-commit)
1b6b0e8 build: add MIT license
6af0e2d build: update pkg name and build system
0b1d927 pkg: rm scripts folder to reduce clutter
086d3af docs: adding jupyter example
be74868 (tag: v0.2.0) build: v0.2.0
```

## v0.2.0

This was a complete refactor of the package structure for best practices and to make it distributable.
- The major refactor was handled with interative claude code session, so no specs on that.
- All example script separated from core package and moved to examples/ directory.
- Ruff format introduced as the linter and formatter in this version.

After the refactor, several additional features were:
- Add a CLI script to run the functionality.
- Moved model_path hard-coding to variable in env var, cli arg, or function arg.
- Updated the pyproject configs for building package.
- Introduced dedicated tests directory.

To view the complete transcript of the interactive refactor claude code session see this [gist](https://gist.github.com/sutt/66eeb6a3b4d293262ae45f74f0dc632d).

Note: some commits are updating neither `stego_llm/` ("src diffs") nor `tests/` ("test diffs") but instead updating `docs/` or `examples/` so they are showing +0/-0 diffs.


| Task File | Contents (truncated) | Accepted SHA | Src Diffs | Test Diffs | Notes |
|------|-------------|---------|-------------|------------|-----------|
| [update-examples.md](../.public-agdocs/specs/update-examples.md) | Updates scripts in examples/ directory to reflect change about model_path needing to be passed in explicitly. Includes diffs for __init__.py, cli.py, core modules, and llm interface changes. | [e7b8d5b](https://github.com/sutt/innocuous/commit/e7b8d5b) | +0/-0 | +0/-0 | Time-saving use-case of handling downstream breaking changes from a refactor. |
| [fix-tests.md](../.public-agdocs/specs/fix-tests.md) | Update tests to pass after changes to create_llm_client import and function signature. Tests were failing because create_llm_client was moved from cli.py and the function interface changed to accept llm_path parameter. | [c7cdd56](https://github.com/sutt/innocuous/commit/c7cdd56) | +0/-0 | +0/-10 | Spec uses the dump stdout + git diff data, and generation solves it. |
| [check-llm.md](../.public-agdocs/specs/check-llm.md) | Add subcommand "check-llm" and exportable function "check_llm" to verify LLM path from CLI/env var, check file existence, and execute simple inference task. Print terse confirmation of each step. | [0355954](https://github.com/sutt/innocuous/commit/0355954) | +51/-9 | +38/-0 | Generation followed multiple separate instructions well. |
| [modelpath-env.md](../.public-agdocs/specs/modelpath-env.md) | In llm.interface:create_llm_client have model_path load from env var "INNOCUOUS_LLM_PATH". Add optional CLI arg and function args to override env var. | [55cf7ce](https://github.com/sutt/innocuous/commit/55cf7ce) | +24/-10 | +0/-0 | Two small mistakes in the genration as seen in the subsequent commit. |
| [devsummary-task-b.md](../.public-agdocs/specs/devsummary-task-b.md) | Update table in docs/dev-summary.md for v0.1.0 with git diff values for code changes columns. Each value represented as "+A/-D" format for additions/deletions from git diff --stat. | [d3321ed](https://github.com/sutt/innocuous/commit/d3321ed) | +0/-0 | +0/-0 | Modfied this script to be a little more complicated and factor in multiple slices of repo |
| [devsummary-task-a.md](../.public-agdocs/specs/devsummary-task-a.md) | Add updated taskfiles to markdown table in docs/dev-summary.md for v0.1.0 with filename, summary, and GitHub SHA links. Sort by date descending and include only specs/* files. | [9f91a82](https://github.com/sutt/innocuous/commit/9f91a82) | +0/-0 | +0/-0 | Modified this script to be re-useable for each new version.|
| [cli-add.md](../.public-agdocs/specs/cli-add.md) | Add CLI interface for stego-llm package with script "innocuous" having encode/decode subcommands. Include optional flags for verbosity, chunk size, and initial prompt options. Create tests for functionality. | [0cb642f](https://github.com/sutt/innocuous/commit/0cb642f) | +101/-0 | +139/-0 | Highly detailed and well formatted spec, generation works quite well, adds generous amount of tests with mocking. |

```
be74868 build: v0.2.0
466af55 specs: v0.2.0
e7b8d5b feat: add configurable LLM path and check-llm command
3dbcef6 fix: fixups and env example
0355954 feat: add check-llm subcommand to validate LLM configuration
c7cdd56 test: remove mock for moved create_llm_client function
010e17d fix: remove hardcoded model_path
55cf7ce feat: allow specifying LLM path via CLI arg or env var
6b3f7b0 format: ruff format for previous
36d836d fix: hardcode prompt for cli + test_cli configs
0cb642f feat: add innocuous command-line interface
0738198 build: update uv.lock for new pkg structure
447bb3b tests: create first demo test
42449fb refactor: ruff format applied (first time)
0f6c89d refactor: remove jupyter notebooks and notepad scripts
40eab8c refactor: manually unnec modules and funcs from new package structure
78770d5 refactor: another major pkg refactor
fa88e0b refactor: major package refactor (claude)
c10a969 refactor: move logging to central trace function (claude)
d3321ed feat: impl devsummary-task-b with claude (agro auto-commit)
d405351 docs: manual updates to dev-summary v0.1.0
9f91a82 feat: impl devsummary-task-a with claude (agro auto-commit)
```

## v0.1.0

This was a proof of concept stage. Lots of experimentation and scratch work.

Note: there is no comprehensive tests/ directory so `Tests Diff` will be n/a here.

| Task File | Contents (truncated) | Accepted SHA | Non-test Diffs | Test Diffs | Notes |
|------|-------------|---------|-------------|------------|-----------|
| [prepost-filter-decode.md](../.public-agdocs/specs/prepost-filter-decode.md) | Apply refactor of filter_tok logic to pre_accept_filter + post_accept_filter functions in src/main:main_decode. Allow main_decode to take into account same logic so decoded data matches input. Functions will be extended with additional details. | [960c697](https://github.com/sutt/innocuous/commit/960c697) | +2/-0 | n/a | simpler than anticipated. the fix on top was actually a problem with encoder logic being emulated. |
| [decode-accept-1.md](../.public-agdocs/specs/decode-accept-1.md) | Apply the accept_tok logic that was added to main_encode to main_decode. Use partial diff showing function usage. Allow main_decode to take into account same logic so decoded data matches input. Accept_tok will be extended with additional details. | [79a4c67](https://github.com/sutt/innocuous/commit/79a4c67) | +14/-0 | n/a | prompt uses the "previous diff pattern". fine solution, nothing too challenging. |
| [decode-branch.md](../.public-agdocs/specs/decode-branch.md) | Refactor decode_main function to handle situation where remaining_text may .startswith match with multiple eligible tokens. Need branching to check maxsize of first 2**chunk_size tokens after tok_filter. Apply hacky solution for now. | [cdabc98](https://github.com/sutt/innocuous/commit/cdabc98) | +48/-25 | n/a | phenomenal solution; implemented difficult concept in 1-shot. fix was only for an llm library bug the ai-coder couldn't have realized. |
| [decode1.md](../.public-agdocs/specs/decode1.md) | In src/main.py implement main_decode | [d4dd55e](https://github.com/sutt/innocuous/commit/d4dd55e) | +43/-4 | n/a | prompts is very terse, and ai-generation understands intent prefectly, get a little liberal with modifying other existing methods but in a helpful way. |

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