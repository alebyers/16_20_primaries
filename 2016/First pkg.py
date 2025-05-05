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


# read header
header=pd.read_csv("indiv_header_file.csv",dtype=str)
# chunk.columns = header.columns

# Change to False when reading entire raw (indiv16) file


##### uncomment to read entire raw (indiv16) file
# dtype=str tells pandas to not mess with leading zeros, or numbers in general

raw = pd.read_csv("indiv16/itcont.txt", dtype=str, sep="|", header=None)
raw.columns = header.columns
 
n_now = len(raw)
print("# of Records Read:", n_now, flush=True) 
raw.to_pickle("USA.pkl")
print("Building Sample", flush=True)
sample = raw.sample(frac=0.01)
sample.to_pickle("USA-sample.pkl")



#%%

nys = raw[raw["STATE"].str.strip()=="NY"]
    
nys.to_pickle("nys.pkl")

ny_cities = nys["CITY"].value_counts()

keepers = ['NEW YORK', 'NY', 'NYC', 'NEW YORK CITY', 'FLUSHING', 'JAMAICA', 
           'BROOKLYN', 'BRONX', 'STATEN ISLAND']

nyc = nys [nys["CITY"].isin(keepers)]

nyc.to_pickle("nyc.pkl")
