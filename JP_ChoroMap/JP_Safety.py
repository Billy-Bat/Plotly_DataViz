



#1 LOAD EXCEL DATA
import pandas as pd
from unidecode import unidecode

# import raw name of columns
cols_raw = pd.read_excel('JP_FullData/Safety.xls', skiprows=8, nrows=1, usecols=lambda x: 'Unnamed' not in x,)
cols_raw = list(map(unidecode, cols_raw.columns))[1:]
cols_df = ['Location', 'NONE']
years = ['2010', '2015', '2017']
to_replace = ['(inhabitable area 100km^2)', '(per 100,000 persons)', '(per capita)', '(per 100 building fire cases)', '(per fire case)', '(per 1,000km of real length of roads)',
             '(per 100 traffic accidents)', '(per 1,000 persons)', '(per 1,000 persons of 14-19 years old)', '(per policy in force)', '(per household)', '(per 1,000 private households)',
             '(per recipient)', ]
for i in range(len(cols_raw)) :
    cols_raw[i] = cols_raw[i].replace('\n', '')
    for rep in to_replace :
        cols_raw[i] = cols_raw[i].replace(rep, '')
    for year in years :
        cols_df.append(cols_raw[i] + year)

df_raw = pd.read_excel('JP_FullData/Safety.xls', skiprows=12, usecols='J:FE', skipfooter=9, names=cols_df)
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

Col_Interest = 'Popularization of voluntary automobile insurance on property2017' # PUT HERE THE COLUMN TO DISPLAY ON MAP
#1 Set the column you want to display
cols = list(df_raw.columns)
cols.remove('Location')
cols.remove(Col_Interest) # PUT HERE THE COLUMN TO DISPLAY ON MAP
df = df_raw.drop(columns=cols)
df = df.drop(df.tail(2).index) # Dropping mean and SD

for row_id in df.index :
    df['Location'].iloc[row_id] = Mapper_NameId[df['Location'].iloc[row_id]]

