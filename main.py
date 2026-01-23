from City import City
from driver import Driver
from rider import Rider
from DispatchEngine import DispatchEngine
from RollbackManager import RollbackManager
from RideShareSystem import RideShareSystem

def run_tests():
    city = City()
    city.add_road("A", "B", 5)
    city.add_road("B", "C", 3)

    drivers = [
        Driver(1, "A", "Zone1"),
        Driver(2, "C", "Zone2")
    ]

    rider = Rider(101, "B", "C")

    dispatch = DispatchEngine(city)
    rollback = RollbackManager()
    system = RideShareSystem(dispatch, rollback)

    trip = system.request_trip(1, rider, drivers)
    assert trip is not None
    assert trip.state == "ASSIGNED"

    system.cancel_trip(trip)
    assert trip.state == "CANCELLED"
    assert drivers[0].available is True

    print("All tests passed successfully.")

if __name__ == "__main__":
    run_tests()
