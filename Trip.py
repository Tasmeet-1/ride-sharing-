class Trip:
    VALID_TRANSITIONS = {
        "REQUESTED": ["ASSIGNED", "CANCELLED"],
        "ASSIGNED": ["ONGOING", "CANCELLED"],
        "ONGOING": ["COMPLETED"],
        "COMPLETED": [],
        "CANCELLED": []
    }

    def __init__(self, trip_id, rider, driver=None):
        self.trip_id = trip_id
        self.rider = rider
        self.driver = driver
        self.state = "REQUESTED"
        self.distance = 0

    def transition(self, new_state):
        if new_state not in self.VALID_TRANSITIONS[self.state]:
            raise Exception(f"Invalid transition from {self.state} to {new_state}")
        self.state = new_state
