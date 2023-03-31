import time
from datetime import datetime


class PicoRunner:
    def __init__(self):
        self.weight_base_line = 0
        return

    def loop(self):
        start_time = 0
        end_time = 0
        weight_changed_before = False
        while True:
            # simulate reading from sensor. 
            weight_reading = input("Enter a weight: ")
            weight_reading = int(weight_reading)
            if self.is_weight_changed(weight_reading, self.weight_base_line) and not weight_changed_before:
                start_time = time.time()
                weight_changed_before = True
            if not self.is_weight_changed(weight_reading, self.weight_base_line) and weight_changed_before:
                end_time = time.time()
            if (start_time != 0 and end_time != 0):
                duration = end_time - start_time

                start_time = 0
                end_time = 0
                weight_changed_before = False

                event_type = self.detemine_poop_or_pee(duration)
                timestamp = datetime.now()
                self.upload_to_cloud(timestamp, event_type)
        
            time.sleep(0.1)

    
    def is_weight_changed(self, weight_reading, weight_base_line):
        # may be weight_reading - weight_base_line > 0.5 because of the reading error
        return weight_reading != weight_base_line
        
    def detemine_poop_or_pee(self, duration):
        # we need to do some data collect to determine the time thresholds
        if duration > 30:
            return "Poop"
        elif 10 < duration <= 30:
            return "Pee"
        else:
            return "Unknown - for debugging purpose"
    
    def upload_to_cloud(self, timestamp, activity, catName="Haybe"):
        print("++++ Logging data to the cloud ++++")
        print(timestamp, activity, catName)
        print()

if __name__ == "__main__":
    picoRunner = PicoRunner()
    picoRunner.loop()

