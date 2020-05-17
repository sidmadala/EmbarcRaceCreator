from heuristics import loop, out_and_back, osm_to_gpx
import pandas as pd
import decimal

"""
1. Get name, coordinates, distance 
2. Create route based on above parameters
3. Save route in .gpx file => name-route-number.gpx
4. Send to Kevin for validation
"""

df = pd.read_excel(open('data/RaceRoutes.xlsx','rb'))
print(df.head())

#loops = loop.create_route(lat_long, distance)

for index, runner in df.iterrows():
    name = runner["Name"]
    start_latitude = df['Latitude']
    start_longitude = df['Longitude']
    lat = float(start_latitude[index])
    long = float(start_longitude[index])
    distance = df['Distance (km)'][index]
    lat_long = (lat, long)
    
    print(runner['Name'])
    print(lat_long)
    print(distance)
    
    try:
        loops, nodes = loop.create_route(lat_long, distance, name)
    except:
        print(f"Error creating routes for runner: {name}")

    print(f"Number of routes: {len(loops)}")

    count = 1
    for path in loops:
        try:
            osm_to_gpx.convert(path=path, nodes=nodes, filename=f"routes/{name}-route-{count}.gpx")
        except:
            print(f"Error creating gpx for runner: {name}")
        count += 1




