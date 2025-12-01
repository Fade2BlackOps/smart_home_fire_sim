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

# === Step 4 (Optional): Launch HCI dashboard ===
launch_dashboard = input("Do you want to launch the Flask HCI dashboard? (y/n): ").strip().lower()
if launch_dashboard == 'y':
    # run the flask server in a background thread so the terminal stays interactive
    from flask_app import run_server
    import threading
    print("🖥️  Launching Flask HCI Dashboard at http://127.0.0.1:5000 ...")
    t = threading.Thread(target=lambda: run_server(host="127.0.0.1", port=5000, background_thread=True), daemon=True)
    t.start()
    print("Dashboard launched in background thread. Press Enter to exit.")
    input()