# 2 Plot
import plotly.express as px
fig = px.choropleth_mapbox(df, geojson=prefs, locations='Location', color=Col_Interest,
                           color_continuous_scale="Inferno",
                           range_color=(min(df[Col_Interest]), max(df[Col_Interest])),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": 136},
                           opacity=0.5,
                           labels={''}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


""" COLS AVAL
Fire stations 2010
Fire stations 2015
Fire stations 2017
Fire fighting units and sub-units 2010
Fire fighting units and sub-units 2015
Fire fighting units and sub-units 2017
Fire engines and cars existing 2010
Fire engines and cars existing 2015
Fire engines and cars existing 2017
Water facilities for fire fighting 2010
Water facilities for fire fighting 2015
Water facilities for fire fighting 2017
Firemen in stations and units 2010
Firemen in stations and units 2015
Firemen in stations and units 2017
Firemen in stations 2010
Firemen in stations 2015
Firemen in stations 2017
Operation frequencies 2010
Operation frequencies 2015
Operation frequencies 2017
Operation frequencies for fire extinction 2010
Operation frequencies for fire extinction 2015
Operation frequencies for fire extinction 2017
Occurrences of fire 2010
Occurrences of fire 2015
Occurrences of fire 2017
Occurrences of building fires 2010
Occurrences of building fires 2015
Occurrences of building fires 2017
Persons killed or injured by fires 2010
Persons killed or injured by fires 2015
Persons killed or injured by fires 2017
Estimated value of loss by building fires 2010
Estimated value of loss by building fires 2015
Estimated value of loss by building fires 2017
Households suffered by fires 2010
Households suffered by fires 2015
Households suffered by fires 2017
Persons killed or injured by fires 2010.1
Persons killed or injured by fires 2015.1
Persons killed or injured by fires 2017.1
Estimated value of loss by building fires 2010.1
Estimated value of loss by building fires 2015.1
Estimated value of loss by building fires 2017.1
Elevated crossings 2010
Elevated crossings 2015
Elevated crossings 2017
Traffic accidents (per 1,000km real length of roads)2010
Traffic accidents (per 1,000km real length of roads)2015
Traffic accidents (per 1,000km real length of roads)2017
Traffic accidents 2010
Traffic accidents 2015
Traffic accidents 2017
Persons killed or injured by traffic accidents 2010
Persons killed or injured by traffic accidents 2015
Persons killed or injured by traffic accidents 2017
Persons killed by traffic accidents2010
Persons killed by traffic accidents2015
Persons killed by traffic accidents2017
Persons injured by traffic accidents2010
Persons injured by traffic accidents2015
Persons injured by traffic accidents2017
Persons killed or injured 2010
Persons killed or injured 2015
Persons killed or injured 2017
Persons killed 2010
Persons killed 2015
Persons killed 2017
Arrests for traffic violations 2010
Arrests for traffic violations 2015
Arrests for traffic violations 2017
Police men 2010
Police men 2015
Police men 2017
Recognitions of criminal offenses2010
Recognitions of criminal offenses2015
Recognitions of criminal offenses2017
Recognitions of larceny offenses 2010
Recognitions of larceny offenses 2015
Recognitions of larceny offenses 2017
Ratio of arrests to recognitions of criminal offenses2010
Ratio of arrests to recognitions of criminal offenses2015
Ratio of arrests to recognitions of criminal offenses2017
Ratio of arrests to recognitions of larceny offenses2010
Ratio of arrests to recognitions of larceny offenses2015
Ratio of arrests to recognitions of larceny offenses2017
Ratio of felonious offenses to recognitions of criminal offenses2010
Ratio of felonious offenses to recognitions of criminal offenses2015
Ratio of felonious offenses to recognitions of criminal offenses2017
Ratio of violent offenses to recognitions of criminal offenses2010
Ratio of violent offenses to recognitions of criminal offenses2015
Ratio of violent offenses to recognitions of criminal offenses2017
Ratio of larceny offenses to recognitions of criminal offenses2010
Ratio of larceny offenses to recognitions of criminal offenses2015
Ratio of larceny offenses to recognitions of criminal offenses2017
Ratio of moral offenses to recognitions of criminal offenses2010
Ratio of moral offenses to recognitions of criminal offenses2015
Ratio of moral offenses to recognitions of criminal offenses2017
Juvenile delinquent arrested for criminal offenses2010
Juvenile delinquent arrested for criminal offenses2015
Juvenile delinquent arrested for criminal offenses2017
Juvenile delinquent arrested for criminal larceny2010
Juvenile delinquent arrested for criminal larceny2015
Juvenile delinquent arrested for criminal larceny2017
Cases indicted for special criminal laws 2010
Cases indicted for special criminal laws 2015
Cases indicted for special criminal laws 2017
Cases indicted for drug law 2010
Cases indicted for drug law 2015
Cases indicted for drug law 2017
Value of damage by disasters 2010
Value of damage by disasters 2015
Value of damage by disasters 2017
Deaths by accidents 2010
Deaths by accidents 2015
Deaths by accidents 2017
Cases of grievances against pollution 2010
Cases of grievances against pollution 2015
Cases of grievances against pollution 2017
Private life insurance policies in force 2010
Private life insurance policies in force 2015
Private life insurance policies in force 2017
Amount insured by private life insurance 2010
Amount insured by private life insurance 2015
Amount insured by private life insurance 2017
Amount insured by private life insurance 2010.1
Amount insured by private life insurance 2015.1
Amount insured by private life insurance 2017.1
New fire insurance policies effected 2010
New fire insurance policies effected 2015
New fire insurance policies effected 2017
Cases of payments of fire insurance 2010
Cases of payments of fire insurance 2015
Cases of payments of fire insurance 2017
Amount insured by fire insurance 2010
Amount insured by fire insurance 2015
Amount insured by fire insurance 2017
Insurance paid by compulsory automobile liability insurance 2010
Insurance paid by compulsory automobile liability insurance 2015
Insurance paid by compulsory automobile liability insurance 2017
Popularization of voluntary automobile insurance on vehicles2010
Popularization of voluntary automobile insurance on vehicles2015
Popularization of voluntary automobile insurance on vehicles2017
Popularization of voluntary automobile insurance on persons2010
Popularization of voluntary automobile insurance on persons2015
Popularization of voluntary automobile insurance on persons2017
Popularization of voluntary automobile insurance on property2010
Popularization of voluntary automobile insurance on property2015
Popularization of voluntary automobile insurance on property2017
"""
