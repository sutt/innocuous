"""The coded-message example must stay reproducible from committed logits."""

from examples.coded_message import (
    INITIAL_PROMPT,
    SECRET_MESSAGE,
    run_coded_message,
)


def test_coded_message_round_trip():
    covertext = run_coded_message()
    assert covertext.startswith(INITIAL_PROMPT)
    assert covertext != INITIAL_PROMPT
    assert SECRET_MESSAGE == b"groovy baby"
