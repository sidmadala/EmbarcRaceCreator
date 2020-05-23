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
                 "<gpx xmlns=\"http://www.topografix.com/GPX/1/1\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" version=\"1.1\"" + "\n" +
                 "xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd\">" + "\n" +
                 "<trk>" + "\n" +
                 "<trkseg>" + "\n")
    body = [str("<trkpt lon=\"{:}\" lat=\"{:}\"></trkpt>".format(nodes.loc[k].x, nodes.loc[k].y) + "\n") for k in path]
    end = str("</trkseg></trk></gpx>")
    with open(filename, "w+") as output:
        output.write(header)
        output.writelines(body)
        output.write(end)