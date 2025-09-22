### main task
In tests/test_replay_v1:test_gen_1 add extra patching logic/methods to account for poetneital backtracking in decode for resetting iteration number in MockLlama to align with recorded-logits logs key.

### details
- tests/test_replay_v1:test_gen_0 passes but tests/test_replay_v1:test_gen_1 xfails. these tests have the same logic but use different example data from gen_schedule. 
- In the tests that xfails it's because the backtracking step is hit: _trace_decoding_step("branch_deadend", possible_matches=possible_matches, state=state). see the example of how this prints out below when two toptokens have overlapping key values, e.g. "realm" and "real".
- The reason this causes a test of mocked get_token_probabilities to fail is because the MockLlama.counter keeps getting incremented, when it should be rewound to match the number of decoder.main_decode.solve popped off the stack.

Add logic that will the MockLlama counter to be decremented / rewinded or stay aligned with current iteration after backtracking in main_decode occurs.

### trace example
DEBUG:stego_llm.core.trace:branch deadend, possible_matches: [(1, ' realm'), (6, ' real')] | state: ('Below is an iambic penatameter poem. Complete it:\nThe king of all the', ' realms did lie there weak,\nWith eyes that wept their last goodbye to day,\nThe crown did glister by his lifeless cheeks,\nYet still no heir to')

### quickstart
You can run the files as:
> uv run pytests tests/test_replay_v1
and get:
collected 2 items
tests/test_replay_v1.py .x                                                            [100%]

=============================== 1 passed, 1 xfailed in 0.44s ==

or you run:
> uv run tests/test_replay_v1.py
and get:


tests/test_replay_v1.py::test_gen_0 
initial_prompt: 'Below is an iambic penatameter poem. Complete it:
The king'
secret_message: b'hello world'
encoded_prompt: 'Below is an iambic penatameter poem. Complete it:
The king with a scepter in hand so bold,
His subjects before him knelt and told,
Of fields barren and crops failing so long,
He vowed to his subjects their plight was not strong,
He swore he had means to make right the wronged past wrongs and right them soon'
decoded_message: b'hello world'
PASSED
tests/test_replay_v1.py::test_gen_1 
initial_prompt: 'Below is an iambic penatameter poem. Complete it:
The king'
secret_message: b'hello world'
encoded_prompt: 'Below is an iambic penatameter poem. Complete it:
The king of all the realms did lie there weak,
With eyes that wept their last goodbye to day,
The crown did glister by his lifeless cheeks,
Yet still no heir to'
decoded_message: None
XFAIL