#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 14:14:14 2025

@author: machine
"""


import pandas as pd
import geopandas as gpd

# stops warnings if adding columns to a df where rows are deleted
pd.options.mode.copy_on_write=True


id_blu =    "C00401224"
id_bern =   "C00696948"
id_pete =   "C00697441"
id_biden =  "C00703975"
id_kamala = "C00694455"
id_warren = "C00693234"

raw = pd.read_pickle("USA.zip")

altog = raw.fillna("")

#%%


# check the number of missing dates

year = altog["TRANSACTION_DT"].str[-4:]
is_okay = year.isin(["2019", "2020"])

altog = altog[is_okay]


# changing the transaction date column to convert dates to datetime format
altog["TRANSACTION_DT"] = pd.to_datetime(altog["TRANSACTION_DT"], format="%m%d%Y")

dateok = altog["TRANSACTION_DT"]<"2020-04-08"
print("Original # of Recs:", len(altog))
print("Contribs btwn 2019 and April 7, 2020:", dateok.sum())

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
print(f"Bernie contribs: {is_bs.sum():,d}")

is_ew = (altog["CMTE_ID"]==id_warren) | (altog["OTHER_ID"]==id_warren)
print(f"Warren contribs: {is_ew.sum():,d}")

is_pb = (altog["CMTE_ID"]==id_pete) | (altog["OTHER_ID"]==id_pete)
print(f"Pete contribs: {is_pb.sum():,d}")

is_jb = (altog["CMTE_ID"]==id_biden) | (altog["OTHER_ID"]==id_biden)
print(f"Biden contribs: {is_jb.sum():,d}")

is_kh = (altog["CMTE_ID"]==id_kamala) | (altog["OTHER_ID"]==id_kamala)
print(f"Kamala contribs: {is_kh.sum():,d}")


#%%


altogdems = altog[is_bs | is_jb | is_kh | is_ew | is_pb]

altogdems["cand"] = "unknown"

# loc = location (tells pandas what to change)
# putting names of candidates in 'cand'
altogdems.loc[is_bs, "cand"] = 'bernie'

altogdems.loc[is_pb, "cand"] = 'pete'

altogdems.loc[is_jb, "cand"] = 'biden'

altogdems.loc[is_kh, "cand"] = 'kamala'

altogdems.loc[is_ew, "cand"] = 'warren'


#%% Prep for whittle down to individuals

# just picks out the left 5 characters in the zip column
altogdems["zip5"]= altogdems["ZIP_CODE"].str[:5]

# turning a string into a number
altogdems["TRANSACTION_AMT"] = altogdems["TRANSACTION_AMT"].astype(int)

# grouping these three columns 
grp_indi = altogdems.groupby(['NAME', 'zip5', 'cand'])

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

byzip.to_pickle("byzip.zip")

#%% Prep for GIS/maps visuals

# "pivoting" the right most column in the index for a 2-level
# (the columns are a list of tuples to Python -- byzip.columns)
byzip = byzip.unstack()

byzip = byzip.fillna(0)

# flattens the 2-level index (new_cols)
new_cols = byzip.columns.map('_'.join)

byzip.columns = new_cols

byzip = byzip.reset_index()

geo = gpd.read_file("clipt_zips.gpkg")

#%% Attaching and mapping via individual contributors and their location


geo = geo.merge(byzip, left_on='ZCTA5CE10', right_on='zip5',
                how="outer", indicator=True, validate="1:1")

is_mapable = geo["_merge"]!="right_only"

not_mapable = geo[~is_mapable]

geo = geo[is_mapable]

geo = geo.drop(columns="_merge")

geo["ratio_BB"]= geo["indi_bernie"]/(geo["indi_bernie"]+ geo["indi_biden"])

geo["ratio_BW"]= geo["indi_bernie"]/(geo["indi_bernie"]+ geo["indi_warren"])

geo["ratio_PB"]= geo["indi_bernie"]/(geo["indi_bernie"]+ geo["indi_pete"])

geo["ratio_BK"]= geo["indi_bernie"]/(geo["indi_bernie"]+ geo["indi_kamala"])


geo["ratio_all"]= geo["indi_bernie"]/(geo["indi_bernie"]+geo["indi_biden"] 
                                      + geo["indi_kamala"] + geo["indi_warren"] + geo["indi_pete"])


geo.to_file("USA_primaries.gpkg", layer="2020")


