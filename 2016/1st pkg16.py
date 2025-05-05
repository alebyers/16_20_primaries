#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 10:20:26 2025

@author: machine
"""

import pandas as pd


# 1st download candidate master list+header: https://www.fec.gov/data/browse-data/?tab=bulk-data
# read header
head=pd.read_csv("indiv_header_file.csv",dtype=str)
# chunk.columns = header.columns

# open zip of candidate master to then open the .txt file
cand = 'cn.txt'
cand = pd.read_csv("cn.txt", dtype=str, sep="|", header=None)
# attaching the header to the cand df
cand.columns = head.columns
# keeping only candidates with the following names
who = cand[cand["CAND_NAME"].str.contains("SANDERS, BERNARD") 
           |cand["CAND_NAME"].str.contains("CLINTON, HILLARY")]


# dtype=str tells pandas to not mess with leading zeros, or numbers in general
# opening a .txt file and putting the information in a new df called raw
# then attaching the head (header file above) to raw
raw = pd.read_csv("indiv16/itcont.txt", dtype=str, sep="|", header=None)
raw.columns = head.columns

# reading & printing the length of raw, pkl'n it, pulling a 1% sample, pikl'n it too
n_now = len(raw)
print("# of Records Read:", n_now, flush=True) 
raw.to_pickle("USA.pkl")
print("Building Sample", flush=True)
sample = raw.sample(frac=0.01)
sample.to_pickle("USA-sample.pkl")



#%% Pulling NY State out of df "raw"
#     then pulling NYC + its boroughs out & pkl'n 'em

nys = raw[raw["STATE"].str.strip()=="NY"]
    
nys.to_pickle("nys.pkl")

ny_cities = nys["CITY"].value_counts()

keepers = ['NEW YORK', 'NY', 'NYC', 'NEW YORK CITY', 'FLUSHING', 'JAMAICA', 
           'BROOKLYN', 'BRONX', 'STATEN ISLAND']

nyc = nys [nys["CITY"].isin(keepers)]

nyc.to_pickle("nyc.pkl")

