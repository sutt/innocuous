# Dev Summary

## v0.2.3

#### `extra-args-test.md`
- **Spec Summary:** *Add 1-2 tests for llm_extra_args feature. Test that args pass through encode/decode to constructors without real inference. Example usage: llm_extra_args={"n_ctx": 1024}. Mock instantiation/loading.*
- **Commit Message:** *TBD*
- **Task Notes:** Simple task, not best execution.
- **Src Diffs:** +0/-0 | **Test Diffs:** +29/-0
- **Spec:** extra-args-test.md | **Patch Sha:** 9abdb61
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `cli-numlogprobs.md`
- **Spec Summary:** *Create optional CLI argument --num-logprobs with default value of 100.*
- **Commit Message:** *TBD*
- **Task Notes:** Simple.
- **Src Diffs:** +8/-4 | **Test Diffs:** +0/-0
- **Spec:** cli-numlogprobs.md | **Patch Sha:** fe8dbf6
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `integration-test.md`
- **Spec Summary:** *Add integration test: msg0 -> encode -> decode -> msg1, assert msg0==msg1. Use pytest marker for slow tests. Mock env variable or config for model_path.*
- **Commit Message:** *TBD*
- **Task Notes:** Tricky tests implemented with best practices.
- **Src Diffs:** +0/-0 | **Test Diffs:** +44/-0
- **Spec:** integration-test.md | **Patch Sha:** 6203b4a
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `type-main-funcs.md`
- **Spec Summary:** *Add type hints for args and return types to decoder.main_decoder and encoder.main_encode in stego_llm.core. Include expanded docstrings.*
- **Commit Message:** *TBD*
- **Task Notes:** Simple but the verbose docstrings are useful to handle with ai.
- **Src Diffs:** +48/-14 | **Test Diffs:** +0/-0
- **Spec:** type-main-funcs.md | **Patch Sha:** b00dd60
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `version-cmd.md`
- **Spec Summary:** *Enable CLI and Python import to display package version from pyproject.toml.*
- **Commit Message:** *TBD*
- **Task Notes:** Easy, but esoteric.
- **Src Diffs:** +10/-2 | **Test Diffs:** +0/-0
- **Spec:** version-cmd.md | **Patch Sha:** 80791f9
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

---

## v0.2.2

---

## v0.2.1

