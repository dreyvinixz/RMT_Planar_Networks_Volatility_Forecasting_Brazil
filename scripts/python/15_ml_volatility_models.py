from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "tables"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
RANDOM_SEED = 42
EPS = 1e-8


def qlike_loss(y_true, y_pred, epsilon=1e-12):
    var_true = np.maximum(np.asarray(y_true) ** 2, epsilon)
    var_pred = np.maximum(np.asarray(y_pred) ** 2, epsilon)
    return float(np.mean(np.log(var_pred) + var_true / var_pred))


def evaluate_model(y_true, y_pred, y_train_true):
    mask = pd.notnull(y_true) & pd.notnull(y_pred)
    y_true = np.asarray(y_true[mask], dtype=float)
    y_pred = np.asarray(y_pred[mask], dtype=float)
    if len(y_true) == 0:
        return np.nan, np.nan, np.nan, np.nan

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    qlike = qlike_loss(y_true, y_pred)

    y_train_true = np.asarray(y_train_true, dtype=float)
    mse_pred = mean_squared_error(y_true, y_pred)
    mse_baseline = np.mean((y_true - np.mean(y_train_true)) ** 2)
    r2_oos = 1 - (mse_pred / mse_baseline) if mse_baseline > 0 else np.nan
    return mae, rmse, qlike, r2_oos


def get_feature_sets(df):
    set_a_cols = [
        "rolling_mean_return_5d",
        "rolling_mean_return_20d",
        "rolling_vol_5d",
        "rolling_vol_20d",
        "rolling_vol_60d",
        "rolling_vol_120d",
        "rolling_abs_return_5d",
        "rolling_abs_return_20d",
        "rolling_abs_return_60d",
        "rolling_skew_60d",
        "rolling_kurtosis_60d",
        "ewma_volatility",
        "lagged_rv_5d",
        "lagged_rv_20d",
        "abs_r_t",
        "r2_t",
    ]
    set_a_cols = [c for c in set_a_cols if c in df.columns]

    set_b_cols = set_a_cols + [
        "rolling_average_market_correlation_252d",
        "rolling_average_market_correlation_504d",
        "rolling_median_market_correlation_252d",
        "largest_eigenvalue",
        "market_mode_share",
        "number_of_eigenvalues_above_mp",
    ]
    set_b_cols = [c for c in set_b_cols if c in df.columns]

    net_cols = [
        "mst_original_degree",
        "mst_original_betweenness",
        "mst_group_degree",
        "mst_group_betweenness",
        "pmfg_original_degree",
        "pmfg_original_betweenness",
        "pmfg_group_degree",
        "pmfg_group_betweenness",
        "pmfg_original_clustering",
        "pmfg_group_clustering",
    ]
    sec_cols = [c for c in df.columns if c.startswith("sector_") or c.startswith("subsector_")]
    set_c_cols = [c for c in set_b_cols + net_cols + sec_cols if c in df.columns]

    return {
        "Set A (Classical)": set_a_cols,
        "Set B (+Market/RMT)": set_b_cols,
        "Set C (+Network)": set_c_cols,
    }


class TabularMLP(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 64, dropout: float = 0.15):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
        )
        self.out = nn.Softplus()

    def forward(self, x):
        return self.out(self.net(x)).squeeze(-1) + EPS


class TemporalCNN(nn.Module):
    def __init__(self, n_features: int, n_filters: int = 24, kernel_size: int = 3, dense_dim: int = 32):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(n_features, n_filters, kernel_size=kernel_size, padding=kernel_size // 2),
            nn.ReLU(),
            nn.Conv1d(n_filters, n_filters, kernel_size=kernel_size, padding=kernel_size // 2),
            nn.ReLU(),
            nn.AdaptiveMaxPool1d(1),
        )
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(n_filters, dense_dim),
            nn.ReLU(),
            nn.Dropout(0.15),
            nn.Linear(dense_dim, 1),
        )
        self.out = nn.Softplus()

    def forward(self, x):
        # x arrives as [batch, window, features]; Conv1d expects [batch, features, window].
        x = x.transpose(1, 2)
        return self.out(self.head(self.conv(x))).squeeze(-1) + EPS


