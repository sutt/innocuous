refactor decode_main function to deal with the following situation:
remaining_text may .startswith match with multiple eligible tokens on that iteration.
for example, if remaining_text = "all above" and tok.keys() is ["a","go", "all"] there are two matches. Imagine that the encoder chose "all" but the decoder, as it is now written will select "a" since it comes first in iteration. Then on the next step or subsequent steps it will encounter an error.
we likely need a way to do branching, and check 
note bene: the maxsize of tokens you need to search is the first 2**chunk_size tokens after the tok_filter step.
note bene: we can apply a hacky solution for now where we don't fully solve it perfectly but try to back-up slighlty and go the other direction. One way to do this could be to go back one or two words (separated by a space) and try again