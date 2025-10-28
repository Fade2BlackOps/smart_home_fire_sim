import json
import os
import matplotlib.pyplot as plt
from config import FIRE_START


# Optional: Fahrenheit conversion helper
def to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def generate_plot(ledger_file="data/ledger.json"):
    """
    Generate and save a plot of sensor temperature trends over time.
    Reads from the blockchain ledger file (ledger.json).
    """

    # Defensive: check if ledger file exists
    if not os.path.exists(ledger_file):
        raise FileNotFoundError(f"Ledger file {ledger_file} not found. Run the simulation first.")
    
    # Read the blockchain ledger
    with open(ledger_file, "r") as f:
        blocks = [json.loads(line) for line in f]

    # Defensive: if there are no blocks (or only genesis), produce a warning and exit
    if len(blocks) <= 1:
        raise RuntimeError("Not enough blocks in data/ledger.json to plot temperatures")

    # Extract time steps and temperature data
    times = [b["data"]["time"] for b in blocks[1:]]  # Skip genesis block
    temps = list(zip(*[b["data"]["temps"] for b in blocks[1:]]))
    votes = [b["data"]["votes"] for b in blocks[1:]]
    decisions = [b["data"]["decision"] for b in blocks[1:]]

    # Determine quorum decision time (first "FIRE DETECTED!")
    quorum_time = None
    for t, d in zip(times, decisions):
        if "FIRE DETECTED" in d:
            quorum_time = t
            break

    # Create figure and plot sensor temperatures (in °C)
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, sensor_temps in enumerate(temps):
        ax.plot(times, sensor_temps, label=f"Sensor {i}")

    # Plot vertical lines
    ax.axvline(x=FIRE_START, color="r", linestyle="--", label="Fire start")
    if quorum_time is not None:
        ax.axvline(x=quorum_time, color="g", linestyle="--", label="Quorum Reached")

    # Optional: annotate quorum
    if quorum_time is not None:
        plt.text(quorum_time + 0.5, max(max(s) for s in temps),
                 "Quorum Reached", color="green")

    # Labels and formatting
    ax.set_title("Smart Home Sensor Temperature Trends")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True)

    # Ensure output directory exists
    out_dir = os.path.join("data")
    os.makedirs(out_dir, exist_ok=True)

    # Save before show (for paper figures)
    out_path = os.path.join(out_dir, "temperature_trends.png")
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight", dpi=150)

    # Optionally display
    plt.show()
    plt.close(fig)
