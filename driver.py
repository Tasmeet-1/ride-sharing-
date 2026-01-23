class Driver:
    def __init__(self, driver_id, location, zone):
        self.driver_id = driver_id
        self.location = location
        self.zone = zone
        self.available = True

    def assign(self):
        self.available = False

    def release(self):
        self.available = True
