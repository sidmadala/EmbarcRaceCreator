import osmnx as ox
import networkx as nx
import geopy.distance
import numpy as np


class Conversion:
    def __init__(self, lat):
        self.km_per_lat = 6371 * (np.pi / 180)
        self.km_per_long = np.cos(lat * (np.pi / 180)) * self.km_per_lat

    def __call__(self, dy, dx):
        """
        Converts lat/long distance to km distance
            BE CAREFUL: the conversion between long and km depends on the lat

        Parameters:
            dx (int): change in long

            dy (int): change in lat
        """
        return np.sqrt((dy * self.km_per_lat) ** 2 + (dx * self.km_per_long) ** 2)


def path_length(path, nodes):
    """
    Calculates length of path in km.

    Parameters:
        path (list): specifically a list of integer osmid

        nodes (geodataframe): gdf indexed by osmid, containing lat/long info of the
            node where x = longitude, y = latitude

    Returns:
        dist_travelled (float): length of path (km) inputted
    """
    dist_travelled = 0
    path = [nodes.loc[x] for x in path]
    for k in range(len(path) - 1):
        coords1 = (path[k].y, path[k].x)  # (lat, long)
        coords2 = (path[k + 1].y, path[k + 1].x)
        dist_travelled += geopy.distance.distance(coords1, coords2).km
    return dist_travelled


def osmid_to_gpx(path, nodes, filename="test.gpx"):
    """
    Converts path to gpx file.

    Parameters:
        path (list): specifically a list of integer osmid

        nodes (geodataframe): gdf indexed by osmid, containing lat/long info of the
            node where x = longitude, y = latitude

        filename (string): name_of_file.gpx
    """
    header = str("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n" +
                 "<gpx xmlns=\"http://www.topografix.com/GPX/1/1\" "
                 "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" version=\"1.1\"" + "\n" +
                 "xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd\">" + "\n" +
                 "<trk>" + "\n" +
                 "<trkseg>" + "\n")
    body = [str("<trkpt lon=\"{:}\" lat=\"{:}\"></trkpt>".format(nodes.loc[k].x, nodes.loc[k].y) + "\n") for k in path]
    end = str("</trkseg></trk></gpx>")
    with open(filename, "w+") as output:
        output.write(header)
        output.writelines(body)
        output.write(end)


def get_pivots(graph, start, dist):
    """
    Gets 4 points to use as pivots for the loop algorithm

    Parameters:
        graph (osmnx graph): graph structure determined by start location

        start (int): osmid of nearest node to start coordinates

        dist (int): distance goal in km

    Returns:
        pivots (list): list of 4 pivot nodes, unordered
    """
    nodes, edges = ox.graph_to_gdfs(graph)
    start_coords = (nodes.loc[start]['y'], nodes.loc[start]['x']) # (lat,long)

    norm = Conversion(start_coords[0])

    adjs = list(graph.successors(start))

    slopes = [(nodes.loc[point]['y'] - start_coords[0], nodes.loc[point]['x'] - start_coords[1]) for point in adjs]

    # if not enough pivots:
    if len(adjs) == 1:
        slopes.append((-slopes[0][0], -slopes[0][1]))
        slopes.append((-slopes[0][1], -slopes[0][0]))
        slopes.append((slopes[0][1], slopes[0][0]))
    elif len(adjs) == 2:
        slopes.append(tuple(-np.sum(slopes, axis=0)))
        ang1 = np.arccos(np.dot((slopes[0] / np.linalg.norm(slopes[0])), (slopes[1] / np.linalg.norm(slopes[1]))))
        ang2 = np.arccos(np.dot((slopes[1] / np.linalg.norm(slopes[1])), (slopes[2] / np.linalg.norm(slopes[2]))))
        ang3 = np.arccos(np.dot((slopes[2] / np.linalg.norm(slopes[2])), (slopes[0] / np.linalg.norm(slopes[0]))))
        idx = np.argmax([ang1, ang2, ang3])
        slopes.append(tuple(-np.array(slopes[idx - 1])))
    elif len(adjs) == 3:
        ang1 = np.arccos(np.dot((slopes[0] / np.linalg.norm(slopes[0])), (slopes[1] / np.linalg.norm(slopes[1]))))
        ang2 = np.arccos(np.dot((slopes[1] / np.linalg.norm(slopes[1])), (slopes[2] / np.linalg.norm(slopes[2]))))
        ang3 = np.arccos(np.dot((slopes[2] / np.linalg.norm(slopes[2])), (slopes[0] / np.linalg.norm(slopes[0]))))
        idx = np.argmax([ang1, ang2, ang3])
        slopes.append(tuple(-np.array(slopes[idx - 1])))

    pivot_coords = [(dy * dist / (2 * np.pi + 1) / norm(dy, dx) + start_coords[0],
                     dx * dist / (2 * np.pi + 1) / norm(dy, dx) + start_coords[1]) for dy, dx in slopes]

    pivots = [ox.get_nearest_node(graph, pc) for pc in pivot_coords]

    return pivots


def make_loop(graph, center_pivot, start, dist):
    """
    Makes loop trail corresponding to center-pivot w.r.t start

    Parameters:
        graph (osmnx graph): graph structure determined by start location

        center_pivot (int): osmid of center-pivot node

        start (int): osmid of nearest node to start coordinates

        dist (int): distance goal in km

    Returns:
        temp (list): list of osmid corresponding to path nodes
    """
    pivots = get_pivots(graph, center_pivot, dist)

    temp = nx.multi_source_dijkstra(graph, pivots, start, weight="length")[-1]
    visited = {temp[0]}
    while len(pivots) != len(visited):
        temp[0:0] = nx.multi_source_dijkstra(graph, set(pivots) - visited, temp[0], weight="length")[-1][:-1]
        visited.add(temp[0])

    temp[0:0] = nx.shortest_path(graph, start, temp[0], weight="length")[:-1]
    return temp
