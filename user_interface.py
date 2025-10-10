import tkinter as tk
import json
import threading
import time

LED_COLOR = {
    True: "red",
    False: "green"
}

class Dashboard:
    def __init__(self, ledger_file="data/ledger.json"):
        self.ledger_file = ledger_file
        self.root = tk.Tk()
        self.root.title("Smart Home Safety Dashboard")
        self.root.geometry("600x400")

        # Labels
        self.time_label = tk.Label(self.root, text="Time Step: --", font=("Helvetica", 14))
        self.time_label.pack(pady=5)

        self.sensor_frame = tk.Frame(self.root)
        self.sensor_frame.pack(pady=10)
        self.sensor_labels = []

        self.alert_label = tk.Label(self.root, text="ALERT STATUS: SAFE", font=("Helvetica", 16), fg="green")
        self.alert_label.pack(pady=10)

        # Blockchain info
        self.block_label = tk.Label(self.root, text="Blocks Recorded: 0", font=("Helvetica", 12))
        self.block_label.pack(pady=5)

        self.running = True
        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.mainloop()

    def on_close(self):
        self.running = False
        self.root.destroy()

    def update_loop(self):
        last_block_count = 0
        while self.running:
            try:
                with open(self.ledger_file, "r") as f:
                    blocks = [json.loads(line) for line in f]
                if not blocks:
                    time.sleep(1)
                    continue

                latest = blocks[-1]
                time_step = latest["data"]["time"]
                temps = latest["data"]["temps"]
                votes = latest["data"]["votes"]
                decision = latest["data"]["decision"]
                block_count = len(blocks)

                # Update sensor labels
                if len(self.sensor_labels) != len(temps):
                    for lbl in self.sensor_labels:
                        lbl.destroy()
                    self.sensor_labels.clear()
                    for i, (t, v) in enumerate(zip(temps, votes)):
                        lbl = tk.Label(self.sensor_frame, text=f"Sensor {i}: {t:.1f}°F | Vote: {v}", font=("Helvetica", 12))
                        lbl.pack()
                        self.sensor_labels.append(lbl)
                else:
                    for i, (t, v) in enumerate(zip(temps, votes)):
                        self.sensor_labels[i].config(text=f"Sensor {i}: {t:.1f}°F | Vote: {v}")

                self.time_label.config(text=f"Time Step: {time_step}")
                self.alert_label.config(text=f"ALERT STATUS: {decision}", fg="red" if "FIRE" in decision else "green")
                self.block_label.config(text=f"Blocks Recorded: {block_count}")

                time.sleep(1)
            except Exception as e:
                print("Dashboard update error:", e)
                time.sleep(1)
