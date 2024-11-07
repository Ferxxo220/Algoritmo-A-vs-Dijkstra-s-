import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time

lugar = "Xalapa, Veracruz"

G = ox.graph_from_place(lugar, network_type="all")


latitud_casa = 19.532861591457866
longitud_casa = -96.9372087165773


nodo_casa = ox.distance.nearest_nodes(G, X=longitud_casa, Y=latitud_casa)


latitud_inicio = 19.515701081915243
longitud_inicio = -96.85515386258835


nodo_inicio = ox.distance.nearest_nodes(G, X=longitud_inicio, Y=latitud_inicio)

def heuristica(u, v):
    x1, y1 = G.nodes[u]['x'], G.nodes[u]['y']
    x2, y2 = G.nodes[v]['x'], G.nodes[v]['y']
    return ox.distance.euclidean_dist_vec(y1, x1, y2, x2)

def astar_with_counting(G, source, target, heuristic, weight):
    iterations = 0
    path = nx.astar_path(G, source, target, heuristic=heuristic, weight=weight)
    iterations = len(path) - 1
    return path, iterations


start_time = time.time()
camino, iterations = astar_with_counting(G, nodo_inicio, nodo_casa, heuristic=heuristica, weight="length")
execution_time = time.time() - start_time


route_length = 0
for u, v in zip(camino[:-1], camino[1:]):
    edge_data = G.get_edge_data(u, v, default=None)
    if edge_data is None:
        edge_data = G.get_edge_data(v, u, default=None)
    if edge_data is not None:
        route_length += edge_data[0]['length']

#velocidad promedio de 40 km/h
average_speed_kph = 40  # km/h
route_length_km = route_length / 1000
estimated_time_hours = route_length_km / average_speed_kph


print(f"Iteraciones: {iterations}")
print(f"Distancia total (m): {route_length:.2f}")
print(f"Tiempo de ejecución (segundos): {execution_time:.4f}")
print(f"Tiempo estimado de viaje (horas): {estimated_time_hours:.2f}")

# Dibujar el grafo y marcar el camino más corto en azul
fig, ax = ox.plot_graph_route(
    G, camino, route_linewidth=2, route_color="blue",
    node_size=30, node_color="red", edge_color="gray",
    show=False, close=False
)

# Cambiar el color de fondo a negro
ax.set_facecolor("black")

# Marcar la casa en el mapa
ax.plot(longitud_casa, latitud_casa, 'go', markersize=10, label="Mi Casa")
ax.legend()
plt.show()

