in llm.interface:create_llm_client
have the model_path arg load from an env var "INNOCUOUS_LLM_PATH"
- on the cli add an optional arg to pass the 
- add an optional arg "llm_path" to main_decode and main_encode 
- the cli arg and function arg should override the env var if both are present