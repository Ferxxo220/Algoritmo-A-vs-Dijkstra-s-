import osmnx as ox
import networkx as nx
import time


city_name = "Xalapa, Veracruz, Mexico"
G = ox.graph_from_place(city_name, network_type='drive')

orig_point = (19.518365989221824, -96.88150301884444)  # Coordenadas de inicio
dest_point = (19.523249, -96.907580)  # Coordenadas de destino

orig_node = ox.distance.nearest_nodes(G, X=orig_point[1], Y=orig_point[0])
dest_node = ox.distance.nearest_nodes(G, X=dest_point[1], Y=dest_point[0])

iterations = 0


def dijkstra_with_counting(G, source, target, weight):
    global iterations
    iterations = 0
    distances = {source: 0}
    predecessors = {source: None}
    visited = set()

    queue = [(0, source)]
    while queue:
        (cost, node) = queue.pop(0)

        if node in visited:
            continue
        visited.add(node)

        iterations += 1  

        
        if node == target:
            break

     
        for neighbor, edge_data in G[node].items():
            if neighbor in visited:
                continue
            edge_weight = edge_data[0][weight]
            new_cost = cost + edge_weight
            if neighbor not in distances or new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                predecessors[neighbor] = node
                queue.append((new_cost, neighbor))
                queue.sort()

  
    path = []
    while target is not None:
        path.append(target)
        target = predecessors[target]
    path.reverse()
    return path



start_time = time.time()
shortest_path = dijkstra_with_counting(G, orig_node, dest_node, weight='length')
execution_time = time.time() - start_time


route_length = 0
for u, v in zip(shortest_path[:-1], shortest_path[1:]):
    
    edge_data = G.get_edge_data(u, v, default=None)
    if edge_data is None:  
        edge_data = G.get_edge_data(v, u, default=None)
    if edge_data is not None:
        route_length += edge_data[0]['length']  

# velocidad promedio de 40 km/h
average_speed_kph = 40  # km/h
route_length_km = route_length / 1000  
estimated_time_hours = route_length_km / average_speed_kph


print(f"Iteraciones: {iterations}")
print(f"Distancia total (m): {route_length:.2f}")
print(f"Tiempo de ejecución (segundos): {execution_time:.4f}")
print(f"Tiempo estimado de viaje (horas): {estimated_time_hours:.2f}")


ox.plot_graph_route(G, shortest_path, route_linewidth=3, node_size=0, bgcolor='w')
