import osmnx as ox
import networkx as nx


def create_route(coords, dist_goal, tolerance=10):
    """
    Creates list of routes

    Parameters:
        coords (tuple): (latitude,longitude)

        dist_goal (int): desired length in km

        tolerance (int): desired length +- tolerance
            defaults to 10 METERS

    Returns:
        paths (list): list of lists, each sublist is a path (list of (lat, long) tuples)
    """
    graph = ox.core.graph_from_point(coords, distance=dist_goal * 500 + tolerance)
    start = ox.get_nearest_node(graph, coords)
    nodes, _ = ox.graph_to_gdfs(graph)

    nodes_lengths = nx.single_source_dijkstra_path_length(graph, start, cutoff=dist_goal * 500,
                                                          weight='length')

    candidates = [v for v, l in nodes_lengths.items()
                  if (l < (dist_goal * 500 + tolerance) and l > (dist_goal * 500 - tolerance))]

    paths = []
    for node in candidates:
        there = nx.shortest_path(graph, start, node, weight="length")
        back = there[-2::-1]
        back[0:0] = there
        paths.append([(nodes.loc[k].y, nodes.loc[k].x) for k in back])
        # paths.append(back)
        # ox.plot_graph_route(graph, there)

    return paths
