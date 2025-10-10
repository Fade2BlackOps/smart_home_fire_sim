import json
import os
import matplotlib.pyplot as plt
from config import FIRE_START


# Optional: Fahrenheit conversion helper
def to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


# Read the blockchain ledger
with open("data/ledger.json", "r") as f:
    blocks = [json.loads(line) for line in f]


# Defensive: if there are no blocks (or only genesis), produce a warning and exit
if len(blocks) <= 1:
    raise RuntimeError("Not enough blocks in data/ledger.json to plot temperatures")


# Extract time steps and temperature data
times = [b["data"]["time"] for b in blocks[1:]]  # Skip genesis block
temps = list(zip(*[b["data"]["temps"] for b in blocks[1:]]))


# Create figure and plot
fig, ax = plt.subplots(figsize=(10, 6))
for i, sensor_temps in enumerate(temps):
    sensor_temps_f = [to_fahrenheit(t) for t in sensor_temps]
    ax.plot(times, sensor_temps_f, label=f"Sensor {i}")

# Mark the fire start time
ax.axvline(x=FIRE_START, color="r", linestyle="--", label="Fire start")

# Labels and formatting
ax.set_title("Smart Home Sensor Temperature Trends")
ax.set_xlabel("Time Step")
ax.set_ylabel("Temperature (°F)")
ax.legend()
ax.grid(True)

# Ensure output directory exists
out_dir = os.path.join("data")
os.makedirs(out_dir, exist_ok=True)

# Save before show. Use tight bounding box and higher dpi to avoid empty/white images
out_path = os.path.join(out_dir, "temperature_trends.png")
fig.tight_layout()
fig.savefig(out_path, bbox_inches="tight", dpi=150)

# Optionally display the figure in interactive environments
plt.show()
plt.close(fig)
