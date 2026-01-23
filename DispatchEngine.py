class DispatchEngine:
    def __init__(self, city):
        self.city = city

    def assign_driver(self, drivers, rider):
        best_driver = None
        best_distance = float('inf')

        for driver in drivers:
            if driver.available:
                dist = self.city.shortest_path(driver.location, rider.pickup)
                if dist < best_distance:
                    best_distance = dist
                    best_driver = driver

        return best_driver, best_distance
