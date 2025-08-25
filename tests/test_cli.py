import logging

import pytest

from stego_llm import cli


def test_encode_text(mocker):
    """Test encode command with --text."""
    mocker.patch("sys.argv", ["innocuous", "encode", "--text", "hello"])
    mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
    mock_create_llm = mocker.patch("stego_llm.cli.create_llm_client")
    mocker.patch("builtins.print")

    cli.main()

    mock_create_llm.assert_called_once()
    mock_main_encode.assert_called_once()
    assert mock_main_encode.call_args.kwargs["msg"] == b"hello"


def test_encode_bytes(mocker):
    """Test encode command with --bytes."""
    mocker.patch("sys.argv", ["innocuous", "encode", "--bytes", "68656c6c6f"])  # "hello" in hex
    mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
    mocker.patch("stego_llm.cli.create_llm_client")
    mocker.patch("builtins.print")

    cli.main()

    mock_main_encode.assert_called_once()
    assert mock_main_encode.call_args.kwargs["msg"] == b"hello"


def test_encode_btc_addr(mocker):
    """Test encode command with --btc-addr."""
    addr = "bc1q..."
    mocker.patch("sys.argv", ["innocuous", "encode", "--btc-addr", addr])
    mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
    mocker.patch("stego_llm.cli.create_llm_client")
    mocker.patch("builtins.print")

    cli.main()

    mock_main_encode.assert_called_once()
    assert mock_main_encode.call_args.kwargs["msg"] == addr.encode("utf-8")


def test_decode_message(mocker):
    """Test decode command with --message."""
    mocker.patch("sys.argv", ["innocuous", "decode", "--message", "some encoded message"])
    mock_main_decode = mocker.patch("stego_llm.cli.main_decode", return_value=b"decoded")
    mocker.patch("stego_llm.cli.create_llm_client")
    mocker.patch("builtins.print")

    cli.main()

    mock_main_decode.assert_called_once()
    assert mock_main_decode.call_args.kwargs["encoded_prompt"] == "some encoded message"


def test_decode_file(mocker, tmp_path):
    """Test decode command with --file."""
    p = tmp_path / "message.txt"
    p.write_text("file encoded message")
    mocker.patch("sys.argv", ["innocuous", "decode", "--file", str(p)])
    mock_main_decode = mocker.patch("stego_llm.cli.main_decode", return_value=b"decoded")
    mocker.patch("stego_llm.cli.create_llm_client")
    mocker.patch("builtins.print")

    cli.main()

    mock_main_decode.assert_called_once()
    assert mock_main_decode.call_args.kwargs["encoded_prompt"] == "file encoded message"


def test_initial_prompt_text(mocker):
    """Test --initial-prompt-text flag."""
    mocker.patch("sys.argv", ["innocuous", "--initial-prompt-text", "my prompt", "encode", "--text", "t"])
    mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
    mocker.patch("stego_llm.cli.create_llm_client")
    mocker.patch("builtins.print")

    cli.main()

    mock_main_encode.assert_called_once()
    assert mock_main_encode.call_args.kwargs["initial_prompt"] == "my prompt"


def test_initial_prompt_file(mocker, tmp_path):
    """Test --initial-prompt-file flag."""
    p = tmp_path / "prompt.txt"
    p.write_text("prompt from file")
    mocker.patch("sys.argv", ["innocuous", "--initial-prompt-file", str(p), "encode", "--text", "t"])
    mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
    mocker.patch("stego_llm.cli.create_llm_client")
    mocker.patch("builtins.print")

    cli.main()

    mock_main_encode.assert_called_once()
    assert mock_main_encode.call_args.kwargs["initial_prompt"] == "prompt from file"


def test_chunk_size(mocker):
    """Test --chunk_size flag."""
    mocker.patch("sys.argv", ["innocuous", "--chunk_size", "4", "encode", "--text", "t"])
    mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
    mocker.patch("stego_llm.cli.create_llm_client")
    mocker.patch("builtins.print")

    cli.main()

    mock_main_encode.assert_called_once()
    assert mock_main_encode.call_args.kwargs["chunk_size"] == 4


@pytest.mark.parametrize(
    "verbose_arg, expected_level",
    [
        ([], logging.WARNING),
        (["-v"], logging.INFO),
        (["-vv"], logging.DEBUG),
        (["-vvv"], logging.DEBUG),
    ],
)
def test_verbosity(mocker, verbose_arg, expected_level):
    """Test verbosity flags."""
    argv = ["innocuous"] + verbose_arg + ["encode", "--text", "t"]
    mocker.patch("sys.argv", argv)
    mocker.patch("stego_llm.cli.main_encode")
    mocker.patch("stego_llm.cli.create_llm_client")
    mock_basic_config = mocker.patch("logging.basicConfig")
    mocker.patch("builtins.print")

    cli.main()

    mock_basic_config.assert_called_once()
    assert mock_basic_config.call_args.kwargs["level"] == expected_level
