import matplotlib
import matplotlib.pyplot as pyplot
import glob
import re
import math
import pandas as pd

def _draw(ax, t):
    names, ticks = getData(t)
    ax.set_title({ "F": "float", "D":"double", "LD":"long double"}[t])
    ax.set_yscale("log")
    ax.scatter(names,ticks, s=300)
    ax.set_ylim(1e-2,1e1)
    ax.grid()

def mid(a):
    return sorted(a)[len(a)//2]

def toFloat(row):
    try:
        ptr = row["ptr"]
        if type(ptr) is float and math.isnan(ptr):
            return float('nan')
        print( "ptr is ", repr(ptr))
        p = int(ptr, 16)
        if p==0:
            return float('nan')
        return float(row["tick"])
    except ValueError:
        return float('nan')

def main(fn, kv, post):
    pyplot.style.use("ggplot")
    ytVals = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4]
    ytLabels = ["%.0e" % y for y in ytVals ]
    xtVals = range(0,33,4)
    ytLabels = ["%.0e" % y for y in ytVals ]
    z=5
    fig, axes = pyplot.subplots(nrows=1, ncols=1, figsize=(5*z, 3*z))
    ax = axes
    ax.set_yscale('log')
    ax.set_xlim([0,32])
    ax.set_ylim([ytVals[0], ytVals[len(ytVals)-1]])
    ax.set_yticks(ytVals, ytLabels, fontsize=8*z, fontname="Menlo")
    ax.set_xticks(xtVals, list(xtVals), fontsize=8*z, fontname="Menlo")
    axnum=0
    linestyles = ["solid", "dashed", "dotted"] + ["dotted"]*10
    for k in kv:
        ticks=[]
        for i in range(5):
            df = pd.read_csv(f"../res/{fn}_{k}_{post}_{i}.csv", encoding = "utf-8", names=['type', 'bits', 'tick', 'ptr'])
            for ix, row in df.iterrows():
                print( ix, row["bits"], row["tick"] )
                if len(ticks)<=ix:
                    ticks.append([])
                ticks[ix].append(toFloat(row))
        t = [ mid(ts) for ts in ticks ]
        ax.plot(t, lw=(10-axnum) * z/2, linestyle=linestyles[axnum] ,label=kv[k] )
        axnum+=1        
    ax.set_title(fn + "/" + post, fontsize=15*z)
    ax.legend(loc="upper left", fontsize=8*z)
    pyplot.tight_layout()
    pyplot.savefig(f"graph/{fn}_{post}.png")

# main(f"cpp_clang_n_rp64")

def cpp():
    for pc in ["macm1", "rp32", "rp64"]:
        for cc in (["clang"] if pc=="macm1" else ["gcc"]):
            m = {
                "c":"calloc",
                "m":"malloc",
                "v":"vec (ctor with size)",
                "r":"vec (reserve(size))",
                "s":"vec (resize(size))",
                "n":"new",
            }
            main(f"cpp_{cc}", m, pc)

def go():
    for pc in ["macm1", "rp32", "rp64"]:
        m = {
            "c":"capacity",
            "l":"length",
        }
        main(f"go", m, pc)

cpp()
go()
