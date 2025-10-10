import json
import matplotlib.pyplot as plt
from config import FIRE_START

# Optional: Fahrenheit conversion helper
def to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

# Read the blockchain ledger
with open("data/ledger.json", "r") as f:
    blocks = [json.loads(line) for line in f]

# Extract time steps and temperature data
times = [b["data"]["time"] for b in blocks]
temps = list(zip(*[b["data"]["temps"] for b in blocks]))

# Plot each sensor's temperature curve
plt.figure(figsize=(10, 6))
for i, sensor_temps in enumerate(temps):
    # Convert to Fahrenheit if not already
    sensor_temps_f = [to_fahrenheit(t) for t in sensor_temps]
    plt.plot(times, sensor_temps_f, label=f"Sensor {i}")

# Mark the fire start time
plt.axvline(x=FIRE_START, color="r", linestyle="--", label="🔥 Fire start")

# Labels and formatting
plt.title("Smart Home Sensor Temperature Trends")
plt.xlabel("Time Step")
plt.ylabel("Temperature (°F)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
plt.savefig("data/temperature_trends.png")  # Save the plot if needed
plt.close()
