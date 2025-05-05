#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 10:20:26 2025

@author: machine
"""

import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os


# 1st download candidate master list+header: https://www.fec.gov/data/browse-data/?tab=bulk-data
# upload header
head=pd.read_csv("cn_header_file.csv",dtype=str)

# open zip of candidate master to then open the .txt file
cand = 'cn.txt'
cand = pd.read_csv("cn.txt", dtype=str, sep="|", header=None)
# attaching the header to the cand df
cand.columns = head.columns
# keeping only candidates with the following names
who = cand[cand["CAND_NAME"].str.contains("SANDERS, BERNARD") 
           |cand["CAND_NAME"].str.contains("WARREN, ELIZABETH")
           |cand["CAND_NAME"].str.contains("KAMALA")
           |cand["CAND_NAME"].str.contains("BIDEN")
           |cand["CAND_NAME"].str.contains("BUTTIGIEG")]

#%% 

# read header
header=pd.read_csv("indiv_header_file.csv",dtype=str)
# chunk.columns = header.columns

# Change to False when reading entire raw (indiv20) file


##### uncomment to read entire raw (indiv20) file
# dtype=str tells pandas to not mess with leading zeros, or numbers in general

# Read the txt file, skipping bad lines
raw = pd.read_csv("indiv20/itcont.txt", dtype=str, sep="|", header=None, on_bad_lines='warn')


# raw = pd.read_csv("indiv20/itcont.txt", dtype=str, sep="|", header=None)
raw.columns = header.columns

keepers = ["CMTE_ID", "TRANSACTION_PGI", "NAME", "CITY", "STATE", "ZIP_CODE", 
           "EMPLOYER", "OCCUPATION", "TRANSACTION_DT", "TRANSACTION_AMT", 
           "OTHER_ID", "MEMO_CD", "MEMO_TEXT"]

raw = raw[keepers]

 
n_now = len(raw)
print("# of Records Read:", n_now, flush=True) 
raw.to_pickle("USA.zip")
print("Building Sample", flush=True)
sample = raw.sample(frac=0.01)
sample.to_pickle("USA-sample.pkl")



#%%

nys = raw[raw["STATE"].str.strip()=="NY"]
    
nys.to_pickle("nys.pkl")

ny_cities = nys["CITY"].value_counts()

keepers = ['NEW YORK', 'NY', 'NYC', 'NEW YORK CITY', 'FLUSHING', 'JAMAICA', 
           'BROOKLYN', 'BRONX', 'STATEN ISLAND', 'QUEENS', 'MANHATTAN', 'THE BRONX']

nyc = nys [nys["CITY"].isin(keepers)]

nyc.to_pickle("nyc.pkl")
