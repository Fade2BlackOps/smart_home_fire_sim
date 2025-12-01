# flask_app.py
import json
import time
import threading
import os
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit

LED_COLOR = {True: "red", False: "green"}

app = Flask(__name__, static_folder="static", template_folder="templates")

# Switch to 'threading' for Windows stability
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

LED_COLOR = {True: "red", False: "green"}

# path to ledger (same as simulation)
LEDGER_FILE = os.path.join(os.path.dirname(__file__), "data", "ledger.json")

def read_ledger():
    """Return parsed blocks list (safe) or empty list if not present."""
    if not os.path.exists(LEDGER_FILE):
        return []
    blocks = []
    try:
        with open(LEDGER_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    blocks.append(json.loads(line))
                except Exception:
                    # skip malformed lines
                    continue
    except Exception:
        return []
    return blocks

# flask_app.py

def ledger_summary():
    """Return compact summary for client UI (last block + vote counts + times)."""
    blocks = read_ledger()
    if not blocks:
        return {"blocks": [], "latest": None}
    
    # --- Filter out the Genesis block ---
    # We only want blocks that actually have temperature data.
    valid_blocks = [b for b in blocks if b.get("data", {}).get("temps")]
    
    if not valid_blocks:
        return {"blocks": [], "latest": None}

    # send last N blocks (e.g. last 20)
    N = 20
    recent = valid_blocks[-N:]
    latest = recent[-1]
    compact = []
    for b in recent:
        compact.append({
            "index": b.get("index"),
            "time": b.get("data", {}).get("time"),
            "temps": b.get("data", {}).get("temps"),
            "votes": b.get("data", {}).get("votes"),
            "decision": b.get("data", {}).get("decision"),
            "timestamp": b.get("timestamp"),
        })
    return {"blocks": compact, "latest": compact[-1]}

def background_emit(interval=1.0):
    """Background thread that reads ledger and emits updates via socketio."""
    last_index = None
    while True:
        try:
            summary = ledger_summary()
            latest = summary.get("latest")
            if latest:
                idx = latest.get("index")
                # emit even if same (UI will decide)
                socketio.emit("ledger_update", summary, namespace="/dashboard")
                last_index = idx
            else:
                socketio.emit("ledger_update", summary, namespace="/dashboard")
        except Exception as e:
            # keep emitting minimal info on error
            socketio.emit("ledger_error", {"error": str(e)}, namespace="/dashboard")
        socketio.sleep(interval)

@app.route("/")
def index():
    return render_template("index.html")

# serve static (if needed)
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, "static"), filename)

def run_server(host="0.0.0.0", port=5000, background_thread=True):
    """Start the Flask-SocketIO server. Call this from main.py or run directly."""
    if background_thread:
        # start background emitter
        socketio.start_background_task(target=background_emit, interval=1.0)
    socketio.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server()
