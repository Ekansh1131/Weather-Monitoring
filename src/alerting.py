from .config import TEMPERATURE_THRESHOLD, CONSECUTIVE_UPDATES_THRESHOLD

class AlertSystem:
    def __init__(self):
        self.consecutive_high_temp_count = {}  # Dictionary to track counts per city

    def check_temperature_alert(self, city, temp):
        if temp > TEMPERATURE_THRESHOLD:
            self.consecutive_high_temp_count[city] = self.consecutive_high_temp_count.get(city, 0) + 1
            if self.consecutive_high_temp_count[city] >= CONSECUTIVE_UPDATES_THRESHOLD:
                return True
        else:
            self.consecutive_high_temp_count[city] = 0
        return False

    def generate_alert(self, city, temp):
        message = (
            f"⚠️ ALERT: Temperature in {city} has exceeded {TEMPERATURE_THRESHOLD}°C "
            f"for {CONSECUTIVE_UPDATES_THRESHOLD} consecutive updates.\n"
            f"Current temperature: {temp:.1f}°C"
        )
        print("\n" + "=" * 60)
        print(message)
        print("=" * 60 + "\n")
        
        # Here you could add email notifications or other alert mechanisms
        return message