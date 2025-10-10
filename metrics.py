import json

class Metrics:
    def __init__(self):
        self.latency = None          # time steps until quorum reached
        self.false_positives = 0
        self.false_negatives = 0
        self.total_alerts = 0
        self.quorum_time = None

    def update(self, ledger_file="data/ledger.json", alert_threshold=140.0):
        # Reset counters each run to avoid accumulation
        self.false_positives = 0
        self.false_negatives = 0
        self.total_alerts = 0
        self.quorum_time = None

        with open(ledger_file, "r") as f:
            blocks = [json.loads(line) for line in f]

        # Skip genesis block (index 0) which may contain a different data schema
        data_blocks = blocks[1:]

        # Find first quorum decision (first block that contains a "FIRE DETECTED" decision)
        for b in data_blocks:
            data = b.get("data", {})
            decision = data.get("decision", "")
            if "FIRE DETECTED" in decision:
                self.quorum_time = data.get("time")
                break

        # Compute false positives / negatives and total alerts
        for b in data_blocks:
            data = b.get("data", {})
            temps = data.get("temps", [])
            step = data.get("time")
            decision = data.get("decision", "")

            actual_fire = any((t is not None and t >= alert_threshold) for t in temps)
            detected_fire = "FIRE DETECTED" in decision

            if detected_fire and not actual_fire:
                self.false_positives += 1
            if actual_fire and not detected_fire:
                self.false_negatives += 1
            if detected_fire:
                self.total_alerts += 1

        # Latency: steps from first actual fire reading to quorum_time
        fire_steps = [data.get("time") for data in (b.get("data", {}) for b in data_blocks) if any((t is not None and t >= alert_threshold) for t in data.get("temps", []))]
        if fire_steps and self.quorum_time is not None:
            # Use the first timestep where an actual fire reading occurred
            self.latency = self.quorum_time - fire_steps[0]

    def report(self):
        print("=== Simulation Metrics ===")
        print(f"Detection latency (timesteps): {self.latency}")
        print(f"Total alerts recorded: {self.total_alerts}")
        print(f"False positives: {self.false_positives}")
        print(f"False negatives: {self.false_negatives}")
        print(f"Quorum reached at timestep: {self.quorum_time}")
        print("==========================")
        return {
            "latency": self.latency,
            "false_positives": self.false_positives,
            "false_negatives": self.false_negatives,
            "total_alerts": self.total_alerts,
            "quorum_time": self.quorum_time
        }