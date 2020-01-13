import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

map_df = gpd.read_file('Shp_Data/SHP.shp')
map_df.plot()
plt.show()
