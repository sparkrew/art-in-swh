import os
import json
from openai import OpenAI
from collections import Counter
import matplotlib.pyplot as plt
from qwen3_prompts import *


# Global vars
CLIENT = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key=""
)

PROMPT_TEMPLATE = PROMPT_2

def chat_with_vllm(
    user_prompt: str,
    model: str = "qwen3-coder-30b-fp8",
    system_prompt: str = "You are a helpful coding assistant.",
    max_tokens: int = 256,
    temperature: float = 0.1
    ) -> str:
    return CLIENT.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    ).choices[0].message.content

def list_src_files(dir):
    """
    Given a dir, it returns the list of source files to analyse
    """
    files = os.listdir(dir)
    files = [f for f in files if f.endswith(('.js', '.html')) and os.path.isfile(os.path.join(dir, f))]
    return files


def get_manual_annotation(file_path):
    """
    Given a file, it returns its json labels
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def read_file_content(file_path):
    """
    Read content of source file
    """
    with open(file_path, 'r') as f:
        return f.read()


def get_file_prediction(file_name, src_content):
    """
    Given a txt string of a file, generate its labels.
    """
    user_prompt = f"{PROMPT_TEMPLATE}\n ```\n{src_content}\n```"
    model_output = chat_with_vllm(user_prompt)
    try:
        result = json.loads(model_output)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON for {file_name}: {model_output}")
        result = {"error": "invalid_json", "raw_output": model_output}
    return result


def export_json(filepath, content):
    with open(filepath, 'w') as f:
        json.dump(content, f)
        

def process_files(examples_dir, batch_processing=False):
    """
    Process all source files in examples directory

    args:
        examples_dir (str): file path with the src files
        batch_processing (bool): will control if exports 1 json per file or multiple jsons. NotImplementedYet.
    """
    src_files = list_src_files(examples_dir)

    for file_name in src_files:
        
        file_path = os.path.join(examples_dir, file_name)
        src_content = read_file_content(file_path)
        predicted_labels = get_file_prediction(file_path, src_content)

        # Export one json per src file
        file_name = "".join(file_name.split(".")[:-1]) + ".json"
        output_file_path = os.path.join(examples_dir + "/results" , file_name)  
        export_json(output_file_path, predicted_labels)

        # break


def compute_label_accuracy(true_dir=".", pred_dir="results"):

    keys = ["entities", "interaction", "outcome"]

    correct = {k: 0 for k in keys}
    total = {k: 0 for k in keys}

    true_files = [
        f for f in os.listdir(true_dir)
        if f.endswith(".json") and os.path.isfile(os.path.join(true_dir, f))
    ]

    for fname in true_files:
        true_path = os.path.join(true_dir, fname)
        pred_path = os.path.join(pred_dir, fname)
        if not os.path.exists(pred_path):
            continue

        with open(true_path) as f:
            true_labels = json.load(f)
        with open(pred_path) as f:
            pred_labels = json.load(f)

        all_ok = True
        for k in keys:
            total[k] += 1
            if set(true_labels.get(k, [])) == set(pred_labels.get(k, [])):
                correct[k] += 1
            else:
                all_ok = False

        overall_total += 1
        if all_ok:
            overall_correct += 1

    acc = {}
    for k in keys:
        acc[k] = (correct[k] / total[k]) if total[k] else 0.0

    return acc


def compute_and_save_label_accuracy(
    true_dir=".", pred_dir="results", out_filename="accuracy.txt"):

    os.makedirs(pred_dir, exist_ok=True)
    acc = compute_label_accuracy(true_dir=true_dir, pred_dir=pred_dir)
    out_path = os.path.join(pred_dir, out_filename)

    with open(out_path, "w") as f:
        for key, value in acc.items():
            f.write(f"{key}: {value:.6f}\n")

    return acc



def plot_label_distribution(true_dir=".", pred_dir="results",
                            out_filename="label_distribution.png"):
    """
    Computes label frequencies (true vs predicted), plots them,
    and saves the figure to pred_dir/out_filename.
    """
    os.makedirs(pred_dir, exist_ok=True)

    true_counts = Counter()
    pred_counts = Counter()

    true_files = [
        f for f in os.listdir(true_dir)
        if f.endswith(".json") and os.path.isfile(os.path.join(true_dir, f))
    ]

    for fname in true_files:
        true_path = os.path.join(true_dir, fname)
        pred_path = os.path.join(pred_dir, fname)

        if not os.path.exists(pred_path):
            continue

        with open(true_path, "r") as f:
            true_labels = json.load(f)
        with open(pred_path, "r") as f:
            pred_labels = json.load(f)

        for key in ["entities", "interaction", "outcome"]:
            for tag in true_labels.get(key, []):
                true_counts[tag] += 1
            for tag in pred_labels.get(key, []):
                pred_counts[tag] += 1

    all_labels = sorted(set(true_counts) | set(pred_counts))
    xs = list(range(len(all_labels)))
    x_true = [x - 0.2 for x in xs]
    x_pred = [x + 0.2 for x in xs]
    true_vals = [true_counts.get(lbl, 0) for lbl in all_labels]
    pred_vals = [pred_counts.get(lbl, 0) for lbl in all_labels]

    plt.figure(figsize=(10, 5))
    plt.bar(x_true, true_vals, width=0.4, label="True")
    plt.bar(x_pred, pred_vals, width=0.4, label="Predicted")
    plt.xticks(xs, all_labels, rotation=45, ha="right")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(pred_dir, out_filename)
    plt.savefig(out_path, dpi=150)
    plt.close()
    

if __name__ == "__main__":
    examples_dir = "examples"
    
    print("Processing files...")
    results = process_files(examples_dir)
    print("\n", results)
    
    acc = compute_and_save_label_accuracy(
        true_dir=examples_dir,
        pred_dir=examples_dir+"/results"
    )
    print("Accuracy:", acc)

    plot_label_distribution(
        true_dir=examples_dir,
        pred_dir=examples_dir+"/results"
    )
