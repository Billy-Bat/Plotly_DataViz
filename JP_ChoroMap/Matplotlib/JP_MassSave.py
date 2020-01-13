import geopandas as gpd
import pandas as pd
import xlsxwriter
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import os
from os.path import isfile, join
from unidecode import unidecode

# LOAD shp files
map_df = gpd.read_file('Shp_Data/SHP.shp')

files = [f for f in os.listdir('JP_FullData') if isfile(join('JP_FullData', f))]
try :
    os.mkdir('JP_ChoroMap/Matplotlib/figs')
except :
    print('Fig Directory Creation Failed')

cmaps = ['Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
         'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
          'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

for cmap_id, file in enumerate(files) :

    fp = 'JP_FullData/' + file
    sample_row = pd.read_excel(fp, skiprows=35, nrows=1)
    lastcol_ID = xlsxwriter.utility.xl_col_to_name(sample_row.shape[1]-2)
    sample_col = pd.read_excel(fp, usecols='K')
    last_rowID = sample_col.shape[0]

    cols_raw = pd.read_excel(fp, skiprows=8, nrows=1, usecols=lambda x: 'Unnamed' not in x,)
    cols_raw = list(map(unidecode, cols_raw.columns))[1:]

    cols_df = ['Location', 'NONE']
    years = ['2010', '2015', '2017']
    for i in range(len(cols_raw)) :
        for year in years :
            cols_df.append(cols_raw[i] + '\n' + year)


    df_raw = pd.read_excel(fp, skiprows=12, nrows=47, usecols='J:'+lastcol_ID, names=cols_df)
    df_raw.drop(df_raw.columns[1], axis=1, inplace=True)

    for row_id in df_raw.index :
        df_raw['Location'].iloc[row_id] = df_raw['Location'].iloc[row_id].replace('-ken', '')
        df_raw['Location'].iloc[row_id] = df_raw['Location'].iloc[row_id].replace('-to', '')
        df_raw['Location'].iloc[row_id] = df_raw['Location'].iloc[row_id].replace('-fu', '')
        df_raw['Location'].iloc[row_id] = df_raw['Location'].iloc[row_id].lower()
        if df_raw['Location'].iloc[row_id] == 'gumma' : # Spelling not consistent
            df_raw['Location'].iloc[row_id] = 'gunma'

    try :
        for variable in cols_df :
            if (variable == 'Location') | (variable == 'NONE') :
                continue
            # Create the directories
            try :
                os.mkdir('JP_ChoroMap/Matplotlib/figs/' + file)
            except :
                print('SubDirectory Creation Failed')

            cols = list(df_raw.columns)
            cols.remove('Location')
            cols.remove(variable) # PUT HERE THE COLUMN TO DISPLAY ON MAP
            df = df_raw.drop(columns=cols)
            df = df.drop(df.tail(2).index) # Dropping mean and SD

            # Create The Map
            merged = map_df.set_index('name').join(df.set_index('Location'))

            fig, ax = plt.subplots(1, figsize=(10, 6))
            merged.plot(column=variable, cmap=cmaps[cmap_id], linewidth=0.8, ax=ax, edgecolor='0.8')
            ax.axis('off')
            ax.set_title(variable, fontsize='10')
            ax.annotate('Source: Statistic Bureau of Japan 2019', xy=(0.1, 0.1),
                        xycoords='figure fraction', horizontalalignment='left',
                        verticalalignment='bottom', fontsize=6, color='#555555')
            sm = plt.cm.ScalarMappable(cmap=cmaps[cmap_id],
                                       norm=plt.Normalize(vmin=min(df[variable]), vmax=max(df[variable])))
            sm._A = []
            cbar = fig.colorbar(sm)
            title = variable.replace(' ', '')
            title = title.replace('(', '')
            title = title.replace(')', '')
            title = title.replace(r'\n', '')

            plt.savefig('JP_ChoroMap/Matplotlib/figs/' + file + '/' + title + '.png')
    except :
        print('FAILED at col : ' + variable + ' in file : ' + file)
