### Script Vars
Utilize these variables below for the task as you read it and process it. The script var will be denoted with $my_script_var when utilized and should be read the value corresponding.

- target_doc: docs/dev-summary.md 
- version_to_update: v0.1.0
- diffs_main_directory: src
- diffs_on_other_directories: n/a

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
    - use the column name to understand which slices of the codebase should be considered for the diffs
    - for the first diff column, use the diffs in $diff_main_directory
    - for other columns, use the columns name as a hint to try to match to a directory in repo root, and use the $diff_on_other_directories values for guidance (if the value is set to n/a then place "n/a" in the all the other non-main diff columns for the version being updated.)
- each value should be represented as "+A/-D" where A is the number of additions and -D is deletion or modifications from a git diff / git diff --stat,
    - e.g. "+23/-12", or "+5/-0"

Use git commands to investigate these commit shas and run git diffs that will allows you to fill in the full table.

Rules used to build the table previously:
- only include specs/* files for rows
- sort by date order desc (the date information will supplied at the end)

Reference for commit sha's in the table
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


