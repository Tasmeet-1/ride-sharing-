# ================================
# City_cpp.py
# Implementation
# ================================

from City_h import City


class City:
    def __init__(self):
        # adjacency list
        # { location: [(neighbor, distance), ...] }
        self.graph = {}

        # zone mapping
        # { location: zone_id }
        self.zones = {}

    # =========================
    # Location & Zone Handling
    # =========================
    def add_location(self, location, zone_id):
        if location not in self.graph:
            self.graph[location] = []
            self.zones[location] = zone_id

    def add_road(self, src, dest, distance):
        if src not in self.graph or dest not in self.graph:
            raise Exception("Both locations must exist")

        self.graph[src].append((dest, distance))
        self.graph[dest].append((src, distance))

    def get_zone(self, location):
        return self.zones.get(location, None)

    # =========================
    # Shortest Path (Dijkstra)
    # NO heapq used
    # =========================
    def shortest_path(self, start, end):
        if start not in self.graph or end not in self.graph:
            raise Exception("Invalid start or end location")

        visited = set()
        distance = {}

        # Initialize distances
        for node in self.graph:
            distance[node] = float('inf')

        distance[start] = 0

        while len(visited) < len(self.graph):
            # Pick unvisited node with min distance
            current = None
            min_dist = float('inf')

            for node in self.graph:
                if node not in visited and distance[node] < min_dist:
                    min_dist = distance[node]
                    current = node

            if current is None:
                break

            visited.add(current)

            # Relax neighbors
            for neighbor, weight in self.graph[current]:
                if neighbor not in visited:
                    if distance[current] + weight < distance[neighbor]:
                        distance[neighbor] = distance[current] + weight

        return distance[end]

    # =========================
    # Debug Utility
    # =========================
    def print_city(self):
        print("City Map:")
        for loc in self.graph:
            print(f"{loc} (Zone {self.zones[loc]}) -> {self.graph[loc]}")

#testing code
from City_cpp import City

city = City()

city.add_location("A", 1)
city.add_location("B", 1)
city.add_location("C", 2)

city.add_road("A", "B", 5)
city.add_road("B", "C", 7)

print(city.shortest_path("A", "C"))  # 12
city.print_city()
#testbreak