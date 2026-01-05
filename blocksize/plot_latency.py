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
    "1P1M1D": ["por.db", "dispute.db", "marketmatch.db"],
    "2P1M1D": ["por.db", "por2.db", "dispute.db", "marketmatch.db"],
    "chainboost": ["por.db"]
}

contacts = [0.5, 1.0, 1.5, 2.0]

normalizer = 3



def get_pandas_df(path):
    print(path)
    con = sqlite3.connect(path)
    df = pd.read_sql_query("Select * FROM RoundTable", con)

    con.close()
    return df

def plot(dataframedict):
        name = f"lat_blocksize.png"
        fig, ax = plt.subplots()
        ax.set_box_aspect(0.8)
        plt.rcParams['font.size'] = 22
        for item in ([ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(20)
        for key, value in dataframedict.items():
            plt.plot(value[0], [x/1000 for x in value[1]], marker=points[key], ms="10", label=key)
        plt.xlabel("Sidechain block size (MB)")
        plt.ylabel("Confirmation Time (x1000s)")
        fig.legend(loc="upper left", ncol=1, bbox_to_anchor=(0.56, 0.9), fontsize="x-small")
        plt.grid()
        plt.savefig(name, bbox_inches='tight')
        plt.show()


if __name__ == "__main__":
    dfdict = {i:[[],[]] for i in file_config.keys()}
    for mc, v in file_config.items():
        for sc in contacts:
            sc_mean = 0
            for element in v:
                sc_df = get_pandas_df(f"{mc}/{sc}/{element}")[:-1]
                sc_df.rename(columns=sc_cols, inplace=True)
                df = sc_df[sc_df["Total Transactions"]%30 != 0]
                mean = df["Confirmation Time"].mean()
                print(f"{sc}-{mc}-{element}: Lat: {mean} - {mean * 30/normalizer}" )
                sc_mean += mean
            sc_mean /= len(v)
            sc_mean *= 30/normalizer
            dfdict[mc][0].append(sc)
            dfdict[mc][1].append(sc_mean)
    print(dfdict)
    plot(dfdict)