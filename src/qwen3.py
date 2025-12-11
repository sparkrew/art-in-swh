import os
import json
import yaml
from Model import LLM_Model
from Evaluator import Evaluator
from Prompts import *

def get_prompt_template(prompt_version):
    return globals()[prompt_version].template


def list_src_files(dir):
    """
    Given a dir, it returns the list of source files to analyse
    """
    files = os.listdir(dir)
    files = [f for f in files if f.endswith(('.js', '.html')) and os.path.isfile(os.path.join(dir, f))]
    return files


def process_files(prompt_template, src_dir, output_dir, model):
    """
    Process all source files in examples directory
    
    now we're processing in sequence.
        can we process them in parallel?
    """
    src_files = list_src_files(src_dir)

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

        # Export one json per src file
        file_name = "".join(file_name.split(".")[:-1]) + ".json"
        output_file_path = os.path.join(output_dir, file_name)
        
        # Export file
        with open(output_file_path, 'w') as f:
            json.dump(predicted_labels, f)  
        # break


if __name__ == "__main__":
    # =======================
    # Configs
    # =======================
    print("Configs...")
    with open("config.yml", "r") as f:
        configs = yaml.safe_load(f)

    config_mode = configs["chosen_config"]['config_mode']
    model = configs["chosen_config"]["model"]
    prompt_version = configs["chosen_config"]["prompt_version"]
    
    # Get the prompt template object
    prompt_template = get_prompt_template(prompt_version)
    
    # Imports
    true_dir = configs[config_mode]["true_labels_path"]
    pred_dir = configs[config_mode]["predicted_labels_path"]
    src_dir=configs[config_mode]["src_path"]
    # Exports
    report_path = os.path.join(configs[config_mode]["report_folder_path"], "accuracy_report.txt")
    label_dist_report_path = os.path.join(configs[config_mode]["report_folder_path"], "label_distribution.png")
    
    # Global vars
    llm_model = LLM_Model(
        model_name=configs[model]['config_mode'],
        base_url=configs[model]['base_url'],
        system_prompt=configs[model]['system_prompt']
    )
    
    evaluator = Evaluator(
        true_dir=true_dir,
        pred_dir=pred_dir, 
        report_path=report_path,
        config_mode=config_mode
    )
    # =======================
    
    # Predict!
    print("Processing files...")
    process_files(
        prompt_template=prompt_template,
        src_dir=configs[config_mode]["src_path"],
        output_dir=configs[config_mode]["predicted_labels_path"],
        model=llm_model
    )
    
    # Export
    print("Evaluating predictions...")
    evaluator.export_reports(label_dist_report_path=label_dist_report_path)
    print("Final Metrics:", evaluator.metrics)
