import json
import yaml
from Model import LLM_Model
from Prompts import *
from collections import Counter
import matplotlib.pyplot as plt

def get_prompt_template(prompt_version):
    return globals()[prompt_version].template

def count_labels(examples, classification_key):
    counter = Counter()

    for ex in examples:
        classification = ex.get(classification_key, {})

        for dimension, labels in classification.items():
            for label in labels:
                counter[f"{dimension}_{label}"] += 1

    return dict(counter)


def count_all_labels(examples):
    return {
        "classification": count_labels(examples, "classification"),
        "predicted_classification": count_labels(examples, "predicted_classification"),
    }

def count_labels(examples, classification_key):
    counter = Counter()

    for ex in examples:
        classification = ex.get(classification_key, {})
        for dimension, labels in classification.items():
            for label in labels:
                counter[f"{dimension}_{label}"] += 1

    return counter


def plot_all_distributions(examples):
    true_counts = count_labels(examples, "classification")
    pred_counts = count_labels(examples, "predicted_classification")

    all_labels = sorted(set(true_counts) | set(pred_counts))
    x = range(len(all_labels))
    width = 0.4

    plt.figure(figsize=(12, 5))
    plt.bar([i - width/2 for i in x], [true_counts.get(label, 0) for label in all_labels], width=width, label="classification")
    plt.bar([i + width/2 for i in x], [pred_counts.get(label, 0) for label in all_labels], width=width, label="predicted_classification")

    plt.xticks(x, all_labels, rotation=45, ha="right")
    plt.ylabel("Count")
    plt.title("Classification vs Predicted Classification")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_distributions_by_dimension(examples):
    true_counts = count_labels(examples, "classification")
    pred_counts = count_labels(examples, "predicted_classification")

    for dimension in ["entities", "interaction", "outcome"]:
        labels = sorted([
            key.split("_", 1)[1]
            for key in set(true_counts) | set(pred_counts)
            if key.startswith(f"{dimension}_")
        ])

        x = range(len(labels))
        width = 0.4

        plt.figure(figsize=(8, 4)) 
        plt.bar([i - width/2 for i in x], [true_counts.get(f"{dimension}_{label}", 0) for label in labels], width=width, label="classification")
        plt.bar([i + width/2 for i in x], [pred_counts.get(f"{dimension}_{label}", 0) for label in labels], width=width, label="predicted_classification")

        plt.xticks(x, labels, rotation=45, ha="right")
        plt.ylabel("Count")
        plt.title(f"{dimension}: classification vs predicted")
        plt.legend()
        plt.tight_layout()
        plt.show()