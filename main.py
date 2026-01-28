# main.py
from simulation import run_simulation
from metrics import Metrics
import plots
import sys

# Ensure UTF-8 encoding for emojis
sys.stdout.reconfigure(encoding='utf-8')

# === Step 1: Run the simulation ===
print("🚀 Running Smart Home Fire Simulation...")
run_simulation()
print("✅ Simulation complete!")

# === Step 2: Collect preliminary metrics ===
metrics = Metrics()
metrics.update()
metrics.report()

# === Step 3: Generate plots ===
print("📊 Generating plots...")
plots.generate_plot(show=False)  # We will slightly modify plots.py to have a generate_plot() function
print("✅ Plots generated!")