#### `devsummary-task-b.md`
- **Spec Summary:** *Update table in docs/dev-summary.md for v0.1.0 with git diff values for code changes columns. Each value represented as "+A/-D" format for additions/deletions from git diff --stat.*
- **Commit Message:** *TBD*
- **Task Notes:** 
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-0
- **Spec:** devsummary-task-b.md | **Patch Sha:** 97da5a8
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `devsummary-task-a.md`
- **Spec Summary:** *Add updated taskfiles to markdown table in docs/dev-summary.md for v0.1.0 with filename, summary, and GitHub SHA links. Sort by date descending and include only specs/* files.*
- **Commit Message:** *TBD*
- **Task Notes:** 
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-0
- **Spec:** devsummary-task-a.md | **Patch Sha:** 46468bd
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

---

## v0.2.0

#### `update-examples.md`
- **Spec Summary:** *Updates scripts in examples/ directory to reflect change about model_path needing to be passed in explicitly. Includes diffs for __init__.py, cli.py, core modules, and llm interface changes.*
- **Commit Message:** *TBD*
- **Task Notes:** Time-saving use-case of handling downstream breaking changes from a refactor.
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-0
- **Spec:** update-examples.md | **Patch Sha:** e7b8d5b
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `fix-tests.md`
- **Spec Summary:** *Update tests to pass after changes to create_llm_client import and function signature. Tests were failing because create_llm_client was moved from cli.py and the function interface changed to accept llm_path parameter.*
- **Commit Message:** *TBD*
- **Task Notes:** Spec uses the dump stdout + git diff data, and generation solves it.
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-10
- **Spec:** fix-tests.md | **Patch Sha:** c7cdd56
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `check-llm.md`
- **Spec Summary:** *Add subcommand "check-llm" and exportable function "check_llm" to verify LLM path from CLI/env var, check file existence, and execute simple inference task. Print terse confirmation of each step.*
- **Commit Message:** *TBD*
- **Task Notes:** Generation followed multiple separate instructions well.
- **Src Diffs:** +51/-9 | **Test Diffs:** +38/-0
- **Spec:** check-llm.md | **Patch Sha:** 0355954
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `modelpath-env.md`
- **Spec Summary:** *In llm.interface:create_llm_client have model_path load from env var "INNOCUOUS_LLM_PATH". Add optional CLI arg and function args to override env var.*
- **Commit Message:** *TBD*
- **Task Notes:** Two small mistakes in the genration as seen in the subsequent commit.
- **Src Diffs:** +24/-10 | **Test Diffs:** +0/-0
- **Spec:** modelpath-env.md | **Patch Sha:** 55cf7ce
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `devsummary-task-b.md`
- **Spec Summary:** *Update table in docs/dev-summary.md for v0.1.0 with git diff values for code changes columns. Each value represented as "+A/-D" format for additions/deletions from git diff --stat.*
- **Commit Message:** *TBD*
- **Task Notes:** Modfied this script to be a little more complicated and factor in multiple slices of repo
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-0
- **Spec:** devsummary-task-b.md | **Patch Sha:** d3321ed
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `devsummary-task-a.md`
- **Spec Summary:** *Add updated taskfiles to markdown table in docs/dev-summary.md for v0.1.0 with filename, summary, and GitHub SHA links. Sort by date descending and include only specs/* files.*
- **Commit Message:** *TBD*
- **Task Notes:** Modified this script to be re-useable for each new version.
- **Src Diffs:** +0/-0 | **Test Diffs:** +0/-0
- **Spec:** devsummary-task-a.md | **Patch Sha:** 9f91a82
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `cli-add.md`
- **Spec Summary:** *Add CLI interface for stego-llm package with script "innocuous" having encode/decode subcommands. Include optional flags for verbosity, chunk size, and initial prompt options. Create tests for functionality.*
- **Commit Message:** *TBD*
- **Task Notes:** Highly detailed and well formatted spec, generation works quite well, adds generous amount of tests with mocking.
- **Src Diffs:** +101/-0 | **Test Diffs:** +139/-0
- **Spec:** cli-add.md | **Patch Sha:** 0cb642f
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

---

## v0.1.0

#### `prepost-filter-decode.md`
- **Spec Summary:** *Apply refactor of filter_tok logic to pre_accept_filter + post_accept_filter functions in src/main:main_decode. Allow main_decode to take into account same logic so decoded data matches input. Functions will be extended with additional details.*
- **Commit Message:** *TBD*
- **Task Notes:** simpler than anticipated. the fix on top was actually a problem with encoder logic being emulated.
- **Src Diffs:** +2/-0 | **Test Diffs:** n/a
- **Spec:** prepost-filter-decode.md | **Patch Sha:** 960c697
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `decode-accept-1.md`
- **Spec Summary:** *Apply the accept_tok logic that was added to main_encode to main_decode. Use partial diff showing function usage. Allow main_decode to take into account same logic so decoded data matches input. Accept_tok will be extended with additional details.*
- **Commit Message:** *TBD*
- **Task Notes:** prompt uses the "previous diff pattern". fine solution, nothing too challenging.
- **Src Diffs:** +14/-0 | **Test Diffs:** n/a
- **Spec:** decode-accept-1.md | **Patch Sha:** 79a4c67
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `decode-branch.md`
- **Spec Summary:** *Refactor decode_main function to handle situation where remaining_text may .startswith match with multiple eligible tokens. Need branching to check maxsize of first 2**chunk_size tokens after tok_filter. Apply hacky solution for now.*
- **Commit Message:** *TBD*
- **Task Notes:** phenomenal solution; implemented difficult concept in 1-shot. fix was only for an llm library bug the ai-coder couldn't have realized.
- **Src Diffs:** +48/-25 | **Test Diffs:** n/a
- **Spec:** decode-branch.md | **Patch Sha:** cdabc98
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

#### `decode1.md`
- **Spec Summary:** *In src/main.py implement main_decode*
- **Commit Message:** *TBD*
- **Task Notes:** prompts is very terse, and ai-generation understands intent prefectly, get a little liberal with modifying other existing methods but in a helpful way.
- **Src Diffs:** +43/-4 | **Test Diffs:** n/a
- **Spec:** decode1.md | **Patch Sha:** d4dd55e
<details>
<summary>full details</summary> 
<h3>Spec</h3>
TBD
<h3>Patch</h3>
TBD
</details>

---
