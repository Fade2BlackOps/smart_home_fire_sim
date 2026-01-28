# flask_app.py
import json
import os
from flask import Flask, render_template, send_from_directory, jsonify

app = Flask(__name__, static_folder="static", template_folder="templates")

# Path to ledger
LEDGER_FILE = os.path.join(os.path.dirname(__file__), "data", "ledger.json")

def read_ledger():
    if not os.path.exists(LEDGER_FILE):
        return []
    blocks = []
    try:
        with open(LEDGER_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        blocks.append(json.loads(line))
                    except:
                        continue
    except Exception:
        return []
    return blocks

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/updates")
def get_updates():
    """The browser will request this URL every second."""
    blocks = read_ledger()
    if not blocks:
        return jsonify({"blocks": [], "latest": None})
    
    # Send last 20 blocks
    recent = blocks[-20:]
    latest = recent[-1]
    
    # Safety: Ensure structure exists to prevent JS crashes
    safe_latest = {
        "time": latest.get("data", {}).get("time", "--"),
        "decision": latest.get("data", {}).get("decision", "--"),
        "votes": latest.get("data", {}).get("votes", []),
    }

    return jsonify({"blocks": recent, "latest": safe_latest})

# Serve static files
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, "static"), filename)

if __name__ == "__main__":
    # Standard Flask run - no special async_mode needed!
    app.run(host="127.0.0.1", port=5000, debug=True)