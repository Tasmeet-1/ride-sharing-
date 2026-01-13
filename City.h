#ifndef CITY_H
#define CITY_H
class City {
public:
    City(int numNodes);
    void addEdge(int u, int v, int weight);
    int shortestPath(int start, int end);
private:
    int nodes;
    int** adjacencyMatrix; 
};
#endif