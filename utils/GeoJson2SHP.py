import geojson, subprocess
"""
WARNING : Calling shell script
"""

def geojson2shp(inputpath, outputpath) :
    args = ['ogr2ogr', '-f', 'ESRI Shapefile', outputpath, inputpath]
    subprocess.Popen(args, cwd='/Users/Liam/Desktop/plotly')
    subprocess.Popen(args)

    return 0


Ipath = 'utils/data.json'
Opath = 'Shp_Data/SHP.shp'

geojson2shp(Ipath, Opath)
