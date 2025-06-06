#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 10:20:26 2025

@author: machine
"""

import pandas as pd


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

#%% Pulling the huge 2020 FEC data; linking header; stripping unused columns

# read header
head=pd.read_csv("indiv_header_file.csv",dtype=str)


# dtype=str tells pandas to not mess with leading zeros, or numbers in general
# Read the txt file, skipping bad lines
raw = pd.read_csv("indiv20/itcont.txt", dtype=str, sep="|", header=None, on_bad_lines='warn')

raw.columns = head.columns

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
