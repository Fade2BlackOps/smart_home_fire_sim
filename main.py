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
launch_dashboard = input("Do you want to launch the HCI dashboard? (y/n): ").lower()
if launch_dashboard == 'y':
    from user_interface import Dashboard
    print("🖥️ Launching HCI Dashboard...")
    Dashboard()
    # threading.Thread(target=Dashboard, daemon=True).start()     # this runs the Tkinter mainloop
    print("✅ Dashboard closed.")
    # Dashboard runs in its own window and reads ledger.json in real-time