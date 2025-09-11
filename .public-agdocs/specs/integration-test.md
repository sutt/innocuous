add new test which run an msg0 -> encode -> decode -> msg1, assert msg0==msg1 check.
use a pytest test marker to indicate these will run slowly and don't run by default.
add structure to mock the env variable or to pass in the model_path via a config.