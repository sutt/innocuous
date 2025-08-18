from llama_cpp import Llama



def main():
    llm = Llama(
        model_path="../data/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        seed=1, # Uncomment to set a specific seed
        # n_gpu_layers=-1, # Uncomment to use GPU acceleration
        # n_ctx=2048, # Uncomment to increase the context window
    )
    output = llm(
        "Q: What is the largest planet in the solar system? A: ",
        max_tokens=32, 
        stop=["Q:", "\n"],
        echo=True
    )
    print(output)


if __name__ == "__main__":
    main()
