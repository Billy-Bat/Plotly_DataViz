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
        cols_df.append(cols_raw[i] + '\n' + year)

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
variable = 'Water facilities for fire fighting \n(per 100,000 persons)\n2010' # PUT HERE THE COLUMN TO DISPLAY ON MAP
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
ax.set_title(variable, fontsize='10')
ax.annotate('Source: Statistic Bureau of Japan 2019', xy=(0.1, 0.1),
            xycoords='figure fraction', horizontalalignment='left',
            verticalalignment='bottom', fontsize=6, color='#555555')
sm = plt.cm.ScalarMappable(cmap='Blues',
                           norm=plt.Normalize(vmin=min(df[variable]), vmax=max(df[variable])))
sm._A = []
cbar = fig.colorbar(sm)

plt.show()
