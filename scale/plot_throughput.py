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
    "3P1M1D": ["por.db", "por2.db", "por3.db", "dispute.db", "marketmatch.db"],
    "chainboost": ["por.db"]
}

contacts = {"32K": 32, 
           "64K": 64,
           "128K": 128,
           "512K": 512}

normalizer = 3



def get_pandas_df(path):
    con = sqlite3.connect(path)
    df = pd.read_sql_query("Select * FROM RoundTable", con)

    con.close()
    return df

def plot(dataframedict):
        name = f"tp_scale.png"
        fig, ax = plt.subplots()
        ax.set_box_aspect(0.8)
        plt.rcParams['font.size'] = 22
        for item in ([ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(20)
        for key, value in dataframedict.items():
            plt.plot(value[0], [x/1000 for x in value[1]], marker=points[key], ms="10", label=key)
        plt.xlabel("No. of Contracts (x 1000)")
        plt.ylabel("(x1000) tx/s")
        fig.legend(loc="upper left", ncol=1, bbox_to_anchor=(0.5, 0.5), fontsize="x-small")
        plt.grid()
        plt.savefig(name, bbox_inches='tight')
        plt.show()


if __name__ == "__main__":
    dfdict = {i:[[],[]] for i in file_config.keys()}
    for mc, v in file_config.items():
        for sc in contacts.keys():
            print(f"{mc}_{sc}")
            mc_df = get_pandas_df(f"{mc}/{sc}/mainchain.db")[1:-1]
            mc_df.rename(columns=mc_cols, inplace=True)
            mc_mean = mc_df["Total Transactions"].mean()
            print (f">>>mc", mc_mean)
            for element in v:
                sc_df = get_pandas_df(f"{mc}/{sc}/{element}")[:-1]
                sc_df.rename(columns=sc_cols, inplace=True)
                print (f">>>{element}", sc_df["Total Transactions"].mean())
                mc_mean += normalizer * sc_df["Total Transactions"].mean()
            print(mc_mean)
            mc_mean /= 30
            dfdict[mc][0].append(contacts[sc])
            dfdict[mc][1].append(mc_mean)
    print(dfdict)
    plot(dfdict)