# digital_twin.py
import statistics
from config import TWIN_HISTORY_SIZE, BASE_TEMP

class DigitalTwin:
    def __init__(self):
        self.history = [BASE_TEMP]
        self.expected = BASE_TEMP

    def update(self, new_temp: float):
        """Update the twin's expected value based on recent readings."""
        self.history.append(new_temp)
        if len(self.history) > TWIN_HISTORY_SIZE:
            self.history.pop(0)
        self.expected = statistics.mean(self.history)

    def deviation(self, current_temp: float) -> float:
        """Return difference between real reading and twin's prediction."""
        return current_temp - self.expected
