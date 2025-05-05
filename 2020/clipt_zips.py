#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  5 08:30:17 2025

@author: machine
"""

import geopandas as gpd


borders = gpd.read_file("cb_2020_us_state_500k.zip")

borders = borders.query("STATEFP<'57'")

extent = borders.total_bounds

print("reading zips", flush=True)

geo = gpd.read_file("cb_2019_us_zcta510_500k.zip", bbox=tuple(extent))

print("reprojecting zips", flush=True)

geo=geo.to_crs(epsg=6350)

print("saving zips", flush=True)

geo.to_file("clipt_zips.gpkg", layer="zips")

borders=borders.to_crs(epsg=6350)

borders.to_file("clipt_zips.gpkg", layer="states")

