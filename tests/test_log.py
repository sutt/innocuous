import json
import numpy as np
from stego_llm.log import get_logger, reset_logger


def _zep(num: float):
    """test util to do float casting"""
    return float(np.float32(num))


def test_stego_logger(tmp_path):
    """Test StegoLogger functionality."""
    reset_logger()
    logger = get_logger()
    assert logger.step_count == 0
    assert logger.get_log_data() == {}

    # Step 0
    logits1 = {"tokA": np.float32(0.22), "tokB": np.float32(0.11)}
    logger.add_step(logits1)
    assert logger.step_count == 1
    expected_data_1 = {0: {"top_logits": {"tokA": _zep(0.22), "tokB": _zep(0.11)}}}
    assert logger.get_log_data() == expected_data_1

    # Step 1
    logits2 = {"tokC": np.float32(0.33), "tokD": np.float32(0.44)}
    logger.add_step(logits2)
    assert logger.step_count == 2
    expected_data_2 = {
        0: {"top_logits": {"tokA": _zep(0.22), "tokB": _zep(0.11)}},
        1: {"top_logits": {"tokC": _zep(0.33), "tokD": _zep(0.44)}},
    }
    assert logger.get_log_data() == expected_data_2

    # # Test dump
    log_file = tmp_path / "test.log"
    logger.dump(str(log_file))

    with open(log_file, "r") as f:
        loaded_data = json.load(f)

    # json load will give keys as strings
    loaded_data_int_keys = {int(k): v for k, v in loaded_data.items()}
    assert loaded_data_int_keys == expected_data_2

    # # Test singleton behavior
    logger2 = get_logger()
    assert logger is logger2
    assert logger2.step_count == 2

    # # Test reset
    reset_logger()
    logger3 = get_logger()
    assert logger is not logger3
    assert logger3.step_count == 0
