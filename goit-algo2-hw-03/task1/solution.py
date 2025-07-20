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
    # --- Network Definition ---
    net = FlowNetwork()
    source, sink = 'source', 'sink'
    
    # Keep track of original capacities for the report
    original_capacities = {}
    def add_edge_and_track(u, v, w):
        net.add_edge(u, v, w)
        original_capacities[(u, v)] = w

    # Define network structure using the helper
    cap_T1 = 25 + 20 + 15
    cap_T2 = 15 + 30 + 10
    add_edge_and_track(source, 'T1', cap_T1)
    add_edge_and_track(source, 'T2', cap_T2)
    
    add_edge_and_track('T1', 'S1', 25); add_edge_and_track('T1', 'S2', 20); add_edge_and_track('T1', 'S3', 15)
    add_edge_and_track('T2', 'S3', 15); add_edge_and_track('T2', 'S4', 30); add_edge_and_track('T2', 'S2', 10)
    
    shop_caps = {
        'M1': 15, 'M2': 10, 'M3': 20, 'M4': 15, 'M5': 10, 'M6': 25,
        'M7': 20, 'M8': 15, 'M9': 10, 'M10': 20, 'M11': 10, 'M12': 15,
        'M13': 5, 'M14': 10
    }
    add_edge_and_track('S1', 'M1', 15); add_edge_and_track('S1', 'M2', 10); add_edge_and_track('S1', 'M3', 20)
    add_edge_and_track('S2', 'M4', 15); add_edge_and_track('S2', 'M5', 10); add_edge_and_track('S2', 'M6', 25)
    add_edge_and_track('S3', 'M7', 20); add_edge_and_track('S3', 'M8', 15); add_edge_and_track('S3', 'M9', 10)
    add_edge_and_track('S4', 'M10', 20); add_edge_and_track('S4', 'M11', 10); add_edge_and_track('S4', 'M12', 15)
    add_edge_and_track('S4', 'M13', 5); add_edge_and_track('S4', 'M14', 10)

    for m, cap in shop_caps.items():
        add_edge_and_track(m, sink, cap)

    # --- Max Flow Calculation ---
    max_flow = net.edmonds_karp(source, sink)
    print(f"Maximum flow from terminals to shops: {max_flow}\n")

    # --- Simplified Flow Report ---
    print("Звіт: Розподіл потоків від терміналів до магазинів")
    print("-" * 50)
    # This is a heuristic: trace flow back from shops to warehouses, then to terminals
    flows = defaultdict(lambda: defaultdict(int))
    for shop in sorted(shop_caps.keys(), key=lambda x: int(x[1:])):
        for wh in ['S1', 'S2', 'S3', 'S4']:
            flow_ws = net.capacities[shop].get(wh, 0)
            if flow_ws > 0:
                flow_t1_wh = net.capacities[wh].get('T1', 0)
                flow_t2_wh = net.capacities[wh].get('T2', 0)
                total_inflow = flow_t1_wh + flow_t2_wh
                if total_inflow > 0:
                    flows['Термінал 1'][shop] += flow_ws * (flow_t1_wh / total_inflow)
                    flows['Термінал 2'][shop] += flow_ws * (flow_t2_wh / total_inflow)

    for term in ['Термінал 1', 'Термінал 2']:
        for shop in sorted(shop_caps.keys(), key=lambda x: int(x[1:])):
            flow = flows[term][shop]
            if flow > 0.1:
                print(f"{term}\tМагазин {shop[1:]:<5}\t{int(round(flow))}")
    print("-" * 50)

    # --- Enhanced Visualization ---
    try:
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.DiGraph()
        for (u, v), cap in original_capacities.items():
            flow = net.capacities[v].get(u, 0)
            G.add_edge(u, v, capacity=cap, flow=flow)

        node_colors = {n: 'skyblue' for n in G.nodes()}
        for n in G.nodes():
            if n.startswith('T'): node_colors[n] = 'blue'
            elif n.startswith('S'): node_colors[n] = 'orange'
            elif n.startswith('M'): node_colors[n] = 'green'
            elif n == source: node_colors[n] = 'purple'
            elif n == sink: node_colors[n] = 'gold'

        # Compute and print shortest path once, then style edges
        try:
            sp = nx.shortest_path(G, source, sink)
            shortest_edges = set(zip(sp, sp[1:]))
            print(f"\nНайкоротший шлях від {source} до {sink}: {' -> '.join(sp)}")
        except nx.NetworkXNoPath:
            shortest_edges = set()
            print(f"\nНемає шляху від {source} до {sink}")

        edge_colors = []
        edge_styles = []
        for u, v, data in G.edges(data=True):
            if (u, v) in shortest_edges:
                edge_colors.append('purple')
                edge_styles.append('solid')
            elif data['flow'] == 0:
                edge_colors.append('lightgray')
                edge_styles.append('dotted')
            elif data['flow'] == data['capacity']:
                edge_colors.append('red')  # Bottleneck
                edge_styles.append('solid')
            else:
                edge_colors.append('black')
                edge_styles.append('solid')

        plt.figure(figsize=(20, 24))
        
        for n in G.nodes():
            if n == source: G.nodes[n]["layer"] = 0
            elif n.startswith('T'): G.nodes[n]["layer"] = 1
            elif n.startswith('S'): G.nodes[n]["layer"] = 2
            elif n.startswith('M'): G.nodes[n]["layer"] = 3
            elif n == sink: G.nodes[n]["layer"] = 4
        pos = nx.multipartite_layout(G, subset_key="layer")

        nx.draw(G, pos, with_labels=True, node_color=[node_colors.get(n) for n in G.nodes()],
                edge_color=edge_colors, style=edge_styles, node_size=1000, arrowsize=20)
        edge_labels = {(u, v): f"{int(d['flow'])}/{d['capacity']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='navy')
        
        plt.title("Аналіз потоків логістичної мережі (Потік / Пропускна здатність)", fontsize=20)
        plt.show()

    except ImportError:
        print("\nДля візуалізації встановіть: pip install networkx matplotlib")
