# EEG-to-DMN LOSO benchmark

Code and results for the paper

> **Can Scalp EEG Predict Default Mode Network Activity in Unseen Subjects? A Leakage-Controlled Benchmark of Linear, Transformer and Contrastive Models**

We predict the Default Mode Network (DMN) fMRI signal from simultaneously recorded scalp EEG in the public NATVIEW dataset. We test the models on subjects they were never trained on, using Leave-One-Subject-Out (LOSO) cross-validation. The test subject is never used for training, early stopping or hyperparameter selection.

## Main result

LOSO over 22 subjects. For each subject, r is the Pearson correlation between predicted and measured DMN, averaged over seeds. The table shows the mean ± SD over subjects. Source: `results/v2/results/summary_table.csv`.

| Model | r (mean ± SD) | Subjects with r > 0 | p, paired t-test vs. Transformer + SupCon |
|---|---|---|---|
| Ridge regression | 0.082 ± 0.132 | 15 / 22 | 0.007 |
| MLP | 0.057 ± 0.112 | 15 / 22 | 0.027 |
| HRF-weighted alpha power | 0.056 ± 0.137 | 13 / 22 | 0.067 |
| LaBraM-style patch Transformer (no pretraining) | −0.025 ± 0.095 | 10 / 22 | 0.623 |
| Transformer, no SupCon | −0.019 ± 0.102 | 9 / 22 | 0.728 |
| Transformer + SupCon | −0.014 ± 0.088 | 11 / 22 | — |

The p-values above are unadjusted. After Holm correction, only Ridge remains significantly better than the SupCon Transformer (adjusted p = 0.035). Even the best model explains less than 1% of DMN variance in a new subject (r² ≈ 0.007). [`FACT_SHEET.md`](FACT_SHEET.md) traces every number in the paper to the file it comes from.

## Repository layout

```
notebooks/
  EEG2DMN_UnifiedLOSO_v1.ipynb           preprocessing, EEG-fMRI alignment, all six models with the
                                         original settings, DMN-FPN check (robustness column of Table II)
  EEG2DMN_NestedRegularization_v2.ipynb  nested candidate search on validation subjects
                                         (Tables I-II, Figs. 1-2)
analysis/
  paper_derived_numbers.py               recomputes derived numbers (Holm p-values, subject counts,
                                         prediction-SD ratios, data counts) from results/
results/
  v1/  results/  figures/  runs/         outputs of the v1 notebook
  v2/  results/  figures/  runs/         outputs of the v2 notebook (main results)
FACT_SHEET.md                            source file for every number in the paper
```

`runs/<model>/seed<k>/fold<NN>_<subject>.npz` holds the test predictions (`y_true`, `y_pred`, `exact`, `session`) and a JSON `info` record for one LOSO fold. The per-epoch training logs of the deep models are stored next to it as CSV files.

## Data

We use the preprocessed resting-state recordings of the NATVIEW EEG-fMRI dataset (Telesford et al., "An open-access dataset of naturalistic viewing using simultaneous EEG-fMRI," *Sci. Data* 10, 554, 2023). The data are public in the FCP-INDI S3 bucket. No credentials are needed.

```
s3://fcp-indi/data/Projects/NATVIEW_EEGFMRI/preproc_data
```

The dataset is not redistributed here. The v1 notebook expects a folder containing `sub-01 … sub-22` with, per session:

```
sub-XX/ses-YY/eeg/sub-XX_ses-YY_task-rest_eeg.set   (+ events.tsv, channels.tsv)
sub-XX/ses-YY/func/sub-XX_ses-YY_task-rest_bold/func_atlas/
    sub-XX_ses-YY_task-rest_space-MNI152Lin_res-3mm_atlas-Schaefer2018_dens-100parcels7networks_desc-sm0_bold.tsv
    ... _desc-sm0gsr_bold.tsv   (used only for the DMN-FPN check)
```

## How to reproduce

The notebooks run on Google Colab, Kaggle or a local machine. They detect the environment themselves. We used an NVIDIA T4 GPU. Both notebooks save every finished fold, so they can resume after a disconnect.

1. **Install:** `pip install -r requirements.txt` (on Colab and Kaggle, only `mne` and `nilearn` are missing, and the notebook installs them).
2. **Run `notebooks/EEG2DMN_UnifiedLOSO_v1.ipynb`.** Set `DATA_ROOT` in Cell 1 to the NATVIEW folder, or leave it empty to auto-detect. The notebook writes `EEG2DMN_UnifiedLOSO_v1_outputs/` with `cache/` (preprocessed features), `runs/`, `results/` and `figures/`.
3. **Run `notebooks/EEG2DMN_NestedRegularization_v2.ipynb`.** It reuses the v1 `cache/` and the v1 HRF-alpha and LaBraM-style runs. Set `V1_DIR` in Cell 1 to the v1 output folder, or leave it empty to auto-detect. It writes `Outputs_v2/` next to that folder.
4. **Recompute the derived numbers** from the stored results, from the repository root:
   ```
   python analysis/paper_derived_numbers.py
   ```
   This step needs only `numpy` and `pandas`, and it works on the committed `results/` without the dataset.

Set `SMOKE_TEST = True` in Cell 1 of either notebook for a quick 2-fold, 2-epoch code check before a full run.

The exact library versions of each run are recorded in `results/v*/results/environment*.json`. The v2 runs were split across a Google Colab session and a Kaggle T4 session with identical code and seeds. `results/v2/results/provenance_runs_before_kaggle.json` lists the runs finished before the Kaggle session.

## Citation

If you use this code, please cite the paper above (full reference to be added on publication) and the NATVIEW dataset.

## License

Code: MIT (see [LICENSE](LICENSE)). The NATVIEW data remain under their original terms.
