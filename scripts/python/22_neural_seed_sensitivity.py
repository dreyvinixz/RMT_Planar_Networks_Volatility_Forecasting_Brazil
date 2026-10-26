from __future__ import annotations

import importlib.util
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "outputs" / "tables"
MODEL_PATH = Path(__file__).with_name("15_ml_volatility_models.py")
SPEC = importlib.util.spec_from_file_location("ml_models", MODEL_PATH)
ml = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ml)

SEEDS = (11, 23, 42, 77, 101)
OUT = TABLES / "neural_seed_sensitivity_2006_2025.csv"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def metrics(y: np.ndarray, yhat: np.ndarray) -> tuple[float, float, float]:
    return (
        float(np.mean(np.abs(y - yhat))),
        float(np.sqrt(np.mean((y - yhat) ** 2))),
        ml.qlike_loss(y, yhat),
    )


def main() -> None:
    torch.set_num_threads(2)
    df = pd.read_csv(TABLES / "volatility_forecasting_dataset_2006_2025.csv", parse_dates=["date"])
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)
    feature_sets = ml.get_feature_sets(df)
    train = df["split"].eq("train").to_numpy()
    val = df["split"].eq("validation").to_numpy()
    test = df["split"].eq("test").to_numpy()
    rows: list[dict[str, object]] = []

    for seed in SEEDS:
        ml.RANDOM_SEED = seed
        for horizon in (5, 20):
            target = df[f"target_rv_{horizon}d"].to_numpy(dtype=float)
            valid = np.isfinite(target)
            y_train = target[train & valid].astype(np.float32)
            y_val = target[val & valid].astype(np.float32)

            for feature_set, cols in feature_sets.items():
                X_raw = df[cols].fillna(0).to_numpy(dtype=float)
                scaler = StandardScaler().fit(X_raw[train])
                X = scaler.transform(X_raw).astype(np.float32)
                train_rows = train & valid
                val_rows = val & valid

                set_seed(seed)
                mlp = ml.TabularMLP(input_dim=len(cols))
                mlp, _ = ml.train_torch_regressor(
                    mlp, X[train_rows], target[train_rows].astype(np.float32),
                    X[val_rows], target[val_rows].astype(np.float32),
                )
                prediction = ml.predict_torch(mlp, X)
                for split_name, mask in (("validation", val & valid), ("test", test & valid)):
                    metric = metrics(target[mask], prediction[mask])
                    rows.append({
                        "seed": seed, "model": "MLP", "feature_set": feature_set,
                        "horizon": horizon, "split": split_name, "n_observations": int(mask.sum()),
                        "MAE": metric[0], "RMSE": metric[1], "QLIKE": metric[2],
                    })

            seq_cols = [c for c in (
                "r_t", "abs_r_t", "r2_t", "ewma_volatility", "rolling_vol_5d",
                "rolling_vol_20d", "lagged_rv_5d", "lagged_rv_20d",
            ) if c in df.columns]
            seq_scaler = StandardScaler().fit(df.loc[train, seq_cols].fillna(0))
            df_seq = df.copy()
            df_seq[seq_cols] = seq_scaler.transform(df_seq[seq_cols].fillna(0))
            X_seq, y_seq, row_idx = ml.make_sequence_data(df_seq, horizon, seq_cols, window=20)
            sequence_splits = df.loc[row_idx, "split"].to_numpy()
            sequence_train = sequence_splits == "train"
            sequence_val = sequence_splits == "validation"
            sequence_test = sequence_splits == "test"

            set_seed(seed)
            cnn = ml.TemporalCNN(n_features=len(seq_cols))
            cnn, _ = ml.train_torch_regressor(
                cnn, X_seq[sequence_train], y_seq[sequence_train],
                X_seq[sequence_val], y_seq[sequence_val],
            )
            pred = ml.predict_torch(cnn, X_seq)
            for split_name, mask in (("validation", sequence_val), ("test", sequence_test)):
                metric = metrics(y_seq[mask], pred[mask])
                rows.append({
                    "seed": seed, "model": "CNN-1D", "feature_set": "Sequence window",
                    "horizon": horizon, "split": split_name, "n_observations": int(mask.sum()),
                    "MAE": metric[0], "RMSE": metric[1], "QLIKE": metric[2],
                })
        print(f"Completed neural sensitivity seed {seed}", flush=True)

    result = pd.DataFrame(rows)
    result.to_csv(OUT, index=False)
    summary = (
        result.groupby(["model", "feature_set", "horizon", "split"], as_index=False)
        .agg(
            seeds=("seed", "nunique"),
            QLIKE_mean=("QLIKE", "mean"),
            QLIKE_sd=("QLIKE", "std"),
            QLIKE_min=("QLIKE", "min"),
            QLIKE_max=("QLIKE", "max"),
            RMSE_mean=("RMSE", "mean"),
            RMSE_sd=("RMSE", "std"),
            MAE_mean=("MAE", "mean"),
            MAE_sd=("MAE", "std"),
        )
    )
    summary.to_csv(TABLES / "neural_seed_sensitivity_summary_2006_2025.csv", index=False)
    print(summary[summary["split"].eq("test")].to_string(index=False))


if __name__ == "__main__":
    main()
