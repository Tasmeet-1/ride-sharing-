#include "City.h"
#include <limits>

City::City() : edgeCnt(0), nodeCnt(0) {
    for (int i=0;i<MAX_NODES;i++){ head[i]=-1; zoneOf[i]=-1; }
}
void City::addNode(int id, int zone){
    if(id>=0 && id<MAX_NODES){ zoneOf[id]=zone; nodeCnt++; }
}
void City::addEdge(int u,int v,int w){
    if(edgeCnt<MAX_EDGES && u>=0 && v>=0){
        edges[edgeCnt]={v,w,head[u]}; head[u]=edgeCnt++;
        edges[edgeCnt]={u,w,head[v]}; head[v]=edgeCnt++;
    }
}
int City::getZone(int node) const { return zoneOf[node]; }
int City::nodeCount() const { return nodeCnt; }

// Array-based Dijkstra (no STL). Returns dist[dst] or -1.
int City::shortestPath(int src,int dst,int* dist,int* parent) const{
    const int INF = std::numeric_limits<int>::max()/4;
    bool vis[MAX_NODES]; 
    for(int i=0;i<MAX_NODES;i++){ dist[i]=INF; parent[i]=-1; vis[i]=false; }
    dist[src]=0;
    for(int k=0;k<MAX_NODES;k++){
        int u=-1, best=INF;
        for(int i=0;i<MAX_NODES;i++) if(!vis[i] && dist[i]<best){ best=dist[i]; u=i; }
        if(u==-1) break;
        vis[u]=true;
        for(int e=head[u]; e!=-1; e=edges[e].next){
            int v=edges[e].to, w=edges[e].w;
            if(dist[u]+w<dist[v]){ dist[v]=dist[u]+w; parent[v]=u; }
        }
    }
    return dist[dst]==INF ? -1 : dist[dst];
}