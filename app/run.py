from heuristics import loop, out_and_back, osm_to_gpx
import pandas as pd
import decimal

"""
1. Get name, coordinates, distance 
2. Create route based on above parameters
3. Save route in .gpx file => name-route-number.gpx
4. Send to Kevin for validation
"""

df = pd.read_excel(open('data/RaceRoutes.xlsx','rb'), sheet_name="Sheet4")
# df = pd.read_excel(open('data/RaceRoutes.xlsx','rb'), sheet_name="Sheet2")
print(df.head())

for index, runner in df.iterrows():
    
    # if runner["Name"] != "Helmer":
    #     continue

    name = runner["Name"]
    
    start_latitude = df['Latitude']
    start_longitude = df['Longitude']
    
    lat = float(start_latitude[index])
    lon = float(start_longitude[index])
    distance = df['Distance (km)'][index]
    
    lat_long = (lat, lon)
    
    print(runner['Name'])
    print(lat_long)
    print(distance)
    
    try:
        loops, nodes = loop.create_route(lat_long, distance)
    except Exception as exception:
        print(f"Error creating routes for runner: {name}")
        print(exception)
        continue
    print(f"Number of routes: {len(loops)}")

    count = 1
    for path in loops:
        try:
            osm_to_gpx.convert(path=path, nodes=nodes, filename=f"routes/{name}-route-{count}.gpx")
        except Exception as exception:
            print(f"Error creating gpx for runner: {name}")
            print(exception)
            continue
        count += 1




