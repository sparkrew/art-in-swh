import os
import json
import yaml
from openai import OpenAI
from collections import Counter
import matplotlib.pyplot as plt
from qwen3_prompts import *

def query_vllm(
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


def get_file_prediction(prompt_template, file_name, src_content, model_config):
    """
    Given a txt string of a file, generate its labels.
    """
    user_prompt = f"{prompt_template}\n ```\n{src_content}\n```"
    model_output = query_vllm(
        user_prompt=user_prompt,
        model=model_config["model_name"],
        system_prompt=model_config["system_prompt"],
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"]
    )
    try:
        result = json.loads(model_output)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON for {file_name}: {model_output}")
        result = {"error": "invalid_json", "raw_output": model_output}
    return result


def export_json(filepath, content):
    with open(filepath, 'w') as f:
        json.dump(content, f)
        

def process_files(prompt_template, src_dir, output_dir, model_config, batch_processing=False):
    """
    Process all source files in examples directory

    args:
        src_dir (str): file path with the src files
        output_dir (str): file path where predictions will be saved
        model_config (dict): model configuration from config file
        batch_processing (bool): will control if exports 1 json per file or multiple jsons. NotImplementedYet.
    """
    src_files = list_src_files(src_dir)
    os.makedirs(output_dir, exist_ok=True)

    for file_name in src_files:
        
        file_path = os.path.join(src_dir, file_name)
        src_content = read_file_content(file_path)
        predicted_labels = get_file_prediction(prompt_template, file_path, src_content, model_config)

        # Export one json per src file
        file_name = "".join(file_name.split(".")[:-1]) + ".json"
        output_file_path = os.path.join(output_dir, file_name)  
        export_json(output_file_path, predicted_labels)

        # break


def compute_label_accuracy(true_dir, pred_dir):

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

        for k in keys:
            total[k] += 1
            if set(true_labels.get(k, [])) == set(pred_labels.get(k, [])):
                correct[k] += 1

    acc = {}
    for k in keys:
        acc[k] = (correct[k] / total[k]) if total[k] else 0.0

    return acc


def compute_and_save_label_accuracy(
    true_dir, pred_dir, acc_report_path):

    os.makedirs(pred_dir, exist_ok=True)
    acc = compute_label_accuracy(true_dir=true_dir, pred_dir=pred_dir)

    with open(acc_report_path, "w") as f:
        for key, value in acc.items():
            f.write(f"{key}: {value:.6f}\n")

    return acc


def plot_label_distribution(true_dir, pred_dir, label_dist_report_path):
    """
    Computes label frequencies (true vs predicted), plots them,
    and saves the figure to label_dist_report_path.
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

    plt.savefig(label_dist_report_path, dpi=150)
    plt.close()
    

if __name__ == "__main__":
    # =======================
    # Configs
    # =======================
    model = "qwen"
    config_mode = "examples"
    prompt_template = PROMPT_2
    
    with open("config.yml", "r") as f:
        configs = yaml.safe_load(f)
    
    # Global vars
    CLIENT = OpenAI(
        base_url=configs[model]["base_url"],
        api_key="" # no api key because we're running our own model :)
    )    
    # =======================
    
    print("Processing files...")
    process_files(
        prompt_template=prompt_template,
        src_dir=configs[config_mode]["src_path"],
        output_dir=configs[config_mode]["predicted_labels_path"],
        model_config=configs[model]
    )
    
    acc = compute_and_save_label_accuracy(
        true_dir=configs[config_mode]["true_labels_path"],
        pred_dir=configs[config_mode]["predicted_labels_path"],
        acc_report_path=os.path.join(configs[config_mode]["report_folder_path"], "accuracy_report.txt"),
    )
    print("Accuracy:", acc)

    plot_label_distribution(
        true_dir=configs[config_mode]["true_labels_path"],
        pred_dir=configs[config_mode]["predicted_labels_path"],
        label_dist_report_path=os.path.join(configs[config_mode]["report_folder_path"], "label_distribution.png"),
    )
