#!/usr/bin/env python3
import argparse
import os
import time
from statistics import mean, stdev
from typing import List, Dict, Any, Optional

import requests
import torch
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams


# ------------- Configurable prompt -------------
def build_messages() -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": "You are a concise coding assistant."},
        {"role": "user", "content": "Write a Python function to reverse a linked list."}
    ]


# ------------- Utilities -------------
def now_ts() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")

def safe_stdev(xs: List[float]) -> float:
    return stdev(xs) if len(xs) >= 2 else 0.0

def count_tokens(tok: AutoTokenizer, text: str) -> int:
    # Using tokenizer to estimate generated tokens
    return len(tok.encode(text, add_special_tokens=False))


# ------------- In-process vLLM benchmark -------------
def bench_inprocess(
    model_id: str,
    tok: AutoTokenizer,
    prompt: str,
    repeats: int,
    max_tokens: int,
    tensor_parallel_size: int,
    max_model_len: int,
    temperature: float
) -> Dict[str, Any]:
    # Single LLM instance reused across runs to avoid re-load overhead
    llm = LLM(
        model=model_id,
        tensor_parallel_size=tensor_parallel_size,
        max_model_len=max_model_len,
    )
    sampler = SamplingParams(temperature=temperature, max_tokens=max_tokens)

    # Warmup
    _ = llm.generate([prompt], sampler)

    latencies, tps, gen_tokens_list, out_chars = [], [], [], []

    for i in range(repeats):
        t0 = time.perf_counter()
        outputs = llm.generate([prompt], sampler)
        dt = time.perf_counter() - t0

        text = outputs[0].outputs[0].text
        gen_tokens = count_tokens(tok, text)
        tokens_per_sec = (gen_tokens / dt) if dt > 0 else 0.0

        latencies.append(dt)
        tps.append(tokens_per_sec)
        gen_tokens_list.append(gen_tokens)
        out_chars.append(len(text))

    return {
        "engine": "inprocess_vllm",
        "repeats": repeats,
        "latencies_s": latencies,
        "tokens_per_sec": tps,
        "gen_tokens": gen_tokens_list,
        "output_chars": out_chars,
    }


# ------------- vLLM Server (HTTP) benchmark -------------
def chat_vllm_http(
    base_url: str,
    model: str,
    messages: List[Dict[str, str]],
    max_tokens: int,
    temperature: float,
    timeout: int,
    session: Optional[requests.Session] = None,
) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    s = session or requests.Session()
    r = s.post(
        f"{base_url}/chat/completions",
        json=payload,
        headers={"Authorization": "Bearer EMPTY"},
        timeout=timeout
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def bench_http(
    base_url: str,
    model: str,
    tok: AutoTokenizer,
    messages: List[Dict[str, str]],
    repeats: int,
    max_tokens: int,
    temperature: float,
    timeout: int
) -> Dict[str, Any]:
    session = requests.Session()

    # Warmup
    _ = chat_vllm_http(base_url, model, messages, max_tokens, temperature, timeout, session=session)

    latencies, tps, gen_tokens_list, out_chars = [], [], [], []
    for i in range(repeats):
        t0 = time.perf_counter()
        text = chat_vllm_http(base_url, model, messages, max_tokens, temperature, timeout, session=session)
        dt = time.perf_counter() - t0

        gen_tokens = count_tokens(tok, text)
        tokens_per_sec = (gen_tokens / dt) if dt > 0 else 0.0

        latencies.append(dt)
        tps.append(tokens_per_sec)
        gen_tokens_list.append(gen_tokens)
        out_chars.append(len(text))

    return {
        "engine": "vllm_server_http",
        "repeats": repeats,
        "latencies_s": latencies,
        "tokens_per_sec": tps,
        "gen_tokens": gen_tokens_list,
        "output_chars": out_chars,
    }


# ------------- Report writer -------------
def write_report(
    path: str,
    model_id: str,
    messages: List[Dict[str, str]],
    inproc: Dict[str, Any],
    http: Dict[str, Any],
    gpu_info: str,
    cuda_env: str
) -> None:
    lines = []
    lines.append(f"CodeLlama vLLM Benchmark Report")
    lines.append(f"Timestamp: {now_ts()}")
    lines.append(f"Model: {model_id}")
    lines.append(f"GPU: {gpu_info}")
    lines.append(f"CUDA_VISIBLE_DEVICES: {cuda_env}")
    lines.append("")
    lines.append("Prompt (messages):")
    for m in messages:
        lines.append(f"  - {m['role']}: {m['content']}")
    lines.append("\n==================== RESULTS ====================\n")

    def summarize(block: Dict[str, Any]) -> List[str]:
        lat = block["latencies_s"]
        tps = block["tokens_per_sec"]
        gen = block["gen_tokens"]
        chars = block["output_chars"]

        def fmt(arr):
            return f"avg={mean(arr):.4f}, std={safe_stdev(arr):.4f}, min={min(arr):.4f}, max={max(arr):.4f}"

        out = []
        out.append(f"Engine: {block['engine']}")
        out.append(f"Repeats: {block['repeats']}")
        out.append(f"Total latency (s):     {fmt(lat)}")
        out.append(f"Tokens/sec:            {fmt(tps)}")
        out.append(f"Generated tokens:      {fmt(gen)}")
        out.append(f"Output length (chars): {fmt(chars)}")
        return out

    lines += summarize(inproc)
    lines.append("")
    lines += summarize(http)
    lines.append("\n=================================================\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ------------- Main -------------
def main():
    parser = argparse.ArgumentParser(description="Benchmark CodeLlama with vLLM (in-process vs HTTP server).")
    parser.add_argument("--model-id", default="codellama/CodeLlama-7b-Instruct-hf")
    parser.add_argument("--base-url", default="http://localhost:8000/v1", help="vLLM server base URL")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--max-model-len", type=int, default=8192)
    parser.add_argument("--out", default="codellama_vllm_benchmark.txt")
    args = parser.parse_args()

    # Tokenizer + prompt (use the model's native chat template)
    tok = AutoTokenizer.from_pretrained(args.model_id, use_fast=True)
    messages = build_messages()
    prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    # Collect GPU/env info for the report
    try:
        gpu_info = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CUDA not available"
    except Exception:
        gpu_info = "Unknown GPU"
    cuda_env = os.environ.get("CUDA_VISIBLE_DEVICES", "not set")

    # Run benchmarks
    inproc = bench_inprocess(
        model_id=args.model_id,
        tok=tok,
        prompt=prompt,
        repeats=args.repeats,
        max_tokens=args.max_tokens,
        tensor_parallel_size=args.tensor_parallel_size,
        max_model_len=args.max_model_len,
        temperature=args.temperature,
    )

    http = bench_http(
        base_url=args.base_url.rstrip("/"),
        model=args.model_id,
        tok=tok,
        messages=messages,
        repeats=args.repeats,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        timeout=args.timeout,
    )

    # Write report
    write_report(
        path=args.out,
        model_id=args.model_id,
        messages=messages,
        inproc=inproc,
        http=http,
        gpu_info=gpu_info,
        cuda_env=cuda_env,
    )

    print(f"Done. Report saved to: {args.out}")


if __name__ == "__main__":
    main()
