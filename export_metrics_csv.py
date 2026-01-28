import csv
import os
from datetime import datetime
from metrics import Metrics
import config

RESULTS_PATH = "data/results.csv"

def append_metrics_to_csv(metrics_dict, path=RESULTS_PATH):
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    file_exists = os.path.exists(path)

    with open(path, mode="a", newline="") as f:
        writer = csv.writer(f)

        # Write header once if file is new
        if not file_exists:
            writer.writerow([
                "timestamp",
                "latency",
                "quorum_time",
                "total_alerts",
                "false_positives",
                "false_negatives"
            ])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            metrics_dict["latency"],
            metrics_dict["quorum_time"],
            metrics_dict["total_alerts"],
            metrics_dict["false_positives"],
            metrics_dict["false_negatives"]
        ])

if __name__ == "__main__":
    metrics = Metrics()
    metrics.update(
        ledger_file="data/ledger.json",
        alert_threshold=config.ALERT_THRESHOLD
    )
    results = metrics.report()
    append_metrics_to_csv(results)
    print(f"Metrics appended to {RESULTS_PATH}")
