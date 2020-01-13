#1 LOAD EXCEL DATA
import pandas as pd
from unidecode import unidecode

# import raw name of columns
cols_raw = pd.read_excel('JP_FullData/DailyTime.xls', skiprows=8, nrows=1, usecols=lambda x: 'Unnamed' not in x,)
cols_raw = list(map(unidecode, cols_raw.columns))[1:]
cols_df = ['Location', 'NONE']
years = ['2006', '2011', '2016']
for i in range(len(cols_raw)) :
    for year in years :
        cols_df.append(cols_raw[i] + year)

df_raw = pd.read_excel('JP_FullData/DailyTime.xls', skiprows=12, usecols='J:BS', skipfooter=9, names=cols_df)
df_raw.drop(df_raw.columns[1], axis=1, inplace=True)
for row_id in df_raw.index :
    df_raw['Location'].iloc[row_id] = df_raw['Location'].iloc[row_id].replace('-ken', '')
    df_raw['Location'].iloc[row_id] = df_raw['Location'].iloc[row_id].replace('-to', '')
    df_raw['Location'].iloc[row_id] = df_raw['Location'].iloc[row_id].replace('-fu', '')
    df_raw['Location'].iloc[row_id] = df_raw['Location'].iloc[row_id].lower()
    if df_raw['Location'].iloc[row_id] == 'gumma' : # Spelling not consistent
        df_raw['Location'].iloc[row_id] = 'gunma'


#2 LOAD geojson (FROM SAVED see JP_Main.py)
import pickle
with open('JP_ChoroMap/Data.json', 'rb') as fp :
    prefs = pickle.load(fp)

for feat in prefs['features'] : # Put the id in the right format
    feat['id'] = str(feat['properties']['cartodb_id'])
    del feat['properties']['cartodb_id']

 # Create dict mappers
Pref_Names = []
Pref_Id = []
for pref_id in range(len(prefs['features'])) :
    prefName = prefs['features'][pref_id]['properties']['name_english'].lower()
    prefId = prefs['features'][pref_id]['id']
    Pref_Names.append(prefName)
    Pref_Id.append(prefId)
Mapper_NameId = dict(zip(Pref_Names, Pref_Id))
Mapper_IdName = dict(zip(Pref_Id, Pref_Names)) # Helpers

###################################CREATE MAP###################################
Col_Interest = 'Hobbies and amusements \n[male with a job]2006' # PUT HERE THE COLUMN TO DISPLAY ON MAP
#1 Set the column you want to display
cols = list(df_raw.columns)
cols.remove('Location')
cols.remove(Col_Interest) # PUT HERE THE COLUMN TO DISPLAY ON MAP
df = df_raw.drop(columns=cols)
df = df.drop(df.tail(2).index) # Dropping mean and SD

# Substite location string for the matching ID
Loc_ID = []
for row_id in df.index :
    Loc_ID.append(Mapper_NameId[df['Location'].iloc[row_id]])
df.insert(loc=0, column='Loc_ID', value=Loc_ID)

# 2 Plot
import plotly.express as px

fig = px.choropleth_mapbox(df, geojson=prefs, locations='Loc_ID', hover_name='Location', color=Col_Interest,
                           color_continuous_scale="Inferno",
                           range_color=(min(df[Col_Interest]), max(df[Col_Interest])),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": 136},
                           opacity=0.7,
                           labels={''})

fig.update_layout(margin={"r":0,"t":1,"l":0,"b":0}, coloraxis_colorbar={'title': Col_Interest})
fig.show()
fig.write_image("fig_test.png")

"""
'Location'
'Primary activities [male]2006'
'Primary activities [male]2011'
'Primary activities [male]2016'
'Primary activities [female]2006'
'Primary activities [female]2011'
'Primary activities [female]2016'
'Secondary activities [male with a job]2006'
'Secondary activities [male with a job]2011'
'Secondary activities [male with a job]2016'
'Secondary activities [female with a job]2006'
'Secondary activities [female with a job]2011'
'Secondary activities [female with a job]2016'
'Secondary activities [male without a job]2006'
'Secondary activities [male without a job]2011'
'Secondary activities [male without a job]2016'
'Secondary activities [female without a job]2006'
'Secondary activities [female without a job]2011'
'Secondary activities [female without a job]2016'
'Tertiary activities [male with a job]2006'
'Tertiary activities [male with a job]2011'
'Tertiary activities [male with a job]2016'
'Tertiary activities [female with a job]2006'
'Tertiary activities [female with a job]2011'
'Tertiary activities [female with a job]2016'
'Tertiary activities [male without a job]2006'
'Tertiary activities [male without a job]2011'
'Tertiary activities [male without a job]2016'
'Tertiary activities [female without a job]2006'
'Tertiary activities [female without a job]2011'
'Tertiary activities [female without a job]2016'
'Work [male with a job]2006'
'Work [male with a job]2011'
'Work [male with a job]2016'
'Work [female with a job]2006'
'Work [female with a job]2011'
'Work [female with a job]2016'
'Hobbies and amusements \n[male with a job]2006'
'Hobbies and amusements \n[male with a job]2011'
'Hobbies and amusements \n[male with a job]2016'
'Hobbies and amusements\n [female with a job]2006'
'Hobbies and amusements\n [female with a job]2011'
'Hobbies and amusements\n [female with a job]2016'
'Hobbies and amusements\n[male without a job]2006'
'Hobbies and amusements\n[male without a job]2011'
'Hobbies and amusements\n[male without a job]2016'
'Hobbies and amusements [female without a job]2006'
'Hobbies and amusements [female without a job]2011'
'Hobbies and amusements [female without a job]2016'
'T.V. , radio, newspapers and magazines\n[male with a job]2006'
'T.V. , radio, newspapers and magazines\n[male with a job]2011'
'T.V. , radio, newspapers and magazines\n[male with a job]2016'
'T.V. , radio, newspapers and magazines\n[female with a job]2006'
'T.V. , radio, newspapers and magazines\n[female with a job]2011'
'T.V. , radio, newspapers and magazines\n[female with a job]2016'
'T.V. , radio, newspapers and magazines\n[male without a job]2006'
'T.V. , radio, newspapers and magazines\n[male without a job]2011'
'T.V. , radio, newspapers and magazines\n[male without a job]2016'
'T.V. , radio, newspapers and magazines\n[female without a job]2006'
'T.V. , radio, newspapers and magazines\n[female without a job]2011'
'T.V. , radio, newspapers and magazines\n[female without a job]2016'
"""
