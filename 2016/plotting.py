#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  1 18:18:01 2025

@author: machine
"""

import geopandas as gpd
import matplotlib.pyplot as plt




trim = gpd.read_file("ByZip_Trim.gpkg", layer="zips")

trim=trim.to_crs(epsg=6350)

states = gpd.read_file("ByZip_Trim.gpkg", layer="states")

states=states.to_crs(epsg=6350)

#%% 


fig,ax=plt.subplots(dpi=400)



# This is incomplete
trim.plot("ratio", ax=ax, legend=True, cmap="RdYlGn")

states.boundary.plot(lw=.1, ax=ax, color="xkcd:periwinkle")

ax.axis("off")

# save fig
