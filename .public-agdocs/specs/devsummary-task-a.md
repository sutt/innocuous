### Script Vars
Utilize these variables below for the task as you read it and process it. The script var will be denoted with $my_script_var when utilized and should be read the value corresponding.

- target_doc: docs/dev-summary.md 
- version_to_update: v0.2.3
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
> git diff --stat v0.2.2 v0.2.3 -- .public-agdocs/specs
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

git diff --stat v0.2.2 v0.2.3 -- .public-agdocs/specs

 .public-agdocs/specs/cli-numlogprobs.md   |  1 +
 .public-agdocs/specs/extra-args-test.md   | 92 +++++++++++++++++++++++++++++++
 .public-agdocs/specs/integration-test.md  |  3 +
 .public-agdocs/specs/type-main-funcs.md   |  6 ++
 .public-agdocs/specs/version-cmd.md       |  1 +
 7 files changed, 175 insertions(+), 84 deletions(-)



##### Specs Time-Sorted
Here's the information for the date created which should be used to sort the rows for the table above.

Results of the command: 

ls -lt .agdocs/specs/ 

-rw-r--r-- 1 user user  3348 Sep 11 12:10 extra-args-test.md
-rw-r--r-- 1 user user    81 Sep 11 08:32 cli-numlogprobs.md
-rw-r--r-- 1 user user   251 Sep  4 16:26 integration-test.md
-rw-r--r-- 1 user user   169 Sep  3 19:16 type-main-funcs.md
-rw-r--r-- 1 user user   104 Sep  3 18:46 version-cmd.md


##### Commit Logs
Here's the output of the following command, use this to link a solution sha to a task file

git log --oneline --no-merges  --not  -n 36

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
