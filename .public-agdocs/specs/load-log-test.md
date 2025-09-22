### Main Task
We are able to output a logfile of the top logits at each iteration. We want to load this json and then use it as the return data to mocked implementation of get_token_probabilities.

Implement a .load(log_file=) method in stego_llm.log which will load the json in the log_file to the log_data, plus any additional transfroms nec.

In stego_llm.llm.mock, implement a proc_gen_tokens_v3 which performs this and make it selectable from the factory create_mock_get_token_probabilities. 
- Since the loaded data will have a set number of top_logits per logit, you can filter it to reduce the amount of items returned based on num_output, but if the requested num_outputs is larger than those available, raise a warning but continue to return the max number of logits.

Modify the mocking factory method to be able to pass a filename / filepath to a log file
- The default directory to load from is tests/data/recorded-logits.
- Currently there exists an example of a log file in tests/data/recorded-logits/visit-boston-1.log which was created by running ./examples/visit-boston.sh.

In tests/test_simulate_llm implement a encode-decode cycle style test with the v3 proc_gen_token patching method, with function name "test_encode_decode_simulation_v3".

### Misc Info (ignore implementing this)
- token values are logged after applying logits_to_probabilities() thus they are logged as probabilities not logprobs. We should convert these amounts on .load()