add a cli interface for the stego-llm package and add a script which installs with the package which calls this cli.
- the script name should be "innocuous" 
- the script will have two main subcommands: "encode" and "decode"
> innocuous [optional-flags] [encode] [decode]
optional flags: 
-v, -vv
--chunk_size <CHUNK_SIZE> (int)
--initial-prompt-text <PROMPT> (str) 
--initial-prompt-file <path/to/promptfile> (str or path) this will attempt to read the content of the path to the file and pass as initial_prompt

The encode subcommand takes arguments:
> innocuous encode <flag>
--text <ASCII_TEXT> (str)
--bytes <BYTE_DATA> (str) This will be quoted text of form '\x99\xff' or hexidecimal '0f1e6f' which in converted to byte form
--btc-addr <BTC_ADDR> (str)
It will print the resulting encoded message from main_decode to stdout.
The above flags are mutually exclusive, and one is required.

The decode subcommand takes as arguments:
> innocuous decode <flag>
--message <MESSAGE> (str)
--file <path/to/file> (str or path) this will attempt to read the content of the path to the file, convert the contents to bytes and run main_decode.
This will print the decoded message from the input message of file to stdout.

Create several tests for this functionality in the tests/ directory in a separate file from existing ones.