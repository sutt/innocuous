add a subcommand to the script "check-llm"
add an exportable function "check_llm"
running this command or function should:
check if llm_path is supplied either via cli or env var,
if so, it checks if the file exists
and if so, attempts to execute a simple inference task with the llm, you can use the llm.interface:demo function for this with the nec modifications to use env/cli arg to pass to create_llm_client. Don't print the logprobs by default but only in the case verbose (-vv) is invoked.

Printout a terse confirmation of each step.

Add some tests for loading llm-path from cli/env and running this subcommand.