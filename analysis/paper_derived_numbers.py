"""Recompute every number in the paper that is not copied directly from a results file.
Run from the repository root:  python analysis/paper_derived_numbers.py"""
import glob
import json

import numpy as np
import pandas as pd

V1 = "results/v1"
V2 = "results/v2"


def holm(p):
    p = p.sort_values()
    m = len(p)
    adj = np.maximum.accumulate([min(1.0, (m - i) * v) for i, v in enumerate(p)])
    return dict(zip(p.index, np.round(adj, 4)))


sm = pd.read_csv(f"{V2}/results/summary_table.csv").set_index("model")
ps = pd.read_csv(f"{V2}/results/per_subject_r.csv").set_index("test_subject")
runs = pd.read_csv(f"{V2}/results/all_runs.csv")
runs["pearson_r"] = pd.to_numeric(runs.pearson_r, errors="coerce")

print("Holm, r > 0 (6 models):", holm(sm.p_vs_zero))
print("Holm, vs SupCon paired t:", holm(sm.p_vs_ref_ttest.dropna()))
print("Holm, vs SupCon Wilcoxon:", holm(sm.p_vs_ref_wilcoxon.dropna()))
print("r^2 of mean r:", (sm.r_mean ** 2).round(4).to_dict())
print("SD across subjects:", sm.r_sd.round(3).to_dict())
print("Ridge > SupCon in subjects:", int((ps.ridge > ps.transformer_supcon).sum()))
print("SupCon > no-SupCon in subjects:", int((ps.transformer_supcon > ps.transformer_nocon).sum()))
print("Negative for every model:", list(ps.index[(ps < 0).all(axis=1)]))
print("Examples sub-17 / sub-08:", ps.loc[["sub-17", "sub-08"]].round(3).to_dict("index"))
print("Undefined r (v2):", runs[runs.pearson_r.isna()][["model", "seed", "test_subject"]].values.tolist())
v1runs = pd.read_csv(f"{V1}/results/all_runs.csv")
print("Undefined r (v1):", int(pd.to_numeric(v1runs.pearson_r, errors="coerce").isna().sum()))
print("Ridge alpha counts:", runs[runs.model == "ridge"].alpha.value_counts().to_dict())
print("Median training / validation windows:", runs[runs.model == "mlp"][["n_train", "n_val"]].median().to_dict())
print("Selection counts:", runs.dropna(subset=["selected"]).groupby(["model", "selected"]).size().to_dict())

for base, models in [(V2, ["ridge", "mlp", "transformer_nocon", "transformer_supcon"]), (V1, ["labram_scratch"])]:
    for m in models:
        ratios = []
        for f in glob.glob(f"{base}/runs/{m}/seed*/fold*.npz"):
            with open(f, "rb") as fh, np.load(fh) as z:
                ratios.append(float(z["y_pred"].std() / z["y_true"].std()))
        print(f"pred SD / true SD, {m}: median {np.median(ratios):.3f} over {len(ratios)} runs")

d = json.load(open(f"{V1}/results/data_summary.json"))
s = pd.DataFrame(d["sessions"]).T
for c in ["n_channels_recorded", "n_channels_interpolated", "n_cuts_bridged", "n_cuts_inexact", "n_windows"]:
    x = pd.to_numeric(s[c])
    print(f"{c}: min {x.min()} max {x.max()} median {x.median()} sum {x.sum()}")
print("Sessions with 0 windows:", list(s.index[pd.to_numeric(s.n_windows) == 0]))