def train_torch_regressor(model, X_train, y_train, X_val, y_val, max_epochs=80, patience=10, batch_size=256):
    torch.manual_seed(RANDOM_SEED)
    model = model.to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    criterion = nn.HuberLoss(delta=0.02)

    X_train_t = torch.as_tensor(X_train, dtype=torch.float32)
    y_train_t = torch.as_tensor(y_train, dtype=torch.float32)
    X_val_t = torch.as_tensor(X_val, dtype=torch.float32, device=DEVICE)
    y_val_t = torch.as_tensor(y_val, dtype=torch.float32, device=DEVICE)
    loader = DataLoader(TensorDataset(X_train_t, y_train_t), batch_size=batch_size, shuffle=False)

    best_state = None
    best_val = np.inf
    stale = 0

    for _ in range(max_epochs):
        model.train()
        for xb, yb in loader:
            xb = xb.to(DEVICE)
            yb = yb.to(DEVICE)
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(xb), yb)
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            val_pred = model(X_val_t)
            val_loss = criterion(val_pred, y_val_t).item()

        if val_loss < best_val - 1e-7:
            best_val = val_loss
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            stale = 0
        else:
            stale += 1
            if stale >= patience:
                break

    if best_state is not None:
        model.load_state_dict(best_state)
    return model, best_val


def predict_torch(model, X, batch_size=1024):
    model.eval()
    preds = []
    X_t = torch.as_tensor(X, dtype=torch.float32)
    loader = DataLoader(TensorDataset(X_t), batch_size=batch_size, shuffle=False)
    with torch.no_grad():
        for (xb,) in loader:
            preds.append(model(xb.to(DEVICE)).detach().cpu().numpy())
    return np.maximum(np.concatenate(preds), 1e-6)


def append_metrics(results, predictions, df, y_all, preds_series, model_name, feature_set, horizon, symbols):
    train_mask = df["split"] == "train"
    valid_mask = pd.notnull(y_all)
    for sym in symbols:
        sym_mask = df["symbol"] == sym
        y_train_sym = y_all[train_mask & valid_mask & sym_mask]
        for split_name in ["train", "validation", "test"]:
            split_mask = df["split"] == split_name
            eval_mask = split_mask & valid_mask & sym_mask
            if eval_mask.sum() == 0:
                continue
            mae, rmse, qlike, r2oos = evaluate_model(y_all[eval_mask], preds_series[eval_mask], y_train_sym)
            results.append(
                {
                    "model": model_name,
                    "feature_set": feature_set,
                    "symbol": sym,
                    "horizon": horizon,
                    "split": split_name,
                    "MAE": mae,
                    "RMSE": rmse,
                    "QLIKE": qlike,
                    "R2_oos": r2oos,
                }
            )

            pred_block = df.loc[eval_mask, ["date", "symbol", "split"]].copy()
            pred_block["horizon"] = horizon
            pred_block["model"] = model_name
            pred_block["feature_set"] = feature_set
            pred_block["y_true"] = y_all[eval_mask].to_numpy()
            pred_block["y_pred"] = preds_series[eval_mask].to_numpy()
            predictions.append(pred_block)


def make_sequence_data(df, horizon, feature_cols, window=20):
    X, y, rows = [], [], []
    target_col = f"target_rv_{horizon}d"
    for _, sdf in df.groupby("symbol", sort=False):
        sdf = sdf.sort_values("date")
        values = sdf[feature_cols].fillna(0).to_numpy(dtype=np.float32)
        targets = sdf[target_col].to_numpy(dtype=np.float32)
        index_values = sdf.index.to_numpy()
        for pos in range(window - 1, len(sdf)):
            if np.isfinite(targets[pos]):
                X.append(values[pos - window + 1 : pos + 1])
                y.append(targets[pos])
                rows.append(index_values[pos])
    return np.asarray(X, dtype=np.float32), np.asarray(y, dtype=np.float32), np.asarray(rows)


