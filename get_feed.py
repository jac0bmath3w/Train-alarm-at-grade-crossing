#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 16:52:59 2019

@author: jacob
"""

    import json
    import time
    #import urllib2
    from requests.auth import HTTPBasicAuth
    from getpass import getpass
    import requests
    import pandas as pd
    import threading
    #from pandas import DataFrame 
    url = "https://gtfsapi.metrarail.com"
    path = "/gtfs/positions"
    accessKey = "xxxx"
    secretKey = "yyy"
    
def realtime_metra_feed():    
    threading.Timer(30.0, realtime_metra_feed).start()
    print("\n")
    print("Request sent at ", time.asctime(time.localtime(time.time())))
    print("\n")
    results = requests.get(url+path,auth=HTTPBasicAuth(accessKey,secretKey))
    data = results.json()
    data_df = pd.DataFrame(data)
    #print(data)
    required_data = []
    for i in range(len(data_df)):
        ind = data_df.id[i]
        latitude = data_df.vehicle[i]['position']['latitude']
        longitude = data_df.vehicle[i]['position']['longitude']
        #print(ind)
        #print(latitude)
        #print(longitude)
        required_data.append({'id':ind, 'latitude':latitude,'longitude':longitude})
    required_data = pd.DataFrame(required_data)
    #print(required_data.loc[required_data['id'] == 8547])
    train_geom = [Point(xy) for xy in zip (required_data['longitude'],required_data['latitude'])]
    train_df = gpd.GeoDataFrame(required_data, crs = crs, geometry = train_geom)
    train_df = train_df.to_crs(proj_crs)
#    train_df_buffer = train_df.buffer(distance = 500)
#    train_buffer_df = gpd.GeoDataFrame(train_df.id, geometry=train_df_buffer)
#    overlay = gpd.overlay(data_metra_lines_buffer_df, train_buffer_df, how = "union")
#    overlay.plot()
    sum = 0 
    #index_2 = []
    print("There are ", len(data)," trains available in the feed")
    for k, pt in enumerate(train_df.geometry):
            for j, poly in enumerate(crossings_reduced_buffer_df.geometry):
                if (pt.within(poly)):
                    print("Train %s is occupying Crossing %s buffer" %(train_df.id.iloc[k], crossings_reduced_buffer_df['CrossingID'].iloc[j]))  
                    sum+=1
                    break
    if sum == 0:
        print("There are no trains occupying any crossing buffer")
        
        
#start_time = time.asctime(time.localtime(time.time()))        
start_time = time.time()
end_time = start_time+30*60
t = threading.Timer(30.0, realtime_metra_feed)
t.start()
if (time.time() > end_time):
    t.cancel()
realtime_metra_feed()        
