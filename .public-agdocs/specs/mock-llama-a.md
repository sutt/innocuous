### Overview
Let's build a sophisticated mock system for the Llama object from the llama-cpp-python package. This will be used for testing amd simulation of logic that can run quickly, instead of actual llm inference which works slowly.

In particular we want to mock the methods in stego_llm/llm/interface:
- create_llm_client: we should create a mock object which does not actually load the weights file.
- get_token_probabilities: return a dictionary mock values for the logprobs with number of items = num_output
    - Do not actually run inference forward pass on any llm.

#### Mocking Logic
- return type for get_token_probabilities: Dict[str, np.float32]
    - number of items = num_output argument
    - key (str): will look like this " a1" or " bb16"
    - value (np.float32): should be in range -0.1 to -10.0
        - (notice these will be transformed into probabilities with np.exp in a later step but you don't need to worry about this in the implementation.)
- llama mock object (returned from get_llm_client) should have a counter property in it that will be incremented each time it's called in get_token_probabilities.

#### Return Value for get_token_probabilities
Create a separate module that will allow multiple different versions of how to proceudrally generate keys and values for the dictionary that's returned in the mocked get_token_probabilities.

For the first version which we'll implment here when returning mock values for get_token_probabilites. Here's some pseudo code:
    proc_gen_tokens(iter_num=mock_llama_obj.counter, num_logprobs=num_logprobs)

Keys: these will have  a leading whitespace + a letter-encoding for the iteration number + token number number-encoding 
    - iter=0 => a, iter=1 => b iter=25 => z , iter=26 => aa, ...
Values: you can generate these once as a random function which generate np.float32 values. This should happen at load time once (instead of each time the mock function is called ). The values aren't too important for this implementation.

Some examples:

iter0, num_output=50: {
    " a1": np.float(-2.0),
    " a2": np.float(-2.5),
    ...
    " a50": np.float(-20.0),
}

iter27, num_output=100: {
    " bb1": np.float(-2.0),
    " bb2": np.float(-2.5),
    ...
    " b100": np.float(-20.0),
}

### Specific Task
- Create a new file tests/test_simulate_llm.py
- create a test that prove that the mocking methods work by infering ten tokens of text.
    - provide a method to run this individual function in the file