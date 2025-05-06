#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 14:14:14 2025

@author: machine
"""


import pandas as pd
import geopandas as gpd


pd.options.mode.copy_on_write=True



id_blu = "C00401224"
id_bern = "C00577130"
id_hill = "C00575795"


raw = pd.read_pickle("USA.pkl")
# raw = pd.read_pickle(infile)

altog = raw.fillna("")

# check the number of missing dates
year = altog["TRANSACTION_DT"].str[-4:]
is_okay = year.isin(["2015", "2016"])

altog = altog[is_okay]

# changing the transaction date column to convert dates to datetime format
altog["TRANSACTION_DT"] = pd.to_datetime(altog["TRANSACTION_DT"], format="%m%d%Y")

dateok = altog["TRANSACTION_DT"]<"2016-06-08"
print("Original # of Recs:", len(altog))
print("Contribs btwn 2015 and June 7, 2016:", dateok.sum())

altog = altog[dateok]
 
not_refunds = altog["TRANSACTION_AMT"].astype(int)>0
print("Positive Contribs:", not_refunds.sum())

altog = altog[not_refunds]

# removing in-kind donations from the data
# Remove rows where MEMO_TEXT contains "IN-KIND"
# altog = altog[~inkind]
# checking to see how many in-kind donations
inkind = altog[altog["MEMO_TEXT"].str.contains("IN-KIND", na=False)]
altog = altog[~altog["MEMO_TEXT"].str.contains("IN-KIND", na=False)]


is_bs = (altog["CMTE_ID"]==id_bern) | (altog["OTHER_ID"]==id_bern)
print("Bernie contribs:", is_bs.sum())

is_hc = (altog["CMTE_ID"]==id_hill) | (altog["OTHER_ID"]==id_hill)
print("Hillary contribs:", is_hc.sum())

altog = altog[is_bs | is_hc]

# Created a new column that included H.C. & B.S. with their unique CMTE_ID or OTHER_ID numbers 
# act1["cand"] = act1.apply(lambda x:"H.C." if (x["CMTE_ID"]=="C00575795") | (x["OTHER_ID"]=="C00575795") else "B.S.", axis=1)

altog["cand"] = "unknown"

# loc = location (tells pandas what to change)
# only change rows that are bernie rows, then column to show said change is 'cand'
altog.loc[is_bs, "cand"] = 'bern'

altog.loc[is_hc, "cand"] = 'hill'

#%% Prep for whittle down to individuals

# just picks out the left 5 characters in the zip column
altog["zip5"]= altog["ZIP_CODE"].str[:5]

# turning a string into a number
altog["TRANSACTION_AMT"] = altog["TRANSACTION_AMT"].astype(int)

# grouping these three columns into new df "grp_indi"
grp_indi = altog.groupby(['NAME', 'zip5', 'cand'])

# just makes a new df to start putting columns in
indi = pd.DataFrame()

# count # of contribs by each person
indi["count"] = grp_indi.size()

indi["amt"] = grp_indi["TRANSACTION_AMT"].sum()

#%%

grp_zips = indi.groupby(["zip5", 'cand'])

byzip = pd.DataFrame()

# counting # of ppl in each zip
byzip["indi"]=grp_zips.size()

byzip["count"]=grp_zips["count"].sum()

byzip["amt"]=grp_zips["amt"].sum()

#%% Prep for GIS visuals

# "pivoting" the right most column in the index for a 2-level
# (the columns are a list of tuples to Python -- byzip.columns)
byzip = byzip.unstack()

byzip = byzip.fillna(0)

# flattens the 2-level index (new_cols)
new_cols = byzip.columns.map('_'.join)

byzip.columns = new_cols

byzip.to_csv("byzip.csv")

#%% Attaching zip code shapefile with individual contributions ratio btwn Bernie & Hillary

byzip = byzip.reset_index()

geo = gpd.read_file("cb_2019_us_zcta510_500k.zip")

geo = geo.merge(byzip, left_on='ZCTA5CE10', right_on='zip5',
                how="outer", indicator=True, validate="1:1")

is_mapable = geo["_merge"]!="right_only"

not_mapable = geo[~is_mapable]

geo = geo[is_mapable]

geo["ratio"]= geo["indi_bern"]/(geo["indi_hill"]+geo["indi_bern"])

geo = geo.drop(columns="_merge")

geo.to_file("USA_Primaries.gpkg", layer="2016")


#%% Using Census state shapefile to have state borders on USA_Primaries layer 

borders = gpd.read_file("cb_2019_us_state_500k.zip")

borders = borders.query("STATEFP<'57'")

dis = borders.dissolve()

trim = geo.clip(dis, keep_geom_type=True)

trim.to_file("ByZip_Trim.gpkg", layer="zips")

borders.to_file("ByZip_Trim.gpkg", layer="states")



