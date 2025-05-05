#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 15:14:13 2025

@author: machine
"""


import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os


id_blu = "C00401224"
id_bern = "C00577130"
id_hill = "C00575795"


# JustNYC=pd.read_csv("nyc-zip-codes.csv",dtype=str)

# changing the name of the zip code column
# JustNYC = JustNYC.rename(columns={"ZipCode": "ZIP_CODE"})

# NYCD = raw.merge(JustNYC, how='left', on='ZIP_CODE', 
                       # validate='1:1', indicator=True)



#%% 

# sample.head()
# two_colmns = pd.read_csv("indiv16/intcont.txt", dtype=str, sep = "|", header=None, usecols= ['MEMO_CD','MEMO_TEXT'])



# t variable to takes sample and drops anything with 'nan' in column 19
# t = sample.dropna(subset=19)

# fills all nan across the dataframe (t) with a period "."
#t = sample.fillna(value=".")

# t variable is keeping only words "see below" in column 19 IF I get rid of the "or" aka |
# currently this code is to keep nans and "see belows" in col 19
#t = t[(t["MEMO_TEXT"].str.contains("SEE BELOW"))|(t["MEMO_TEXT"]==".")]



#%% renaming columns with a the header variable


#col_names = list(header.columns)

#dic = {}
#for i in range (0,21):
    #dic[i]= col_names[i]
#sample = sample.rename(columns=dic)

#t = t.rename(columns=dic)
#%%


infile = "nyc.pkl"

raw = pd.read_pickle(infile)

#%% REMOVING rows in the data

# # removing rows that have G2016 in column transaction_pgi
# # t = t[t["TRANSACTION_PGI"]!="G2016"]
# # sample = sample[sample["TRANSACTION_PGI"]!="G2016"]

# # dropping missing dates (there were only 11)
# t = t[t["TRANSACTION_DT"]!="."]
# # making a new column to convert dates to datetime format
# t["TRANSACTION_DTX"] = pd.to_datetime(t["TRANSACTION_DT"], format="%m%d%Y")

# sample = sample.fillna(".")


# # checked the number of missing dates
# sample_null = sample[sample["TRANSACTION_DT"]=="."]

# # dropping missing dates (there were only 13)
# sample = sample[sample["TRANSACTION_DT"]!="."]
# # making a new column to convert dates to datetime format
# sample["TRANSACTION_DT"] = pd.to_datetime(sample["TRANSACTION_DT"], format="%m%d%Y")

# sample_2016_6_8 = sample[sample["TRANSACTION_DT"]<"2016-06-08"]

# sample_P = sample[sample["TRANSACTION_PGI"]=="P2016"]
# sample_G = sample[sample["TRANSACTION_PGI"]=="G2016"]


# # values in the cmte_id column "is in" this list, then keep, otherwise they dump
# t = t[t["CMTE_ID"].isin(["C00401224", "C00575795", "C00577130"])]
# print(t["CMTE_ID"].value_counts())
# sample = sample[sample["CMTE_ID"].isin(["C00401224", "C00575795", "C00577130"])]


# sample["CMTE_ID"].value_counts()
# print(sample["CMTE_ID"].value_counts())

# comm_ids = raw["CMTE_ID"].value_counts()


#%% Taking all ActBlue account from C00401224 into one dataframe from original file

# id_blu is ActBlue and I could X this to do everyone in the whole file
# check for contribs of all else
## THIS PARCELS OUT ACTBLUE DONATIONS ONLY
###raw_ActB = raw[(raw["CMTE_ID"]==id_blu) | (raw["OTHER_ID"]==id_blu)]
###print(raw_ActB["CMTE_ID"].value_counts())

# Removing all Hillary contributions through ActBlue's df
# raw_ActHill = raw_ActB[raw_ActB["CMTE_ID"]=="C00575795"]

# keeping just Hillary & Bernie from ActB listed in CMTE_ID
# raw_ActAll = raw_ActB[raw_ActB["CMTE_ID"].isin(["C00575795", "C00577130"])]
# keeping just Hillary & Bernie from ActB listed in OTHER_ID
# raw_ActOther = raw_ActB[raw_ActB["OTHER_ID"].isin(["C00575795", "C00577130"])]


is_bs = (raw_ActB["CMTE_ID"]=="C00577130") | (raw_ActB["OTHER_ID"]=="C00577130")

is_hc = (raw_ActB["CMTE_ID"]=="C00575795") | (raw_ActB["OTHER_ID"]=="C00575795")

raw_ActAll = raw_ActB[is_bs | is_hc]

# raw_ActAll = raw_ActB[(raw_ActB["CMTE_ID"].isin(["C00575795", "C00577130"])) |
                       #  (raw_ActB["OTHER_ID"].isin(["C00575795", "C00577130"]))]

# checking to see how many zip codes have 5 vs 9 digits for map precision purposes
# ZipChk = raw_ActB[raw_ActB["ZIP_CODE"].str.len()==5]

# replacing all NA or nan with a period
raw_ActAll = raw_ActAll.fillna(".")


# check the number of missing dates
# raw_ActAll = raw_ActAll[raw_ActAll["TRANSACTION_DT"]=="."]

# changing the transaction date column to convert dates to datetime format
raw_ActAll["TRANSACTION_DT"] = pd.to_datetime(raw_ActAll["TRANSACTION_DT"], format="%m%d%Y")

raw_ActAll = raw_ActAll[raw_ActAll["TRANSACTION_DT"]<"2016-06-08"]

act1 = raw_ActAll[raw_ActAll["TRANSACTION_AMT"].astype(int)>0]

act1 = act1.copy()

# Created a new column that included H.C. & B.S. with their unique CMTE_ID or OTHER_ID numbers 
# act1["cand"] = act1.apply(lambda x:"H.C." if (x["CMTE_ID"]=="C00575795") | (x["OTHER_ID"]=="C00575795") else "B.S.", axis=1)

act1["cand"] = "unknown"

# loc = location (tells pandas what to change)
# only change rows that are bernie rows, then column to show said change is 'cand'
act1.loc[is_bs, "cand"] = 'bern'

act1.loc[is_hc, "cand"] = 'hill'

# just picks out the left 5 characters in the zip column
act1["zip5"]= act1["ZIP_CODE"].str[:5]




#%%

read in zip code shapefiles
read in county shape files
pickout zip codes that intersect with counties

a bunchn of zips in NYCD
Then join data by zip code for mapping



#%%

# zip_all = act1["ZIP_CODE"]

# # This makes a series w/ length, in characters, of each zip code.
# ## .str tells Pandas to apply string operation. Then .len() to apply len
# ###  which I thought len was giving a number of records?
# ziplen = zip_all.str.len()

# zip_9 = ziplen == 9

# zip_5 = ziplen == 5

# zip_ok = zip_5 | zip_9

# zip_bad = ~ zip_ok

# zip5 = zip_all.copy()

# # The .str telling Pandas to read the zip as a string. the :5 selects 
# ## the 1st 5 characters from the string
# zip5[zip_9] = zip5[zip_9].str[:5]

# # marks missing data
# zip5[zip_bad] = None

# zip5len = zip5.str.len()
# print("Zip Codes in 5:")
# print(zip5len.value_counts(dropna=False))

# ACT1['zip'] = zip5

#%%

# turning a string into a number
act1["TRANSACTION_AMT"] = act1["TRANSACTION_AMT"].astype(int)

# grouping these three columns
grouped = act1.groupby(['NAME', 'zip5', 'cand'])

# just makes a new df to start putting columns in
byind = pd.DataFrame()

# count # of contribs by each person
byind["count"] = grouped.size()


byind["amt"] = grouped["TRANSACTION_AMT"].sum()







#%% ALL ELSE

# new df from raw that *does not include* act blue. pulling act blue's unique ID out of the mix
rawNAB = raw[(raw["CMTE_ID"]!="C00401224") & (raw["OTHER_ID"]!="C00401224")]


# using same df to keep only hillary & bernie's unique IDs in either column CMTE_ID or OTHER_ID
rawNAB = rawNAB[(rawNAB["CMTE_ID"].isin(["C00575795", "C00577130"])) |
                        (rawNAB["OTHER_ID"].isin(["C00575795", "C00577130"]))]




# RENAME EVERYTING!!!!

# replacing all NA or nan with 0
rawNAB.fillna(0, inplace=True)


# check the number of missing dates
rawMX = rawNAB[rawNAB["TRANSACTION_DT"]!=0]


# changing the transaction date column to convert dates to datetime format
rawNAB["TRANSACTION_DT"] = pd.to_datetime(rawNAB["TRANSACTION_DT"], format="%m%d%Y")

# taking all contributrions made on or after June 8, 2016 out of the data
# boolean to keep only the conditions that are True (less than june 8)
raw68 = rawNAB[rawNAB["TRANSACTION_DT"]<"2016-06-08"]

# taking all refunds out of the data
raw68 = raw68[raw68["TRANSACTION_AMT"].astype(int)>0]

# checking to see how many in-kind donations (473)
inkind = raw68[raw68["MEMO_TEXT"].str.contains("IN-KIND", na=False)]

# removing in-kind donations from the data
# Remove rows where MEMO_TEXT contains "IN-KIND"
raw68 = raw68[~raw68["MEMO_TEXT"].str.contains("IN-KIND", na=False)]


# renaming, if need be
# ACT1 = rawActB_2016_6_8


# Created a new column that included H.C. & B.S. with their unique CMTE_ID or OTHER_ID numbers 
raw68["CAND"] = raw68.apply(lambda x:"H.C." if (x["CMTE_ID"]=="C00575795") |
                            (x["OTHER_ID"]=="C00575795") else "B.S.", axis=1)


rawzip = raw68["ZIP_CODE"]


# This makes a series w/ length, in characters, of each zip code.
## .str tells Pandas to apply string operation. 
###  Then .len() to apply length of characters
rziplen = rawzip.str.len()

rzip_9 = rziplen == 9

rzip_5 = rziplen == 5

rzip_ok = rzip_5 | rzip_9

rzip_bad = ~ rzip_ok
# print(len(rzip5), len(rzip_bad))

rzip5 = rawzip.copy()

# The .str telling Pandas to read the zip as a string. the :5 selects 
## the 1st 5 characters from the string
rzip5[rzip_9] = rzip5[rzip_9].str[:5]

# if length of line is >5 extract 1st 5 numbers:
# BYERS
# index 0 = B
# index 1 = Y 
# index 2 = E 
# line = line[0:4]

# marks missing data
rzip5[rzip_bad] = None

rzip5len = rzip5.str.len()
print("Zip Codes in 5:")
print(rzip5len.value_counts(dropna=False))

raw68['zip'] = rzip5





raw68["TRANSACTION_AMT"] = raw68["TRANSACTION_AMT"].astype(int)
# grouping these three columns
grouped68 = raw68.groupby(['NAME', 'zip', 'OCCUPATION', 'CAND'])

raw_b_zip = grouped68["TRANSACTION_AMT"].sum().reset_index()







#%%



# ASSIGN TO NEW DF & new variable names
# bringing together 
ATG = pd.concat([contrib_by_zip, raw_b_zip])


# groupby ATG by Zip to use for visualizations
ATGZ = ATG.groupby(['zip', 'CAND'])["TRANSACTION_AMT"].sum().reset_index()

# Total Contributions for HC & BS
s = ATGZ["TRANSACTION_AMT"].sum()

# Total contribution for each candidate sh = hillary, sb = bernie
sh = ATGZ.groupby('CAND')["TRANSACTION_AMT"].sum()


# each individual donor to Hill or Bern
si = ATG.groupby('CAND')["NAME"].count()

# altogether file with Z zip Occupation O Name N & C Candidate
ATG.to_csv("Altogether_ZONC.csv")




QZ = ATG[ATG['zip']=="00000"]




NYCZ=pd.read_csv("nyc-zip-codes.csv",dtype=str)


#  Specifying columns to merge and how to merge them. 
## This is a left merge with the index being STATEFP and COUNTYFP.
merge1 = NYCZ.merge(ATGZ,left_on="ZipCode",right_on="zip", how="left")

# for QGIS (w/ out names)
merge1.to_csv("NYC_W_Out_Names.csv")


merge2 = NYCZ.merge(ATG, left_on="ZipCode",right_on="zip", how="left")


merge2.to_csv("NYC_Altogether_ZONC.csv")




#%% I DON'T KNOW WHAT TO DO WITH ANYTHING BELOW THIS LINE RN


# renaming column in raw variable/data/csv file
raw = raw.rename(columns={"TRANSACTION_Primary_Contrib":"PGI"})
# creating a new column in raw variable/data/csv file (no idea re: astype float)
raw["amt"] = raw["TRANSACTION_AMT"].astype(float)

# ymd (year month day) to MMDDYYYY
ymd = pd.to_datetime(raw["TRANSACTION_DT"], format="%m%d%Y")

# creating a new column that takes just the month of the date for grouping by M later
raw["date"] = ymd.dt.to_period("M")

n_last = n_now
year_ok = ymd.dt.year >=2015
date_bad = (ymd.dt.year == 2016)&(ymd.dt.month > 7)
keep = year_ok & (date_bad==False)
print("New # of Records:", n_last)



# creating a new dataframe called contrib. Filters out contributions from earlier years
contrib = raw[keep]

x=contrib["NAME"].str.contains("BYERS")
b=contrib[x]
                               
# len gives the number of records (from the contrib dataframe)
n_now = len(contrib)


## sorting contrib by the column "PGI"
contrib = contrib.sort_values("PGI")
print()


## notice that the state FIPS code MUST be quoted
pcontrib = contrib.query("PGI == 'P'")

print(nys)

print("# of Records Dropped:", n_last-n_now)

# again...not sure why
n_last = n_now
# taking out records from primary elections in 2020
contrib = contrib.query("PGI == 'P2020', 'P'")

# .drop drops whatever you write in front of it. // .dropna drops missing data
by_month = by_month.drop(columns=["total"])


attain = pd.read_csv("census-data.csv", index_col="NAME")

# transposing data
## TIP: to get groupby() to apply to columns...
##  Pandas only allows groupby to be applied to rows, so to aggregate the columns 
##   in attain it will be necessary to transpose attain (swap the rows and columns), 
##    do the aggregation, and then transpose the result back.
attain_tr = attain.T



by_level.to_csv("by_level.csv")

n_now = len(contrib)

print("# of Records from Primary & General 2020:", n_last-n_now)
print("Total # of Records:", n_now)


#%% Making a new variable and printing a total number of said variable

keepvars = ['CMTE_ID', 'STATE', 'ZIP_CODE', 'PGI', 'date','amt']
# new variable = the keepvars column of contrib
trimmed = contrib[keepvars]
# pickling!
trimmed.to_pickle('contrib_all_pkl.zip')

print("# of Records Trimmed:")
print(len(trimmed))
print("Verifying Correct Variables in Trimming?:")
print(list(trimmed.columns))




#%% Building a figure showing the pattern of contributions over time

# grouping the trimmed column by date & PGI?
grouped = trimmed.groupby(["date","PGI"])
# using variable = taking money from the grouped variable in column "amt"...
by_date_pgi = grouped["amt"].sum()/1e6

#unstacking the data by creating separate columns btwn pri & gen election $$
by_date_wide = by_date_pgi.unstack("PGI")

# The making of a figure steps:
fig1, ax1 = plt.subplots(dpi=300)
# Title
fig1.suptitle("Individual Contributions")

by_date_wide.plot(ax=ax1)

ax1.set_ylabel("Million Dollars")
ax1.set_xlabel("Date")

fig1.tight_layout() 
fig1.savefig("by_month.png")




#%%




# getting zip file from the contrib_all (different file/assignment in same folder)
contrib = pd.read_pickle('contrib_all_pkl.zip')

zip_all = contrib["ZIP_CODE"]

# This makes a series w/ length, in characters, of each zip code.
## .str tells Pandas to apply string operation. Then .len() to apply len
###  which I thought len was giving a number of records?
ziplen = zip_all.str.len()

print("Table of Zip Code Lengths")
print(ziplen.value_counts(dropna=False))

zip_9 = ziplen == 9

zip_5 = ziplen == 5

zip_ok = zip_5 | zip_9

zip_bad = ~ zip_ok

zip5 = zip_all.copy()

# The .str telling Pandas to read the zip as a string. the :5 selects 
## the 1st 5 characters from the string
zip5[zip_9] = zip5[zip_9].str[:5]

# marks missing data
zip5[zip_bad] = None

zip5len = zip5.str.len()
print("Zip Codes in 5:")
print(zip5len.value_counts(dropna=False))

contrib['zip'] = zip5

# grouping these three columns
grouped = contrib.groupby(['CMTE_ID', 'STATE', 'zip'])

contrib_by_zip = grouped["amt"].sum()
contrib_by_zip.to_csv("contrib_by_zip.csv")







#%% 2020 primary code to filter and sort



n_last = n_now
year_ok = ymd.dt.year >=2019
date_bad = (ymd.dt.year == 2020)&(ymd.dt.month > 3)
keep = year_ok & (date_bad==False)



# creating a new dataframe called contrib. Filters out contributions from earlier years
contrib = raw[keep]

x=contrib["NAME"].str.contains("BYERS")
b=contrib[x]
                               
# len gives the number of records (from the contrib dataframe)
n_now = len(contrib)


## sorting contrib by the column "PGI"
contrib = contrib.sort_values("PGI")
print()


## notice that the state FIPS code MUST be quoted
pcontrib = contrib.query("PGI == 'P'")

print(nys)

print("# of Records Dropped:", n_last-n_now)

# again...not sure why
n_last = n_now
# taking out records from primary elections in 2020
contrib = contrib.query("PGI == 'P2020', 'P'")

# .drop drops whatever you write in front of it. // .dropna drops missing data
by_month = by_month.drop(columns=["total"])


attain = pd.read_csv("census-data.csv", index_col="NAME")

# transposing data
## TIP: to get groupby() to apply to columns...
##  Pandas only allows groupby to be applied to rows, so to aggregate the columns 
##   in attain it will be necessary to transpose attain (swap the rows and columns), 
##    do the aggregation, and then transpose the result back.
attain_tr = attain.T



by_level.to_csv("by_level.csv")

n_now = len(contrib)

print("# of Records from Primary & General 2020:", n_last-n_now)
print("Total # of Records:", n_now)

