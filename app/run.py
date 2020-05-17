from heuristics import loop
from heuristics import out_and_back
import pandas as pd


df = pd.read_excel(open('data/RaceRoutes.xlsx','rb'))
print(df.head())

#loops = loop.create_route(lat_long, distance)

for index, runner in df.iterrows():
    name = runner["Name"]
    start_lat_long = df['Lat/Long']
    lat = float(start_lat_long[index][0:7])
    long = float(start_lat_long[index][10::])
    distance = df['Distance (km)'][index]
    lat_long = (lat, long)
    
    print(runner['Name'])
    print(lat_long)
    print(distance)
    
    loops = loop.create_route(lat_long, distance, name)
    print(len(loops))
    break    

"""
1. Get name, coordinates, distance 
2. Create route based on above parameters
3. Save route in .gpx file => name-route-number.gpx
4. Send to Kevin for validation
"""

