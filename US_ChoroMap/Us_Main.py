from urllib.request import urlopen
import pandas as pd
import plotly
import json
import pickle

# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response, encoding='utf-8')
# with open('US_ChoroMap/Data.json', 'wb') as fp :
#     pickle.dump(counties, fp, protocol=pickle.DEFAULT_PROTOCOL)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})
# df.to_csv('US_ChoroMap/fips-unemp-16.csv')


# Map Coordinate Data
with open('US_ChoroMap/Data.json', 'rb') as fp :
    counties = pickle.load(fp)
# Map Choropeth Data
df = pd.read_csv('US_ChoroMap/fips-unemp-16.csv', dtype={"fips": str})

import plotly.express as px

fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


#Data Structure
"""
   Unnamed: 0   fips  unemp
0           0  01001    5.3
1           1  01003    5.4
2           2  01005    8.6
3           3  01007    6.6
4           4  01009    5.5
5           5  01011    7.2
6           6  01013    7.1
7           7  01015    6.7
8           8  01017    5.5
9           9  01019    5.2
"""
"""
{'type': 'Feature',
'properties': {'GEO_ID': '0500000US01001',
               'STATE': '01',
               'COUNTY': '001',
                'NAME': 'Autauga',
                'LSAD': 'County',
                'CENSUSAREA': 594.436},
'geometry': {'type': 'Polygon',
             'coordinates': [[[-86.496774, 32.344437], [-86.717897, 32.402814], [-86.814912, 32.340803], [-86.890581, 32.502974], [-86.917595, 32.664169], [-86.71339, 32.661732], [-86.714219, 32.705694], [-86.413116, 32.707386], [-86.411172, 32.409937], [-86.496774, 32.344437]]]},
'id': '01001'}
"""
