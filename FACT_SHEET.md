# Fact sheet: where every number in the paper comes from

Paths are relative to the repository root.
- **v1** = `results/v1` (original settings; also preprocessing, HRF-alpha, LaBraM-style).
- **v2** = `results/v2` (nested candidate search, final results).
- **derived** = recomputed by `analysis/paper_derived_numbers.py` from the v1/v2 files.

## Data and preprocessing (v1 `results/data_summary.json`, code `notebooks/EEG2DMN_UnifiedLOSO_v1.ipynb`)
| Paper text | Value | Source |
|---|---|---|
| Subjects / sessions | 22 / 40 | data_summary.json `n_subjects`, `n_sessions` |
| Volumes per session, TR, EEG rate | 288, 2.1 s, 250 Hz | data_summary.json `n_vols_fmri`; code `TR`, sampling-rate check |
| Channels retained per session | 45–61 | derived (`n_channels_recorded`) |
| Union channel list / features | 61 / 305 | `n_channels`, `n_features_per_volume` |
| Sessions with interpolated channels, median | 37 of 40, median 3 | `sessions_with_channels_interpolated`; derived |
| DMN / FPN parcels, atlas check | 24 / 13, passed | code `DMN_IDX`, `FPN_IDX`; `atlas_label_check` |
| Gaps bridged / inexact | 752 / 158 | derived (`n_cuts_bridged`, `n_cuts_inexact`) |
| Session without data | sub-05 ses-01 | derived |
| Windows total / exact / per subject | 5,107 / 2,077 / 73–455 | `n_windows_total`, `n_windows_exact`, `windows_per_subject` |
| Bands, Welch settings, window 10, lag 3 TR, 5 bins, λ 0.5, τ 0.1, batch 64, 50 epochs, patience 10 | — | code Cell 1 (v1) and Cell 1 (v2) |

## Model selection (v2)
| Paper text | Value | Source |
|---|---|---|
| Candidate settings and parameter counts | Table I | `results/candidate_grids.json`, `results/parameter_counts.json` |
| Selection counts | Table I | `results/selection_counts.csv` |
| Median training / validation windows | 4,200 / 678 | derived (`all_runs.csv`) |
| Ridge penalty chosen | 10^5 ×20, 10^6 ×2 | `selection_counts.csv` |
| LaBraM-style parameters | 548,226 | v1 `results/parameter_counts.json` |
| Undefined-r runs | 2 (v2), 7 (v1) | derived |

## Main results (v2 `results/summary_table.csv`, `stats_vs_transformer_supcon.json`)
| Model | r ± SD | r>0 | p(r>0) | p vs SupCon t / W | MSE |
|---|---|---|---|---|---|
| Ridge | 0.082 ± 0.132 | 15 | 0.009 | 0.007 / 0.011 | 0.904 |
| MLP | 0.057 ± 0.112 | 15 | 0.028 | 0.027 / 0.033 | 0.954 |
| HRF-alpha | 0.056 ± 0.137 | 13 | 0.070 | 0.067 / 0.113 | — |
| LaBraM-style | −0.025 ± 0.095 | 10 | 0.231 | 0.623 / 0.210 | 0.908 |
| Transformer, no SupCon | −0.019 ± 0.102 | 9 | 0.388 | 0.728 / 0.899 | 0.953 |
| Transformer + SupCon | −0.014 ± 0.088 | 11 | 0.478 | — | 0.982 |

"r, defaults" column comes from v1 `results/summary_table.csv`: 0.085, 0.077, 0.056, −0.025, −0.016, −0.009.

## Other numbers in the text
| Paper text | Value | Source |
|---|---|---|
| Holm-adjusted p: Ridge vs SupCon, t-test / Wilcoxon | 0.035 / 0.057 | derived |
| Holm-adjusted p: Ridge r > 0 (6 models) | 0.052 | derived |
| Holm-adjusted p: MLP vs SupCon | 0.107 | derived (said in the text as "only Ridge survives") |
| Ridge better than SupCon in subjects | 16 of 22 | derived; also `n_subjects_ref_better` = 6 |
| SupCon better than no-SupCon; mean difference | 13 of 22; 0.006 | derived; `stats…json` `mean_diff` |
| Subject examples (sub-17, sub-08, sub-18, sub-19) | see text | `per_subject_r.csv` |
| Negative for every model | sub-01, sub-11 | derived |
| Prediction SD / true SD (median) | SupCon 0.074, no SupCon 0.038, Ridge 0.124, MLP 0.173 | derived from `runs/*.npz` |
| Exact-window r (16 subjects) | Ridge 0.074, MLP 0.041, SupCon 0.007, no SupCon −0.022 | `summary_table.csv` `r_mean_exact_windows` |
| r² of best model | 0.007 | derived (0.0815²) |
| DMN–FPN without GSR | 0.824 ± 0.108, 0/40 negative | v1 `results/dmn_fpn_validation.json` |
| DMN–FPN with GSR | 0.269 ± 0.214, 3/40 negative | same file |
| DMN parcel vs DMN average | 0.659–0.872 | same file |

## Figures
- **Fig. 1**: v2 `figures/per_subject_heatmap.png`.
- **Fig. 2**: v2 `figures/ablation_paired.png`.
- **Fig. 3**: v1 `figures/dmn_fpn_validation.png`.
