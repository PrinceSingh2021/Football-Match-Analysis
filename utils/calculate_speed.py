import time
import numpy as np
from collections import defaultdict

class SpeedCalculator:
    """
    Calculates real-world speed of tracked objects in km/h.
    """

    def __init__(self, pixels_per_meter=20):
        """
        Args:
            pixels_per_meter (float): Number of pixels representing 1 meter.
        """
        self.prev_positions = defaultdict(lambda: {"pos": None, "time": None})
        self.PIXELS_PER_METER = pixels_per_meter

    def update(self, track_id, current_position):
        """
        Updates the speed for a given track ID and returns it.

        Args:
            track_id (int): Unique ID of the tracked object.
            current_position (tuple): (x, y) pixel coordinates.

        Returns:
            float: Speed in km/h.
        """
        now = time.time()
        prev_data = self.prev_positions[track_id]
        speed_kph = 0.0

        if prev_data["pos"] is not None:
            dx = current_position[0] - prev_data["pos"][0]
            dy = current_position[1] - prev_data["pos"][1]
            distance_pixels = np.sqrt(dx**2 + dy**2)

            dt = now - prev_data["time"]

            if dt > 0:
                distance_meters = distance_pixels / self.PIXELS_PER_METER
                speed_mps = distance_meters / dt       # meters per second
                speed_kph = speed_mps * 3.6           # km/h

        self.prev_positions[track_id] = {"pos": current_position, "time": now}

        return speed_kph
