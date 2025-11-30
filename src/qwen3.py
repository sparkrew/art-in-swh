from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
)

def chat_with_vllm(message: str) -> str:
    completion = client.chat.completions.create(
        model="qwen3-coder-30b-fp8",
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": message},
        ],
        max_tokens=256,
        temperature=0.1,
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    answer = chat_with_vllm("Generate a Python function to compute factorial.")
    print(answer)
