"""
Edmonds-Karp implementation for maximum flow in a logistics network.
"""
from collections import deque, defaultdict

class FlowNetwork:
    def __init__(self):
        # capacities[u][v] = capacity from u to v
        self.capacities = defaultdict(dict)
        self.neighbors = defaultdict(list)

    def add_edge(self, u, v, w):
        # add forward edge
        self.capacities[u][v] = w
        # initialize reverse edge capacity to 0 if not exists
        if v not in self.capacities or u not in self.capacities[v]:
            self.capacities[v].setdefault(u, 0)
        # track neighbors for BFS
        if v not in self.neighbors[u]:
            self.neighbors[u].append(v)
        if u not in self.neighbors[v]:
            self.neighbors[v].append(u)

    def bfs(self, source, sink, parent):
        visited = set()
        queue = deque([source])
        visited.add(source)
        while queue:
            u = queue.popleft()
            for v in self.neighbors[u]:
                # if not visited and residual capacity > 0
                if v not in visited and self.capacities[u].get(v, 0) > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    def edmonds_karp(self, source, sink):
        parent = {}
        max_flow = 0
        # residual capacities are stored in capacities
        while self.bfs(source, sink, parent):
            # find bottleneck
            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.capacities[parent[s]][s])
                s = parent[s]
            # update residual capacities
            v = sink
            while v != source:
                u = parent[v]
                self.capacities[u][v] -= path_flow
                self.capacities[v][u] += path_flow
                v = u
            max_flow += path_flow
        return max_flow

if __name__ == "__main__":
    # build network
    net = FlowNetwork()
    source = 'source'
    sink = 'sink'

    # Terminals capacities
    cap_T1 = 25 + 20 + 15
    cap_T2 = 15 + 30 + 10
    net.add_edge(source, 'T1', cap_T1)
    net.add_edge(source, 'T2', cap_T2)

    # Terminal to Warehouses
    net.add_edge('T1', 'S1', 25)
    net.add_edge('T1', 'S2', 20)
    net.add_edge('T1', 'S3', 15)
    net.add_edge('T2', 'S3', 15)
    net.add_edge('T2', 'S4', 30)
    net.add_edge('T2', 'S2', 10)

    # Warehouses to Shops
    net.add_edge('S1', 'M1', 15)
    net.add_edge('S1', 'M2', 10)
    net.add_edge('S1', 'M3', 20)
    net.add_edge('S2', 'M4', 15)
    net.add_edge('S2', 'M5', 10)
    net.add_edge('S2', 'M6', 25)
    net.add_edge('S3', 'M7', 20)
    net.add_edge('S3', 'M8', 15)
    net.add_edge('S3', 'M9', 10)
    net.add_edge('S4', 'M10', 20)
    net.add_edge('S4', 'M11', 10)
    net.add_edge('S4', 'M12', 15)
    net.add_edge('S4', 'M13', 5)
    net.add_edge('S4', 'M14', 10)

    # Shops to sink, capacity as sum of incoming
    shop_caps = {
        'M1': 15, 'M2': 10, 'M3': 20,
        'M4': 15, 'M5': 10, 'M6': 25,
        'M7': 20, 'M8': 15, 'M9': 10,
        'M10':20, 'M11':10, 'M12':15, 'M13':5, 'M14':10
    }
    for m, cap in shop_caps.items():
        net.add_edge(m, sink, cap)

    max_flow = net.edmonds_karp(source, sink)
    print(f"Maximum flow from terminals to shops: {max_flow}")

    # print flows on each edge (original capacity - residual)
    print("\nFlows per edge:")
    for u in net.capacities:
        for v, residual in net.capacities[u].items():
            # original capacity = residual in reverse edge
            flow = net.capacities[v].get(u, 0)
            # only print forward edges that had capacity
            if u != 'source' and v != 'sink' and flow > 0:
                print(f"{u} -> {v}: {flow}")
    # also T1,T2 edges
    print("source edges:")
    for v, cap in [('T1', cap_T1), ('T2', cap_T2)]:
        flow = net.capacities[v].get('source', 0)
        print(f"source -> {v}: {flow}")
