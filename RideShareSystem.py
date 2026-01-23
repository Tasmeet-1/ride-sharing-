from Trip import Trip

class RideShareSystem:
    def __init__(self, dispatch_engine, rollback_manager):
        self.dispatch_engine = dispatch_engine
        self.rollback_manager = rollback_manager
        self.trips = []
        self.completed_trips = []
        self.cancelled_trips = []

    def request_trip(self, trip_id, rider, drivers):
        driver, distance = self.dispatch_engine.assign_driver(drivers, rider)
        if not driver:
            return None

        trip = Trip(trip_id, rider, driver)
        trip.distance = distance

        self.rollback_manager.save_state((trip, driver.available))
        driver.assign()
        trip.transition("ASSIGNED")

        self.trips.append(trip)
        return trip

    def cancel_trip(self, trip):
        self.rollback_manager.save_state((trip, trip.driver.available))
        trip.transition("CANCELLED")
        trip.driver.release()
        self.cancelled_trips.append(trip)

    def complete_trip(self, trip):
        trip.transition("ONGOING")
        trip.transition("COMPLETED")
        trip.driver.release()
        self.completed_trips.append(trip)
