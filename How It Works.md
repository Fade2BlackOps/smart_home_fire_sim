# How This Simulation Works
| File               | Role                               | Real-world analogy                     |
| ------------------ | ---------------------------------- | -------------------------------------- |
| `config.py`        | Simulation settings                | System parameters / config panel       |
| `digital_twin.py`  | Predicts expected temperature      | Cloud-based “digital twin” model       |
| `sensor.py`        | Simulates IoT device behavior      | Physical smoke/heat sensors            |
| `blockchain.py`    | Records decisions immutably        | Permissioned ledger (Hyperledger-like) |
| `simulation.py`    | Controls time loop, collects votes | IoT network runtime                    |
| `main.py`          | Entry point                        | ADT hub / master controller            |
| `data/ledger.json` | Output ledger                      | Blockchain storage                     |


## How it works (summary)

- `simulation.py` runs and appends newline-delimited JSON blocks to `data/ledger.json`.
- `flask_app.py` starts Flask + Socket.IO. A background task reads ledger every second and emits `ledger_update` events.
- `templates/index.html` + `static/main.js` connect to Socket.IO and update the Chart.js chart and ledger table in real-time.
- **Launch options:**
    - Standalone server: python3 flask_app.py (or python3 -m flask_app).
    - From main: run python3 main.py, then answer y at prompt to start UI in background.

## How to run (step-by-step)

1. Activate venv:
```
source venv/bin/activate
```

2. Install new dependencies:
```
pip install -r requirements.txt
```

3. Run simulation + UI from main.py:
```
python3 main.py
# when prompted: Do you want to launch the Flask HCI dashboard? (y/n): y
# then open browser to http://<pi-ip>:5000
```

Or run server separately:
```
# in another terminal (venv active)
python3 flask_app.py
# open http://<pi-ip>:5000
```

## Caveats & tips
- Permissions / firewall: On Pi, make sure port 5000 is reachable from your development machine. For access from other machines, use http://<raspberrypi-ip>:5000.
- Sensor count: The JS tries to detect sensor count from blocks. If your temps arrays change size across blocks, the chart will rebuild accordingly.
- Performance: The emitter reads the whole ledger each second — fine for small logs. If ledger grows huge, you may want to only tail the file (read end) or emit diffs.
- Eventlet: Flask-SocketIO + eventlet works reliably on Pi; if you have problems, try pip install gevent and switch async_mode. Eventlet is simplest.
- Security: This is a prototype. Do not expose the server publicly without authentication.