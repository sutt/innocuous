import copy
import json

import pytest

from examples import coded_postcard as postcard


@pytest.fixture
def encoded(tmp_path, monkeypatch):
    model = tmp_path / "fixture.gguf"
    model.write_bytes(b"fixture only; never loaded as a model")
    monkeypatch.setattr(postcard, "main_encode", lambda prompt, payload, **kwargs: prompt + "A peaceful afternoon.")
    monkeypatch.setattr(postcard, "main_decode", lambda *args, **kwargs: postcard.MESSAGE.encode("utf-8"))
    return postcard.encode_postcard(postcard.MESSAGE, model), model


def test_utf8_round_trip_preserves_model_and_exact_carrier(encoded):
    packet, model = encoded
    restored = json.loads(json.dumps(packet, ensure_ascii=False))
    assert postcard.decode_postcard(restored, model) == "Hẹn ở vườn."
    assert restored["model_sha256"] == postcard.model_sha256(model)
    assert restored["carrier"].startswith(postcard.PROMPT)


@pytest.mark.parametrize("field,value", [
    ("format", "other"), ("settings", {}), ("prompt", None),
    ("carrier", None), ("carrier", "edited text"), ("carrier", postcard.PROMPT),
    ("model_sha256", "0" * 64), ("llama_cpp_python", "different-version"),
])
def test_invalid_metadata_is_rejected_before_model_loading(encoded, monkeypatch, field, value):
    packet, model = encoded
    packet = copy.deepcopy(packet)
    packet[field] = value
    def unexpected_decode(*args, **kwargs):
        pytest.fail("invalid metadata must be rejected before inference")
    monkeypatch.setattr(postcard, "main_decode", unexpected_decode)
    with pytest.raises(ValueError):
        postcard.decode_postcard(packet, model)


def test_model_file_changes_are_detected(encoded):
    packet, model = encoded
    model.write_bytes(b"different weights")
    with pytest.raises(ValueError, match="same GGUF"):
        postcard.decode_postcard(packet, model)


@pytest.mark.parametrize("recovered", [None, b"wrong message"])
def test_failed_round_trip_is_not_returned(encoded, monkeypatch, recovered):
    _, model = encoded
    monkeypatch.setattr(postcard, "main_decode", lambda *args, **kwargs: recovered)
    with pytest.raises(ValueError):
        postcard.encode_postcard(postcard.MESSAGE, model)


def test_empty_message_is_rejected_before_inference(tmp_path):
    with pytest.raises(ValueError, match="nonempty"):
        postcard.encode_postcard("", tmp_path / "absent.gguf")


@pytest.mark.parametrize("packet", [None, [], "not a postcard"])
def test_nonobject_json_is_rejected(packet, tmp_path):
    with pytest.raises(ValueError, match="format"):
        postcard.decode_postcard(packet, tmp_path / "absent.gguf")
