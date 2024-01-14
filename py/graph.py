import matplotlib
import matplotlib.pyplot as pyplot
import glob
import re
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

def toFloat(s):
    try:
        return float(s)
    except ValueError:
        return float('nan')

def main(fn):
    pyplot.style.use("ggplot")
    ytVals = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 1e1, 1e2]
    ytLabels = ["%.0e" % y for y in ytVals ]
    ticks=[]
    for i in range(5):
        df = pd.read_csv(f"../res/{fn}_{i}.csv", encoding = "utf-8", names=['type', 'bits', 'tick', 'ptr'])
        for ix, row in df.iterrows():
            print( ix, row["bits"], row["tick"] )
            if len(ticks)<=ix:
                ticks.append([])
            ticks[ix].append(row["tick"])
    t = [toFloat(e) for e in [ mid(ts) for ts in ticks ] ]
    print(t)
    z=5
    fig, axes = pyplot.subplots(nrows=1, ncols=1, figsize=(5*z, 3*z))
    for i in range(6):
        ax = axes
        ax.set_yscale('log')
        ax.plot(t, lw=z*3)

    ax.set_yticks(ytVals, ytLabels, fontsize=8*z, fontname="Menlo")
    ax.set_title(fn, fontsize=15*z)
    pyplot.tight_layout()
    pyplot.savefig(f"graph/{fn}.png")

# main(f"cpp_clang_n_rp64")

for pc in ["macm1", "rp32", "rp64"]:
    for cc in [ "clang", "gcc"]:
        for m in [ "c", "n", "v", "r","s", "m"]:
            main(f"cpp_clang_{m}_{pc}")


