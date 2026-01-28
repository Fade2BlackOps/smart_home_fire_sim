import subprocess
import webbrowser
import time
import sys
import os

# Configuration
DASHBOARD_URL = "http://127.0.0.1:5000"

def run_system():
    print("🚀  Initializing Smart Home System...")

    # 1. Start Flask Dashboard in the background
    # We use sys.executable to ensure we use the same Python interpreter (venv)
    print("🖥️   Starting Flask Server...")
    flask_process = subprocess.Popen([sys.executable, "flask_app.py"])

    # Give Flask a moment to start up
    time.sleep(2)

    # 2. Open the Web Browser automatically
    print(f"🌐  Opening Dashboard at {DASHBOARD_URL}")
    webbrowser.open(DASHBOARD_URL)
    time.sleep(3)  # Small delay to ensure browser opens before simulation starts

    # 3. Run the Main Simulation
    print("🔥  Running Simulation (Check dashboard for live updates!)...")
    try:
        # This will block here until main.py finishes running
        subprocess.run([sys.executable, "main.py"], check=True)

        # 3.1. Export metrics after simulation completes
        print("📊  Exporting Simulation Metrics...")
        subprocess.run([sys.executable, "export_metrics_csv.py"], check=True)

    except KeyboardInterrupt:
        print("\n🛑  Stopping simulation...")

    # 4. Cleanup when simulation finishes
    print("✅  Simulation Complete. Keeping dashboard open.")
    print("    Press CTRL+C to close the dashboard and exit.")
    
    try:
        # Keep script alive so Flask keeps running
        flask_process.wait()
    except KeyboardInterrupt:
        print("\n👋  Shutting down Dashboard...")
        flask_process.terminate()

if __name__ == "__main__":
    run_system()