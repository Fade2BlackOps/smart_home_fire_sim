# main.py
import time
import time
from simulation import run_simulation
from metrics import Metrics
import plots
import threading
from metrics import Metrics
import plots
import threading
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
plots.generate_plot()  # We will slightly modify plots.py to have a generate_plot() function
print("✅ Plots generated!")

# === Step 4: Launch HCI dashboard ===
# We run this directly on the main thread to avoid Socket.IO protocol errors
launch_dashboard = input("Do you want to launch the Flask HCI dashboard? (y/n): ").strip().lower()
if launch_dashboard == 'y':
    from flask_app import run_server
    print("🖥️  Launching Flask HCI Dashboard at http://0.0.0.0:5000 ...")
    print("   (Press CTRL+C to quit)")
    
    # Run directly (blocking), NOT in a thread
    run_server(host="0.0.0.0", port=5000, background_thread=True)