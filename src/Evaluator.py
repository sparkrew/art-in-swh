import os
import json
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
)


class Evaluator:
    
    def __init__(self, true_dir, pred_dir, report_path, config_mode='examples', penalize_missing_preds=False):
        self.true_dir = true_dir
        self.pred_dir = pred_dir
        self.report_path = report_path
        self.config_mode = config_mode
        self.penalize_missing_preds = penalize_missing_preds
    
        self.true_files = [
            f for f in os.listdir(true_dir)
            if f.endswith(".json") and os.path.isfile(os.path.join(true_dir, f))
        ]
        os.makedirs(pred_dir, exist_ok=True)


    def _to_label_set(self, value):
        """Normalize labels to a set of strings."""
        if value is None:
            return set()
        if isinstance(value, list):
            return set(value)
        if isinstance(value, str):
            # assume a single label
            return {value}
        raise TypeError(f"Unexpected label type: {type(value)} -> {value}")


    def _compute_label_metrics(self):
        keys = ["entities", "interaction", "outcome"]
        metrics = {}

        for k in keys:
            y_true_labels = []
            y_pred_labels = []

            for fname in self.true_files:
                true_path = os.path.join(self.true_dir, fname)
                pred_path = os.path.join(self.pred_dir, fname)

                with open(true_path, "r") as f:
                    true_labels = json.load(f)

                true_set = self._to_label_set(true_labels.get(k))

                if os.path.exists(pred_path):
                    with open(pred_path, "r") as f:
                        pred_labels = json.load(f)
                    pred_set = self._to_label_set(pred_labels.get(k))
                else:
                    if self.penalize_missing_preds:
                        pred_set = set()
                    else:
                        continue

                y_true_labels.append(true_set)
                y_pred_labels.append(pred_set)
                
                print()
                print(fname)
                print("True set:", true_set)
                print("Pred set:", pred_set)
                print("\n")

            # No data for this key?
            if not y_true_labels:
                metrics[k] = {
                    "subset_accuracy": 0.0,
                    "precision_micro": 0.0,
                    "recall_micro": 0.0,
                    "f1_micro": 0.0,
                }
                continue

            # Binarize labels (multi-label)
            mlb = MultiLabelBinarizer()
            mlb.fit(y_true_labels + y_pred_labels)

            Y_true = mlb.transform(y_true_labels)
            Y_pred = mlb.transform(y_pred_labels)

            # Subset accuracy = exact set match per sample
            subset_acc = accuracy_score(Y_true, Y_pred)

            # Micro-averaged precision/recall/F1 over all tags
            precision, recall, f1, _ = precision_recall_fscore_support(
                Y_true,
                Y_pred,
                average="micro",
                zero_division=0
            )
        
            metrics[k] = {
                "subset_accuracy": subset_acc,
                "precision_micro": precision,
                "recall_micro": recall,
                "f1_micro": f1,
            }

        return metrics


    def _compute_and_save_label_metrics_sklearn(self):
        """
        Wrapper around compute_label_metrics that saves results to a text file.
        """
        metrics = self._compute_label_metrics()

        with open(self.report_path, "w") as f:
            for key, m in metrics.items():
                f.write(f"[{key}]\n")
                for metric_name, value in m.items():
                    f.write(f"{metric_name}: {value:.6f}\n")
                f.write("\n")

        self.metrics = metrics
        return metrics


    def _plot_label_distribution(self, label_dist_report_path):
        """
        Computes label frequencies (true vs predicted), plots them,
        and saves the figure to label_dist_report_path.
        """

        true_counts = Counter()
        pred_counts = Counter()

        for fname in self.true_files:
            true_path = os.path.join(self.true_dir, fname)
            pred_path = os.path.join(self.pred_dir, fname)

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
        
        # Export img
        plt.savefig(label_dist_report_path, dpi=150)    
    
    
    def export_reports(self, label_dist_report_path=None):
        if self.config_mode == 'examples':
            self._compute_and_save_label_metrics_sklearn()
            if label_dist_report_path:
                self._plot_label_distribution(label_dist_report_path)
        
        elif self.config_mode == 'artworks':
            # what do we wanna evaluate when predicting labels for the artworks?
            raise NotImplementedError
            