import osmnx as ox
from .helpers import path_length, get_pivots, alt_pivots, make_loop, alt_loop
import cProfile, pstats

def create_route(coords, dist_goal):
    """
    Creates list of routes

    Parameters:
        coords (tuple): (latitude,longitude)

        dist_goal (int): desired length in km

    Returns:
        paths (list): list of lists, each sublist is a path (list of (lat, long) tuples)
    """
    graph = ox.core.graph_from_point(coords, distance=dist_goal * 1000, simplify=True)
    start = ox.get_nearest_node(graph, coords)
    nodes, _ = ox.graph_to_gdfs(graph)

    pivots = get_pivots(graph, nodes, start, dist_goal)
    # pivots = alt_pivots(graph, nodes, start, dist_goal)

    paths = []
    for piv in pivots:
        test = make_loop(graph, nodes, piv, start, dist_goal)
        if test is None:
            print("repeat pivots, skipping")
            continue
        paths.append(test)

#        ox.plot_graph_route(graph, test)
        # print(len(test))

    return paths, nodes

pr = cProfile.Profile()
pr.enable()

loops, nodes = create_route((40.96238, -73.112820), 5)

pr.disable()

with open('profile_log1', 'w+') as f:
    ps = pstats.Stats(pr, stream=f)
    ps.strip_dirs().sort_stats('tottime').print_stats()