def main():
    print("Starting ML/DL volatility models...")
    print(f"PyTorch device: {DEVICE}")

    df_path = OUTPUT_DIR / "volatility_forecasting_dataset_2006_2025.csv"
    df = pd.read_csv(df_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)

    feature_sets = get_feature_sets(df)
    symbols = df["symbol"].unique()
    horizons = [5, 20]

    sklearn_models = {
        "Ridge": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(
            n_estimators=300, max_depth=6, min_samples_leaf=10, random_state=RANDOM_SEED, n_jobs=-1
        ),
        "HistGradientBoosting": HistGradientBoostingRegressor(
            max_iter=300, max_depth=4, learning_rate=0.05, random_state=RANDOM_SEED
        ),
    }

    results = []
    predictions = []
    feature_importances = []

    train_mask = df["split"] == "train"
    val_mask = df["split"] == "validation"

    for h in horizons:
        target_col = f"target_rv_{h}d"
        y_all = df[target_col]
        valid_mask = pd.notnull(y_all)
        y_train = y_all[train_mask & valid_mask]

        if len(y_train) == 0:
            continue

        for set_name, cols in feature_sets.items():
            print(f"  Horizon {h}d | {set_name} | tabular cols: {len(cols)}")
            X_all = df[cols].fillna(0)

            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_all[train_mask])
            X_all_scaled = scaler.transform(X_all)
            X_train_final = X_all_scaled[train_mask & valid_mask]

            for model_name, model in sklearn_models.items():
                model.fit(X_train_final, y_train)
                preds_all = np.maximum(model.predict(X_all_scaled), 1e-6)
                preds_series = pd.Series(preds_all, index=df.index)
                append_metrics(results, predictions, df, y_all, preds_series, model_name, set_name, h, symbols)

                if model_name == "Random Forest" and set_name == "Set C (+Network)":
                    for col, importance in zip(cols, model.feature_importances_):
                        feature_importances.append({"horizon": h, "feature": col, "importance": importance})

            # Incremental tabular deep-learning model.
            mlp = TabularMLP(input_dim=len(cols))
            val_valid = val_mask & valid_mask
            mlp, _ = train_torch_regressor(
                mlp,
                X_train_final,
                y_train.to_numpy(dtype=np.float32),
                X_all_scaled[val_valid],
                y_all[val_valid].to_numpy(dtype=np.float32),
            )
            preds_all = predict_torch(mlp, X_all_scaled)
            preds_series = pd.Series(preds_all, index=df.index)
            append_metrics(results, predictions, df, y_all, preds_series, "MLP", set_name, h, symbols)

        # Incremental temporal CNN inspired by the existing CUDA CNN, adapted for regression.
        seq_cols = [
            c
            for c in [
                "r_t",
                "abs_r_t",
                "r2_t",
                "ewma_volatility",
                "rolling_vol_5d",
                "rolling_vol_20d",
                "lagged_rv_5d",
                "lagged_rv_20d",
            ]
            if c in df.columns
        ]
        print(f"  Horizon {h}d | CNN-1D | sequence cols: {len(seq_cols)}")
        seq_scaler = StandardScaler()
        df_seq = df.copy()
        df_seq[seq_cols] = seq_scaler.fit_transform(df_seq[seq_cols].fillna(0))
        X_seq, y_seq, row_idx = make_sequence_data(df_seq, h, seq_cols, window=20)
        row_splits = df.loc[row_idx, "split"].to_numpy()
        train_seq = row_splits == "train"
        val_seq = row_splits == "validation"

        cnn = TemporalCNN(n_features=len(seq_cols))
        cnn, _ = train_torch_regressor(cnn, X_seq[train_seq], y_seq[train_seq], X_seq[val_seq], y_seq[val_seq])
        seq_preds = predict_torch(cnn, X_seq)
        preds_series = pd.Series(np.nan, index=df.index, dtype=float)
        preds_series.loc[row_idx] = seq_preds
        append_metrics(results, predictions, df, y_all, preds_series, "CNN-1D", "Sequence window", h, symbols)

    comp_df = pd.DataFrame(results)
    pred_df = pd.concat(predictions, ignore_index=True)
    fi_df = pd.DataFrame(feature_importances)

    comp_df.to_csv(OUTPUT_DIR / "ml_model_comparison_2006_2025.csv", index=False)
    comp_df.to_csv(OUTPUT_DIR / "volatility_model_comparison_2006_2025.csv", index=False)
    pred_df.to_csv(OUTPUT_DIR / "volatility_model_predictions_2006_2025.csv", index=False)
    fi_df.to_csv(OUTPUT_DIR / "ml_feature_importances_2006_2025.csv", index=False)

    print("Saved ML/DL comparison, predictions and feature importances.")


if __name__ == "__main__":
    main()
