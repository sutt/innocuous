### Main task
Currently, stego_llm.core.trace gets a dictionary of "tokens_processed" from the encoding step passed to it and logs it out to stderr.

For this new feature: we want to store that dictionary of tokens for each step and then dump the full log at the end.

The datastructure should be:
- first level: iteration number
- second level: will just have the top_logits (the data passed to trace via)
{
    0: {
        "top_logits" : {
            "tokA" : 0.22,
            "tokB" : 0.11,
            ...
        }

    },
    1: {
        "top_logits" : {
            "tokA" : 0.32,
            "tokB" : 0.21,
            ...
        }
    }
    ...
}

### CLI additions
Add an optional flag to cli for option to enable this:
innocuous [--log-file] [LOGFILE] <encode/decode>
- if --log-file is supplied then this logging will be enabled.
- if LOGFILE argument is supplied is will be a filepath to where the log is dumped, if the flag is added but no argument is supplied, it will default to current working directory of innocuous.log

### Extra notes
- the tokens dictionary will have values as np.float, so these need to be serialized 
- this logging should be in a separate module and ideally works when the user
- only implement for encode (for now)
- add some unit tests for the cli and for the functionality)
