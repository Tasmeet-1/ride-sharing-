import heapq

class City:
    def __init__(self):
        self.graph = {}

    def add_location(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_road(self, src, dest, distance):
        self.add_location(src)
        self.add_location(dest)
        self.graph[src].append((dest, distance))
        self.graph[dest].append((src, distance))

    def shortest_path(self, start, end):
        pq = [(0, start)]
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        while pq:
            current_dist, node = heapq.heappop(pq)

            if node == end:
                return current_dist

            if current_dist > distances[node]:
                continue

            for neighbor, weight in self.graph[node]:
                dist = current_dist + weight
                if dist < distances[neighbor]:
                    distances[neighbor] = dist
                    heapq.heappush(pq, (dist, neighbor))

        return float('inf')
