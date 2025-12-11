# Art in Software Heritage
```
How much of humanity's source code is for the arts?
```
This repo includes scripts, tools, notes, data gathered to answer this question. Work done by the software performing art crew in Montreal.

Lists of artists used to search for art are in the following [link](https://github.com/sparkrew/art-in-swh/tree/main/list_of_artisits).


## GitHub Repos Analysis

### URL colection and filtering

### URL Priorization

The url rank reflects the percentage of its topics we consider to be interesting (i.e., topic is listed in our cryptpad list of topics and file extensions - with a few additions).


## Running code in CalculQC

In the login node:

1. Navigate to the repo's root folder
2. Create venv
3. Install requirements.txt

To use the QWEN3 model, open a session in Rorqual's compute node with the NVIDIA_H100_80GB_HBM3_3G.40GB GPU.

If you open a Jupyter server, navigate to the repo's root folder.

1. Open one terminal and run `./src/start-qwen3.sh`
    - This command starts a VLLM API to interact with the model
2. Open another terminal, activate venv, and run `python src/qwen3.py`

The `config.yml` contains the relevant i/o paths.


### Shared files

- Go to: `./links/projects/def-baudry/shared/data` to find code sources.
- Go to: `./links/projects/def-baudry/shared/huggingface` to find LLM models.


### Useful commands

#### Download models

To download models from HuggingFace (from the login node *always*):

```
export HF_HUB_CACHE=/links/projects/def-baudry/shared/huggingface
HF_HUB_DISABLE_XET=1 hf download --max-workers=1 Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
```

This command will download the LLM in a shared folder.


## Open questions

- We use two terminals sessions, one for the API and another to run script. How to run both in a scheduled batch job?
