#!/bin/bash
# start-llm.sh
# make sure to be in the repo's root folder to start

# fail fast if something goes wrong
set -e

# # activate your venv
source .venv/bin/activate

# CUDA_VISIBLE_DEVICES=0 \
# vllm serve ../links/projects/def-baudry/shared/huggingface/models--Qwen--Qwen3-Coder-30B-A3B-Instruct-FP8/snapshots/e8ab3f2db9e388999a004eea5a31c16a8b517bc0 \
#   --host 0.0.0.0 \
#   --port 8000 \
#   --served-model-name qwen3-coder-30b-fp8 \
#   --dtype auto \
#   --max-model-len 8192 \
#   --gpu-memory-utilization 0.9


# CUDA_VISIBLE_DEVICES=0 \
# vllm serve ../links/projects/def-baudry/shared/huggingface/models--Qwen--Qwen3-Coder-30B-A3B-Instruct-FP8/snapshots/e8ab3f2db9e388999a004eea5a31c16a8b517bc0 \
#     --host 0.0.0.0 \
#     --port 8000 \
#     --served-model-name qwen3-coder-30b-fp8 \
#     --dtype auto \
#     --max-model-len 32768 \
#     --gpu-memory-utilization 0.92 \
#     --max-num-batched-tokens 8192

  # --max-model-len 32768 \
  # --gpu-memory-utilization 0.9 \
  # --max-num-batched-tokens 2048 \
  # --max-num-seqs 4



  #### paralelismo
CUDA_VISIBLE_DEVICES=0 \
vllm serve ../links/projects/def-baudry/shared/huggingface/models--Qwen--Qwen3-Coder-30B-A3B-Instruct-FP8/snapshots/e8ab3f2db9e388999a004eea5a31c16a8b517bc0 \
  --host 0.0.0.0 \
  --port 8000 \
  --served-model-name qwen3-coder-30b-fp8 \
  --dtype auto \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.9 \
  --max-num-batched-tokens 32768 \
  --max-num-seqs 32