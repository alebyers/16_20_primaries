#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 15:09:58 2025

@author: machine
"""

import geopandas as gpd

# reading in Census shapefiles
zips = gpd.read_file("tl_2016_us_zcta510.zip")

counties = gpd.read_file("tl_2016_us_county.zip")

nycgeo = ["36047", "36061", "36081", "36085", "36005"]

nyc = counties[counties["GEOID"].isin(nycgeo)]

#  nyc.plot()

nyc_dis = nyc.dissolve()

nyc = nyc.to_crs(26918)

zips = zips.to_crs(26918)

nyc_dis = nyc_dis.to_crs(26918)

select = zips.clip(nyc_dis, keep_geom_type=True)

# select.plot()

zips_cent = select.copy()
zips_cent['geometry'] = zips.centroid

zips_cent = zips_cent.sjoin(nyc, predicate="intersects", how="left")


select.to_file("nyc-zips.gpkg", layer="zips")

nyc.to_file("nyc-zips.gpkg", layer="counties")

zips_cent.to_file("nyc-zips.gpkg", layer="centroids")


