import os
import json
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig

hub = Path(os.path.expanduser("~/.cache/huggingface/hub"))
base = hub / "models--codellama--CodeLlama-7b-Instruct-hf"

# Prefer the ref in refs/main; fall back to the newest snapshot
ref_file = base / "refs" / "main"
commit = ref_file.read_text().strip()

MODEL_PATH = str(base / "snapshots" / commit)

## LOADING MODELS
# 1. tokenizer
tok = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    use_fast=True,
    local_files_only=True,
)

# 2. LLM
# Set quantization and load model
q_config = BitsAndBytesConfig(
   load_in_4bit=True,
   bnb_4bit_quant_type="nf4",
   bnb_4bit_use_double_quant=True,
   bnb_4bit_compute_dtype=torch.bfloat16
) 
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    local_files_only=True,
    device_map="auto",
    low_cpu_mem_usage=True,
    quantization_config=q_config,
    attn_implementation="sdpa", # flash attention
    dtype=torch.bfloat16, # and changing dtype to lower precision
)

# Prompt function
def prompt(prompt, max_new_tokens=128):
    inst = f"<s>[INST] {prompt.strip()} [/INST]"
    inputs = tok(inst, return_tensors="pt").to(model.device)
    with torch.inference_mode():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            num_beams=1,
            pad_token_id=tok.eos_token_id,
            use_cache=True,
        )
    return tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()




