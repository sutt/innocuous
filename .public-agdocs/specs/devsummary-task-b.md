### Script Vars
Utilize these variables below for the task as you read it and process it. The script var will be denoted with $my_script_var when utilized and should be read the value corresponding.

- target_doc: docs/dev-summary.md 
- version_to_update: v0.2.3
- diffs_main_directory: stego_llm
- diffs_on_other_directories: tests

### Steps to Update & Execute this Spec
This section should be ignored by the AI agent; it's for the developer's reference to edit this file for:
Updating:
- Update the variables in script vars:
    - the diffs vars are helpful for different repo setups
Executing:
- Claude excels at this task.
- Enable the `Bash(git:*)` permissions for the claude agent.

### Task
These are the instructions for your task. Remember to insert the script vars from above when seeing a variable preseeded by $.
update the table in $target_doc:
- update the table for $version_to_update
- add values for all (or some of) the "code changes" / "diffs" columns:
    - use the column name to understand which slices of the codebase should be considered for the diffs.
    - these code diffs should only apply to the particular git commit referenced in that row of the table (it should not be the total diffs over the whole version)
    - for the first diff column, use the diffs from within directory $diff_main_directory
    - for the second diff column, use the the diffs from within directory $diff_on_other_directories
- each value should be represented as "+A/-D" where A is the number of additions and -D is deletion or modifications from a git diff / git diff --stat,
    - e.g. "+23/-12", or "+5/-0"

Use git commands to investigate these commit shas and run git diffs that will allows you to fill in the full table.

Rules used to build the table previously:
- only include specs/* files for rows
- sort by date order desc (the date information will supplied at the end)

Reference for commit sha's in the table
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


