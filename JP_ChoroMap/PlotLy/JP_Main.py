from urllib.request import urlopen
import requests
import pandas as pd
import plotly
import json
import pickle
# Convert Japanese to terminal printable ASCII (convenient)
import pykakasi


# GET geojson DATA
# ONLINE
with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/japan.geojson') as response:
    prefs = json.load(response, encoding='utf-8')
with open('JP_ChoroMap/Data.json', 'wb') as fp :
    pickle.dump(prefs, fp, protocol=pickle.HIGHEST_PROTOCOL)


# SAVED
# with open('JP_ChoroMap/Data.pckl', 'rb') as fp :
#     prefs = pickle.load(fp)

for feat in prefs['features'] :
    feat['id'] = str(feat['properties']['cartodb_id'])
    del feat['properties']['cartodb_id']


 # Data Structure
Pref_Names = []
Pref_Id = []
for pref_id in range(len(prefs['features'])) :
    prefName = prefs['features'][pref_id]['properties']['name_english'].lower()
    prefId = prefs['features'][pref_id]['id']
    Pref_Names.append(prefName)
    Pref_Id.append(prefId)

State_Id = range(0, len(Pref_Names))
Mapper_NameId = dict(zip(Pref_Names, Pref_Id))
Mapper_IdName = dict(zip(Pref_Id, Pref_Names))

from bs4 import BeautifulSoup
# GET PREF GDP DATA
url_GDP = 'https://en.wikipedia.org/wiki/List_of_Japanese_prefectures_by_GDP'
wiki_url = requests.get(url_GDP).text
soup = BeautifulSoup(wiki_url, 'lxml')
Table = soup.find('table', class_='wikitable')
rows = Table.findAll('tr')
df_data = []


for row in rows :
    title_entry = row.findAll('a')
    if title_entry :
        pref_name = title_entry[0].getText().lower()
        if pref_name == 'japan' : continue
        data_entries = row.findAll('td')
        data = [pref_name, Mapper_NameId[pref_name],
                int(data_entries[1].getText().rstrip()),
                int(data_entries[2].getText().rstrip().replace(',', '')),
                float(data_entries[3].getText().rstrip().replace(',', '')),
                float(data_entries[4].getText().rstrip().replace(',', ''))]
        df_data.append(data)
df = pd.DataFrame(data=df_data, columns=['prefecture', 'pref_id', 'rank', 'GDP_Y', 'GDP_Dol', 'share'])

# IN YEN
# import plotly.express as px
# df = df.drop(axis=1, columns=['prefecture', 'rank', 'GDP_Dol', 'share'])
# fig = px.choropleth_mapbox(df, geojson=prefs, locations='pref_id', color='GDP_Y',
#                            color_continuous_scale="Inferno",
#                            range_color=(0, max(df.GDP_Y)),
#                            mapbox_style="carto-positron",
#                            zoom=3, center = {"lat": 37.0902, "lon": 136},
#                            opacity=0.5,
#                            labels={'unemp':'unemployment rate'}
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

# IN US DOLLAR
import plotly.express as px
df = df.drop(axis=1, columns=['prefecture', 'rank', 'GDP_Y', 'share'])
fig = px.choropleth_mapbox(df, geojson=prefs, locations='pref_id', color='GDP_Dol',
                           color_continuous_scale="Inferno",
                           range_color=(0, max(df.GDP_Dol)),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": 136},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
