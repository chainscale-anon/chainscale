import matplotlib.pyplot as plt
import csv 
import sys
import sqlite3
import pandas as pd
import numpy as np

mc_cols = {"RegPayTx" : "Pay Transactions", "PoRTx" : "PoR Transactions", "StorjPayTx" : "Storage Payment Transactions",
 "CntPropTx" : "Proposition Transactions", "CntCmtTx" : "Commitment Transactions", "TotalNumTx" : "Total Transactions", "ConfirmationTime": "Confirmation Time"}

sc_cols = {"PoRTx": "Total Transactions", "AveWait": "Confirmation Time"}


colours ={"1P1M1D" : "red", "2P1M1D" : "blue", "3P1M1D": "brown", "chainboost": "orange",}

lines ={"1P1M1D" : "solid", "2P1M1D" : "dashed", "3P1M1D": "dotted", "chainboost": "orange",}

points = {"1P1M1D" : "o", "2P1M1D" : "v", "3P1M1D": "X", "chainboost": "*",}


#points = {"chainboost" : "circle", "no-chainboost" : "triangle"}

#lines = {"chainboost" : "solid", "no-chainboost" : "dotted"}

file_config = {
    "128-CS": ["por.db", "dispute.db", "marketmatch.db"],
   # "128-CS--": ["por.db", "dispute.db", "marketmatch.db"],
    "128-sharding": ["shard0.db", "shard1.db", "shard2.db", "shard3.db"],
}

normalizer = 3



def get_pandas_df(path):
    print(path)
    con = sqlite3.connect(path)
    df = pd.read_sql_query("Select * FROM RoundTable", con)

    con.close()
    return df

def get_pandas_ctr_df(path):
    print(path)
    con = sqlite3.connect(path)
    df = pd.read_sql_query("Select * FROM CTR", con)

    con.close()
    return df

def plot(dataframedict):
        name = f"tp_blocksize.png"
        fig = plt.figure()
        plt.rcParams.update({'font.size': 14})
        for key, value in dataframedict.items():
            plt.plot(value[0], value[1], marker=points[key], ms="10", label=key.replace("chainboost", "cb"))
        plt.xlabel("Sidechain block size (MB)")
        plt.ylabel("Confirmation Time (s)")
        fig.legend(loc="outside upper center", ncol=4)
        plt.grid()
        plt.savefig(name, bbox_inches='tight')
        plt.show()


if __name__ == "__main__":
    dfdict = {i:[[],[]] for i in file_config.keys()}
    for mc, v in file_config.items():
        if mc == "128-sharding":
            mc_mean = 0
            for element in v: 
                path = f"{mc}/{element}"
                mc_df = get_pandas_df(path)[:-1]
                mc_df.rename(columns=mc_cols, inplace=True)
                mean = mc_df["Confirmation Time"].mean()
                print (f"\t {element} - {mean} - {mean * 30}")
                mc_mean += mc_df["Confirmation Time"].mean()
            mc_mean *= 30
            mc_mean /= 4
            print(f"{mc}: tput = {mc_mean}, ctr =0")
        else:
            mc_mean = 0
            print(f"{mc}: ")
            mc_df = get_pandas_df(f"{mc}/mainchain.db")[1:-1]
            mc_df.rename(columns=mc_cols, inplace=True)
            mc_mean = mc_df["Confirmation Time"].mean()
            print (f"\t MC - {mc_mean} - {mc_mean * 30}")
            sc_mean = 0
            for element in v:
                sc_df = get_pandas_df(f"{mc}/{element}")[:-1]
                sc_df.rename(columns=sc_cols, inplace=True)
                sc_df = sc_df[sc_df["Total Transactions"]%30 != 0]
                mean = sc_df["Confirmation Time"].mean()
                print (f"\t {element} - {mean} - {mean * 10}")
                sc_mean += mean
            sc_mean *= 10
            mc_mean *= 30
            print(f"{mc}: tput = {mc_mean} , {sc_mean/3}, {(mc_mean+sc_mean)/4}, ctr =0")