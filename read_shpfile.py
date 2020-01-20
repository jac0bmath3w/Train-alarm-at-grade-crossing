# -*- coding: utf-8 -*-
%matplotlib inline
import geopandas as gpd
import pandas as pd
#https://towardsdatascience.com/geopandas-101-plot-any-data-with-a-latitude-and-longitude-on-a-map-98e01944b972
from shapely.geometry import Point, Polygon
from shapely.geometry import shape
import geoplot as gplt
import geoplot.crs as gcrs
from geopandas.tools import sjoin
import matplotlib.pyplot as plt
from pyproj import Proj, transform
#from rtree import index


#Import Metra Shapefile
#Downloaded from https://data.cityofchicago.org/widgets/q8wx-dznq
data_metra_lines = gpd.read_file('./Metra_20Lines/MetraLinesshp.shp')
#Convert to WGS84 Coordinate System
crs = {'init': 'epsg:4326'}
proj_crs = {'init':'epsg:26971'}
data_metra_lines = data_metra_lines.to_crs(proj_crs)
data_metra_lines_buffer = data_metra_lines.buffer(distance = 50)
data_metra_lines_buffer_df = gpd.GeoDataFrame(
    data_metra_lines['ASSET_ID'], geometry=data_metra_lines_buffer)


#Not sure what this line is
#data_metra_df = gpd.GeoDataFrame.from_file('./Metra_20Lines/MetraLinesshp.shp')

#This came from Metra.R
crossings = pd.read_csv('Filtered_ICC_CollarCounties.csv')
geometry = [Point(xy) for xy in zip (crossings['Longitude'],crossings['Latitude'])]
crossings_df = gpd.GeoDataFrame(crossings, crs = crs, geometry = geometry)
crossings_df = crossings_df.to_crs(proj_crs)
#data_metra_lines.head(3)


#poly_kwargs = {'linewidth': 0.5, 'edgecolor': 'gray', 'zorder': -1}
#point_kwargs = {'linewidth': 0.5, 'edgecolor': 'black', 'alpha': 1}
#ax1 = gplt.pointplot(crossings_df, projection=gcrs.AlbersEqualArea(), **point_kwargs)
#fig, ax1 = plt.subplots()
#ax1.set_aspect('equal')
#ax1 = data_metra_lines.plot(edgecolor='black')
#crossings_df.plot(ax=ax1, marker='o')
#gplt.polyplot(data_metra_lines_buffer, projection=gcrs.AlbersEqualArea(), **poly_kwargs)


sum = 0 
index = []
for i, pt in enumerate(crossings_df.geometry):
    if (i not in index):
        #print(i)
        #print(index)
        for j, poly in enumerate(data_metra_lines_buffer):
            #print(pt.within(poly))
            if (pt.within(poly)):
                sum+=1
                index.append(i)
                break
    else:
        continue
        

print(sum)
print(index)

crossings_reduced_df = gpd.GeoDataFrame(crossings_df['CrossingID'][index],
                                        crs = proj_crs, geometry = crossings_df.geometry[index])
crossings_reduced_buffer = crossings_reduced_df.buffer(distance = 50)
crossings_reduced_buffer_df = gpd.GeoDataFrame(
    crossings_reduced_df['CrossingID'][index], geometry=crossings_reduced_buffer)



