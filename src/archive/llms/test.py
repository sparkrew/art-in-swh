# ping_vllm_min.py
import requests
BASE = "http://0.0.0.0:8000"
print("health:", requests.get(f"{BASE}/health").json())
resp = requests.post(f"{BASE}/v1/chat/completions",
    headers={"Authorization":"Bearer EMPTY"},
    json={"model":"codellama/CodeLlama-7b-Instruct-hf",
          "messages":[{"role":"user","content":"ping"}],
          "max_tokens":16})
print(resp.json()["choices"][0]["message"]["content"])
