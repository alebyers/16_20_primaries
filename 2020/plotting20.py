#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  1 18:18:01 2025

@author: machine
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd



trim = gpd.read_file("USA_primaries.gpkg", layer="2020")


states = gpd.read_file("clipt_zips.gpkg", layer="states")



#%% 

names = {"BB": "Biden", "BK": "Kamala", "BW": "Warren", "PB": "Pete", "all": "All"}

for comp in ["BB", "BK", "BW", "PB", "all"]:
    fig,ax=plt.subplots(dpi=600) 
    fig.suptitle(names[comp])
    trim.plot(f"ratio_{comp}", ax=ax, legend=True, cmap="RdYlGn") 
    states.boundary.plot(lw=.1, ax=ax, color="xkcd:periwinkle") 
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(f"2020_Dem_Primaries{comp}.png")
    


#%% Building a figure showing the pattern of contributions over time

byzip=pd.read_pickle("byzip.zip")

byzip = byzip.reset_index()


groups = byzip.groupby("cand")

totals = groups[['indi', 'count', 'amt']].sum()

names = {'indi': "Individual Contributors", 'count': "Number of Contributions",
         'amt': "Total Dollars Contributed"}

for v in ['indi', 'count', 'amt']:
    fig1, ax1 = plt.subplots(dpi=300)
    fig1.suptitle(names[v])
    totals[v].plot(kind="bar", ax=ax1)
    ax1.set_xlabel("By Candidate")
    fig1.tight_layout() 
    fig1.savefig(f"fig_{v}.png")


