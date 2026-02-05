import os
import json
import yaml
import argparse
from datetime import datetime
from Model import LLM_Model
from Evaluator import Evaluator
from Prompts import *

def get_prompt_template(prompt_version):
    return globals()[prompt_version].template


def list_src_files(src_dir, limit=10):
    """
    Return up to `limit` files found recursively under src_dir.
    Returns relative paths (so os.path.join(src_dir, relpath) works).
    Stops early for speed.
    """
    out = []
    for root, _, files in os.walk(src_dir):
        for f in files:
            full_path = os.path.join(root, f)
            if os.path.isfile(full_path):
                out.append(os.path.relpath(full_path, src_dir))
                if len(out) >= limit:
                    return out
    return out

    
def process_files(prompt_template, src_dir, output_dir, model, timestamp, start=None, end=None):
    """
    Process all source files in examples directory
    
    now we're processing in sequence.
        can we process them in parallel?
    """
    src_files = list_src_files(src_dir)
    print("src_dir:", src_dir)
    
    # Slice the file list if start/end are provided
    if start is not None or end is not None:
        src_files = src_files[start:end]
        print(f"Processing files {start} to {end}: {len(src_files)} files")
    else:
        src_files = src_files[:10]
        print(f"Processing first 10 files: {len(src_files)} files")
    
    # Accumulate all predictions in a dictionary
    all_predictions = {}

    for file_name in src_files:
        file_path = os.path.join(src_dir, file_name)
        
        # Read file
        with open(file_path, 'r') as f:
            art_src_code = f.read()
            
        # Get labels
        predicted_labels = model.get_labels(
            prompt_template=prompt_template, 
            art_src_code=art_src_code, 
            system_prompt=model.system_prompt
            )
        print(file_name, "\n\n")
        print(predicted_labels)

        # Store predictions with filename as key
        all_predictions[file_name] = predicted_labels
    
    # Export all predictions to a single batch JSON file with timestamp
    os.makedirs(output_dir, exist_ok=True)
    batch_output_path = os.path.join(output_dir, f"batch_predictions_{timestamp}.json")
    with open(batch_output_path, 'w') as f:
        json.dump(all_predictions, f, indent=2)
    
    return all_predictions


if __name__ == "__main__":
    # =======================
    # Parse arguments
    # =======================
    parser = argparse.ArgumentParser(description="Process art source files with LLM")
    parser.add_argument("--start", type=int, default=None, help="Start index for file slicing")
    parser.add_argument("--end", type=int, default=None, help="End index for file slicing")
    args = parser.parse_args()
    
    # =======================
    # Configs
    # =======================
    print("Configs...")
    with open("config.yml", "r") as f:
        configs = yaml.safe_load(f)

    config_mode = configs["chosen_config"]['config_mode']
    model = configs["chosen_config"]["model"]
    prompt_version = configs["chosen_config"]["prompt_version"]
    
    # Generate timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Get the prompt template object
    prompt_template = get_prompt_template(prompt_version)
    
    # Imports
    true_dir = configs[config_mode].get("true_labels_path", None) if config_mode == 'examples' else None
    pred_dir = configs[config_mode]["predicted_labels_path"]
    src_dir = configs[config_mode]["src_path"]
    
    # Exports with timestamp
    report_path = os.path.join(configs[config_mode]["report_folder_path"], f"accuracy_report_{timestamp}.txt")
    label_dist_report_path = os.path.join(configs[config_mode]["report_folder_path"], f"label_distribution_{timestamp}.png")
    batch_predictions_filename = f"batch_predictions_{timestamp}.json"
    
    # Global vars
    llm_model = LLM_Model(
        model_name=configs[model]['model_name'],
        base_url=configs[model]['base_url'],
        system_prompt=configs[model]['system_prompt']
    )
    
    evaluator = Evaluator(
        true_dir=true_dir,
        pred_dir=pred_dir, 
        report_path=report_path,
        config_mode=config_mode,
        batch_predictions_filename=batch_predictions_filename
    )
    
    # =======================
    
    # Predict!
    print("Processing files...")
    all_predictions = process_files(
        prompt_template=prompt_template,
        src_dir=configs[config_mode]["src_path"],
        output_dir=configs[config_mode]["predicted_labels_path"],
        model=llm_model,
        timestamp=timestamp,
        start=args.start,
        end=args.end
    )
    
    # Export
    print("Evaluating predictions...")
    evaluator.export_reports(label_dist_report_path=label_dist_report_path, num_files=len(all_predictions))
    if evaluator.metrics:
        print("Final Metrics:", evaluator.metrics)