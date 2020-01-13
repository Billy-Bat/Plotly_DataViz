import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# LOAD shp files
map_df = gpd.read_file('Shp_Data/SHP.shp')
# map_df.plot()

#1 LOAD EXCEL DATA
import pandas as pd
from unidecode import unidecode

# import raw name of columns
cols_raw = pd.read_excel('JP_FullData/Safety.xls', skiprows=8, nrows=1, usecols=lambda x: 'Unnamed' not in x,)
cols_raw = list(map(unidecode, cols_raw.columns))[1:]
cols_df = ['Location', 'NONE']
years = ['2010', '2015', '2017']
for i in range(len(cols_raw)) :
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


###################################CREATE MAP###################################
variable = 'Water facilities for fire fighting \n(per 100,000 persons)2010' # PUT HERE THE COLUMN TO DISPLAY ON MAP
#1 Set the column you want to display
cols = list(df_raw.columns)
cols.remove('Location')
cols.remove(variable) # PUT HERE THE COLUMN TO DISPLAY ON MAP
df = df_raw.drop(columns=cols)
df = df.drop(df.tail(2).index) # Dropping mean and SD

# Create The Map
merged = map_df.set_index('name').join(df.set_index('Location'))


fig, ax = plt.subplots(1, figsize=(10, 6))
merged.plot(column=variable, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')
ax.axis('off')
plt.show()


# """ COLS AVAL
# 'Location'
# 'Fire stations \n(inhabitable area 100km^2)2010'
# 'Fire stations \n(inhabitable area 100km^2)2015'
# 'Fire stations \n(inhabitable area 100km^2)2017'
# 'Fire fighting units and sub-units \n(inhabitable area 100km^2)2010'
# 'Fire fighting units and sub-units \n(inhabitable area 100km^2)2015'
# 'Fire fighting units and sub-units \n(inhabitable area 100km^2)2017'
# 'Fire engines and cars existing \n(per 100,000 persons)2010'
# 'Fire engines and cars existing \n(per 100,000 persons)2015'
# 'Fire engines and cars existing \n(per 100,000 persons)2017'
# 'Water facilities for fire fighting \n(per 100,000 persons)2010'
# 'Water facilities for fire fighting \n(per 100,000 persons)2015'
# 'Water facilities for fire fighting \n(per 100,000 persons)2017'
# 'Firemen in stations and units \n(per 100,000 persons)2010'
# 'Firemen in stations and units \n(per 100,000 persons)2015'
# 'Firemen in stations and units \n(per 100,000 persons)2017'
# 'Firemen in stations (per 100,000 persons)2010'
# 'Firemen in stations (per 100,000 persons)2015'
# 'Firemen in stations (per 100,000 persons)2017'
# 'Operation frequencies \n(per 100,000 persons)2010'
# 'Operation frequencies \n(per 100,000 persons)2015'
# 'Operation frequencies \n(per 100,000 persons)2017'
# 'Operation frequencies for fire extinction \n(per 100,000 persons)2010'
# 'Operation frequencies for fire extinction \n(per 100,000 persons)2015'
# 'Operation frequencies for fire extinction \n(per 100,000 persons)2017'
# 'Occurrences of fire (per 100,000 persons)2010'
# 'Occurrences of fire (per 100,000 persons)2015'
# 'Occurrences of fire (per 100,000 persons)2017'
# 'Occurrences of building fires (per 100,000 persons)2010'
# 'Occurrences of building fires (per 100,000 persons)2015'
# 'Occurrences of building fires (per 100,000 persons)2017'
# 'Persons killed or injured by fires\n (per 100,000 persons)2010'
# 'Persons killed or injured by fires\n (per 100,000 persons)2015'
# 'Persons killed or injured by fires\n (per 100,000 persons)2017'
# 'Estimated value of loss by building fires \n(per capita)2010'
# 'Estimated value of loss by building fires \n(per capita)2015'
# 'Estimated value of loss by building fires \n(per capita)2017'
# 'Households suffered by fires \n(per 100 building fire cases)2010'
# 'Households suffered by fires \n(per 100 building fire cases)2015'
# 'Households suffered by fires \n(per 100 building fire cases)2017'
# 'Persons killed or injured by fires \n(per 100 building fire cases)2010'
# 'Persons killed or injured by fires \n(per 100 building fire cases)2015'
# 'Persons killed or injured by fires \n(per 100 building fire cases)2017'
# 'Estimated value of loss by building fires \n(per fire case)2010'
# 'Estimated value of loss by building fires \n(per fire case)2015'
# 'Estimated value of loss by building fires \n(per fire case)2017'
# 'Elevated crossings \n(per 1,000km of real length of roads)2010'
# 'Elevated crossings \n(per 1,000km of real length of roads)2015'
# 'Elevated crossings \n(per 1,000km of real length of roads)2017'
# 'Traffic accidents (per 1,000km real length of roads)2010'
# 'Traffic accidents (per 1,000km real length of roads)2015'
# 'Traffic accidents (per 1,000km real length of roads)2017'
# 'Traffic accidents (per 100,000 persons)2010'
# 'Traffic accidents (per 100,000 persons)2015'
# 'Traffic accidents (per 100,000 persons)2017'
# 'Persons killed or injured by traffic accidents (per 100,000 persons)2010'
# 'Persons killed or injured by traffic accidents (per 100,000 persons)2015'
# 'Persons killed or injured by traffic accidents (per 100,000 persons)2017'
# 'Persons killed by traffic accidents\n(per 100,000 persons)2010'
# 'Persons killed by traffic accidents\n(per 100,000 persons)2015'
# 'Persons killed by traffic accidents\n(per 100,000 persons)2017'
# 'Persons injured by traffic accidents\n(per 100,000 persons)2010'
# 'Persons injured by traffic accidents\n(per 100,000 persons)2015'
# 'Persons injured by traffic accidents\n(per 100,000 persons)2017'
# 'Persons killed or injured \n(per 100 traffic accidents)2010'
# 'Persons killed or injured \n(per 100 traffic accidents)2015'
# 'Persons killed or injured \n(per 100 traffic accidents)2017'
# 'Persons killed (per 100 traffic accidents)2010'
# 'Persons killed (per 100 traffic accidents)2015'
# 'Persons killed (per 100 traffic accidents)2017'
# 'Arrests for traffic violations (per 1,000 persons)2010'
# 'Arrests for traffic violations (per 1,000 persons)2015'
# 'Arrests for traffic violations (per 1,000 persons)2017'
# 'Police men (per 1,000 persons)2010'
# 'Police men (per 1,000 persons)2015'
# 'Police men (per 1,000 persons)2017'
# 'Recognitions of criminal offenses\n(per 1,000 persons)2010'
# 'Recognitions of criminal offenses\n(per 1,000 persons)2015'
# 'Recognitions of criminal offenses\n(per 1,000 persons)2017'
# 'Recognitions of larceny offenses \n(per 1,000 persons)2010'
# 'Recognitions of larceny offenses \n(per 1,000 persons)2015'
# 'Recognitions of larceny offenses \n(per 1,000 persons)2017'
# 'Ratio of arrests to recognitions of criminal offenses2010'
# 'Ratio of arrests to recognitions of criminal offenses2015'
# 'Ratio of arrests to recognitions of criminal offenses2017'
# 'Ratio of arrests to recognitions of larceny offenses2010'
# 'Ratio of arrests to recognitions of larceny offenses2015'
# 'Ratio of arrests to recognitions of larceny offenses2017'
# 'Ratio of felonious offenses to recognitions of \ncriminal offenses2010'
# 'Ratio of felonious offenses to recognitions of \ncriminal offenses2015'
# 'Ratio of felonious offenses to recognitions of \ncriminal offenses2017'
# 'Ratio of violent offenses to recognitions of \ncriminal offenses2010'
# 'Ratio of violent offenses to recognitions of \ncriminal offenses2015'
# 'Ratio of violent offenses to recognitions of \ncriminal offenses2017'
# 'Ratio of larceny offenses to recognitions of criminal offenses2010'
# 'Ratio of larceny offenses to recognitions of criminal offenses2015'
# 'Ratio of larceny offenses to recognitions of criminal offenses2017'
# 'Ratio of moral offenses to recognitions of \ncriminal offenses2010'
# 'Ratio of moral offenses to recognitions of \ncriminal offenses2015'
# 'Ratio of moral offenses to recognitions of \ncriminal offenses2017'
# 'Juvenile delinquent arrested for criminal offenses\n(per 1,000 persons of 14-19 years old)2010'
# 'Juvenile delinquent arrested for criminal offenses\n(per 1,000 persons of 14-19 years old)2015'
# 'Juvenile delinquent arrested for criminal offenses\n(per 1,000 persons of 14-19 years old)2017'
# 'Juvenile delinquent arrested for criminal larceny\n(per 1,000 persons of 14-19 years old)2010'
# 'Juvenile delinquent arrested for criminal larceny\n(per 1,000 persons of 14-19 years old)2015'
# 'Juvenile delinquent arrested for criminal larceny\n(per 1,000 persons of 14-19 years old)2017'
# 'Cases indicted for special criminal laws \n(per 100,000 persons)2010'
# 'Cases indicted for special criminal laws \n(per 100,000 persons)2015'
# 'Cases indicted for special criminal laws \n(per 100,000 persons)2017'
# 'Cases indicted for drug law \n(per 100,000 persons)2010'
# 'Cases indicted for drug law \n(per 100,000 persons)2015'
# 'Cases indicted for drug law \n(per 100,000 persons)2017'
# 'Value of damage by disasters (per capita)2010'
# 'Value of damage by disasters (per capita)2015'
# 'Value of damage by disasters (per capita)2017'
# 'Deaths by accidents (per 100,000 persons)2010'
# 'Deaths by accidents (per 100,000 persons)2015'
# 'Deaths by accidents (per 100,000 persons)2017'
# 'Cases of grievances against pollution \n(per 100,000 persons)2010'
# 'Cases of grievances against pollution \n(per 100,000 persons)2015'
# 'Cases of grievances against pollution \n(per 100,000 persons)2017'
# 'Private life insurance policies in force \n(per 1,000 persons)2010'
# 'Private life insurance policies in force \n(per 1,000 persons)2015'
# 'Private life insurance policies in force \n(per 1,000 persons)2017'
# 'Amount insured by private life insurance \n(per policy in force)2010'
# 'Amount insured by private life insurance \n(per policy in force)2015'
# 'Amount insured by private life insurance \n(per policy in force)2017'
# 'Amount insured by private life insurance \n(per household)2010'
# 'Amount insured by private life insurance \n(per household)2015'
# 'Amount insured by private life insurance \n(per household)2017'
# 'New fire insurance policies effected \n(per 1,000 private households)2010'
# 'New fire insurance policies effected \n(per 1,000 private households)2015'
# 'New fire insurance policies effected \n(per 1,000 private households)2017'
# 'Cases of payments of fire insurance \n(per 1,000 private households)2010'
# 'Cases of payments of fire insurance \n(per 1,000 private households)2015'
# 'Cases of payments of fire insurance \n(per 1,000 private households)2017'
# 'Amount insured by fire insurance \n(per policy in force)2010'
# 'Amount insured by fire insurance \n(per policy in force)2015'
# 'Amount insured by fire insurance \n(per policy in force)2017'
# 'Insurance paid by compulsory automobile \nliability insurance (per recipient)2010'
# 'Insurance paid by compulsory automobile \nliability insurance (per recipient)2015'
# 'Insurance paid by compulsory automobile \nliability insurance (per recipient)2017'
# 'Popularization of voluntary automobile \ninsurance on vehicles2010'
# 'Popularization of voluntary automobile \ninsurance on vehicles2015'
# 'Popularization of voluntary automobile \ninsurance on vehicles2017'
# 'Popularization of voluntary automobile \ninsurance on persons2010'
# 'Popularization of voluntary automobile \ninsurance on persons2015'
# 'Popularization of voluntary automobile \ninsurance on persons2017'
# 'Popularization of voluntary automobile \ninsurance on property2010'
# 'Popularization of voluntary automobile \ninsurance on property2015'
# 'Popularization of voluntary automobile \ninsurance on property2017'
# """
