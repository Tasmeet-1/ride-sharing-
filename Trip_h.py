# ================================
# Trip_h.py
# (Interface / Header Simulation)
# ================================

from enum import Enum


class TripState(Enum):
    REQUESTED = 1
    ASSIGNED = 2
    ONGOING = 3
    COMPLETED = 4
    CANCELLED = 5


class TripHistoryNode:
    """
    Singly Linked List Node
    Stores one state of trip history
    """

    def __init__(self, state):
        pass


class Trip:
    """
    Trip class with FSM enforcement
    and linked list based history
    """

    def __init__(self, trip_id, rider_id, pickup, dropoff):
        pass

    def assign_driver(self, driver_id):
        pass

    def start_trip(self):
        pass

    def complete_trip(self):
        pass

    def cancel_trip(self):
        pass

    def rollback_last_state(self):
        pass

    def get_current_state(self):
        pass

    def get_history(self):
        pass
