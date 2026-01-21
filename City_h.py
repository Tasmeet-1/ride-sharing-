# ================================
# City_h.py
# Interface / Header Simulation
# ================================

class City:
    """
    Represents the city as a weighted graph.
    Nodes = locations
    Edges = roads with distances
    Zones are logical partitions.
    """

    def __init__(self):
        pass

    def add_location(self, location, zone_id):
        pass

    def add_road(self, src, dest, distance):
        pass

    def get_zone(self, location):
        pass

    def shortest_path(self, start, end):
        pass

    def print_city(self):
        pass