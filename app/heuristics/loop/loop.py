import osmnx as ox
from .helpers import path_length, osmid_to_gpx, get_pivots, make_loop


def create_route(coords, dist_goal, name):
    """
    Creates list of routes
    Parameters:
        coords (tuple): (latitude,longitude)
        dist_goal (int): desired length in km
    Returns:
        paths (list): list of lists, each sublist is a path (list of osmid's)
    """
    graph = ox.core.graph_from_point(coords, distance=dist_goal * 250)
    start = ox.get_nearest_node(graph, coords)
    nodes, _ = ox.graph_to_gdfs(graph)
    pivots = get_pivots(graph, start, dist_goal)

    print(start)

    paths = []
    for piv in pivots:
        test = make_loop(graph, piv, start, dist_goal)
        paths.append(test)
        ox.plot_graph_route(graph, test)

    # count = 1
    # print(len(paths))
    # for path in paths:
    #     print(count)
    #     osmid_to_gpx(path, nodes=nodes, filename=f"{name}-route-{count}.gpx")
    #     count += 1

    return paths
