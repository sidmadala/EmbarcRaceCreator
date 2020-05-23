def convert(path, nodes, filename="test.gpx"):
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
