#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  2 16:32:37 2025

@author: machine
"""


import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os

pd.options.mode.copy_on_write = True


id_blu = "C00401224"
id_bern = "C00696948"
id_biden = "C00703975"
id_kamala = "C00694455"
id_warren = "C00693234"


#%%

infile = "USA-sample.pkl"

sample = pd.read_pickle(infile)

cmte_id = sample["CMTE_ID"].value_counts()
other_id = sample["OTHER_ID"].value_counts()
#%%

is_bs = (sample["CMTE_ID"]==id_bern) | (sample["OTHER_ID"]==id_bern)

is_jb = (sample["CMTE_ID"]==id_biden) | (sample["OTHER_ID"]==id_biden)

is_kh = (sample["CMTE_ID"]==id_kamala) | (sample["OTHER_ID"]==id_kamala)

is_ew = (sample["CMTE_ID"]==id_warren) | (sample["OTHER_ID"]==id_warren)

sample = sample[is_bs | is_jb | is_kh | is_ew]

# Should show the number of True values
print(is_bs.sum())  
print(is_jb.sum())
print(is_kh.sum())
print(is_ew.sum())

#%%

# replacing all NA or nan with 0
sample.fillna(0, inplace=True)


# check the number of missing dates
whittle = sample[sample["TRANSACTION_DT"]!=0]


# changing the transaction date column to convert dates to datetime format
whittle["TRANSACTION_DT"] = pd.to_datetime(whittle["TRANSACTION_DT"], format="%m%d%Y")

# taking all contributrions made on or after June 8, 2016 out of the data
# boolean to keep only the conditions that are True (less than june 8)
whittle = whittle[whittle["TRANSACTION_DT"]<"2020-04-08"]

# taking all refunds out of the data
whittle = whittle[whittle["TRANSACTION_AMT"].astype(int)>0]

# checking to see how many in-kind donations (473)
inkind = whittle[whittle["MEMO_TEXT"].str.contains("IN-KIND", na=False)]

# removing in-kind donations from the data
# Remove rows where MEMO_TEXT contains "IN-KIND"
whittle = whittle[~whittle["MEMO_TEXT"].str.contains("IN-KIND", na=False)]

cmte_id = whittle["CMTE_ID"].value_counts()
other_id = whittle["OTHER_ID"].value_counts()
#%%


# Create a new empty column called "cand" 
whittle["cand"] = "unknown"

# loc = location (tells pandas what to change)
# putting names in 'cand'
whittle.loc[is_bs, "cand"] = 'bernie'

whittle.loc[is_jb, "cand"] = 'biden'

whittle.loc[is_kh, "cand"] = 'kamala'

whittle.loc[is_ew, "cand"] = 'warren'

# just picks out the left 5 characters in the zip column
whittle["zip5"]= whittle["ZIP_CODE"].str[:5]


#%%

# turning a string into a number
whittle["TRANSACTION_AMT"] = whittle["TRANSACTION_AMT"].astype(int)

# grouping these three columns
grouped = whittle.groupby(['NAME', 'zip5', 'cand'])

# just makes a new df to start putting columns in
byind = pd.DataFrame()

# count # of contribs by each person
byind["count"] = grouped.size()


byind["amt"] = grouped["TRANSACTION_AMT"].sum()

