import json, geojson, subprocess
"""
WARNING : Calling shell script
"""

def geojson2shp(inputpath, outputpath,) :
    args = ['ogr2ogr', '-f', 'ESRI Shapefile', outputpath, inputpath]
    subprocess.Popen(args, cwd='/Users/Liam/Desktop/plotly')
    subprocess.Popen(args)

    return 0

def pickle2json(inputpath, outputpath=None):
    import pickle
    import json

    with open(inputpath, 'rb') as file :
        jsonfile = pickle.load(file)
    if outputpath==None :
        return jsonfile
    else :
        with open(outputpath, 'w') as OutFile :
            json.dump(jsonfile, OutFile)

def translatePrefNames(DicObject, RemoveSuffix=True) :
    import pykakasi
    Suffixs = [r'\u770c', r'\u5e9c', r'\u90fd']

    kakasi = pykakasi.kakasi()
    kakasi.setMode("J","a")
    conv = kakasi.getConverter()

    for key in DicObject :
        if type(DicObject[key]) == list :
            for sub_dic in DicObject[key] :
                for sub_keys in sub_dic :
                    if type(sub_dic[sub_keys]) == dict :
                        for Ssub_key in sub_dic[sub_keys] :
                            if Ssub_key == 'name' :
                                sub_dic[sub_keys][Ssub_key] = sub_dic[sub_keys]['name_english'].lower()
                                # # replace suffix
                                # for suf in Suffixs :
                                #     sub_dic[sub_keys][Ssub_key] == sub_dic[sub_keys][Ssub_key].replace(suf, '')
                                # sub_dic[sub_keys][Ssub_key] = conv.do(sub_dic[sub_keys][Ssub_key])

    return DicObject


RPath = 'JP_ChoroMap/Data.pckl'
Ipath = 'utils/data.json'
Opath = 'Shp_Data/SHP.shp'

geodata = pickle2json(RPath)
geodata = translatePrefNames(geodata)
with open(Ipath, 'w') as f :
    json.dump(geodata, f)

geojson2shp(Ipath, Opath)
