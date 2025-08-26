### Script Vars
Utilize these variables below for the task as you read it and process it. The script var will be denoted with $my_script_var when utilized and should be read the value corresponding.

- target_doc: docs/dev-summary.md 
- version_to_update: v0.1.0
- max_summary_chars: 250
- repo_url: github.com/sutt/innocuous

### Steps to Update & Execute this Spec
This section should be ignored by the AI agent; it's for the developer's reference to edit this file for:
Updating:
- Update the variables in script vars
- Run the 3 reference commands and add output to the sections "Command Outputs".
Executing:
- Claude often excels at this task
- Descriptive commit messages are helpful; multiple commit messages with same verbiage can confuse it.

### Command Reference:
These commands you should not run or pay attention to any of these. They are simply are reference for the developer:
> git diff --stat v0.1.0 v0.2.0 -- .public-agdocs/specs
> ls -lt .agdocs/specs/ 
> git log --oneline --no-merges  --not  -n 36

### Task
These are the instructions for your task. Remember to insert the script vars from above when seeing avariable preseeded by $.

Add the updated taskfiles to a markdown table in $target_doc 
for $version_to_update with a row containing:
- just the filename and have it be linked with relative path notation to where it resides in .public-agdocs
- a summary of the files contents (max $max_summary_chars chars)
- add a field that links to a 6-char git sha entry  on the github repo: $repo_url. Do your best guess to find the corresponding commit (available with commit message below). If your guess is too uncertain, or it appears there is no commit for it, place an n/a for this entry.

Rules for the table:
- only include specs/* files for rows
- sort by date order desc (the date information will supplied at the end)
- don't update the rightmost three columns ("diffs" + "notes"). These values will be supplied in a later task.

#### Command Outputs

##### Spec Changes
Here's the result for the following command:

git diff --stat -- .public-agdocs/specs

 .public-agdocs/specs/decode-accept-1.md       | 71 ++++++++++++++++++++++
 .public-agdocs/specs/decode-branch.md         |  6 ++
 .public-agdocs/specs/decode1.md               |  1 +
 .public-agdocs/specs/prepost-filter-decode.md | 77 ++++++++++++++++++++++++

##### Specs Time-Sorted
Here's the information for the date created which should be used to sort the rows for the table above.

Results of the command: 

ls -lt .agdocs/specs/ 

-rw-r--r-- 1 user user 2541 Aug 23 08:28 prepost-filter-decode.md
-rw-r--r-- 1 user user 2216 Aug 21 19:35 decode-accept-1.md
-rw-r--r-- 1 user user  853 Aug 20 18:20 decode-branch.md
-rw-r--r-- 1 user user   36 Aug 20 14:10 decode1.md

##### Commit Logs
Here's the output of the following command, use this to link a solution sha to a task file

git log --oneline --no-merges  --not  -n 36

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
