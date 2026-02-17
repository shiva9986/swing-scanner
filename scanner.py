import pandas as pd
import numpy as np

# ===== LOAD FILE =====
df = pd.read_csv("data/bhavcopy.csv")

print("Rows Loaded:", len(df))
print("Columns Found:", df.columns.tolist())

# ===== CLEAN COLUMN NAMES =====
df.columns = df.columns.str.strip().str.upper()

# ===== FILTER ONLY EQ SERIES (if exists) =====
if "SERIES" in df.columns:
    df = df[df["SERIES"] == "EQ"]

# ===== CALCULATE PERCENT CHANGE =====
df["PCT_CHANGE"] = ((df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

# ===== CLEAN NUMERIC COLUMNS =====
numeric_cols = ["PCT_CHANGE", "DELIV_PER", "TTL_TRD_QNTY"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=numeric_cols)

# ===== MOMENTUM SCORE =====
df["MOMENTUM_SCORE"] = (
    df["PCT_CHANGE"] * 0.6 +
    (df["TTL_TRD_QNTY"] / df["TTL_TRD_QNTY"].max()) * 40
)

# ===== ACCUMULATION SCORE =====
df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 0.7 +
    (df["TTL_TRD_QNTY"] / df["TTL_TRD_QNTY"].max()) * 30
)

# ===== FINAL SCORE =====
df["FINAL_SCORE"] = df["MOMENTUM_SCORE"] + df["ACCUMULATION_SCORE"]

# ===== SORT =====
df = df.sort_values("FINAL_SCORE", ascending=False)

# ===== SELECT OUTPUT =====
output_cols = [
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY",
    "MOMENTUM_SCORE",
    "ACCUMULATION_SCORE",
    "FINAL_SCORE"
]

df_output = df[output_cols]

# ===== SAVE FILE =====
df_output.to_excel("swing_output.xlsx", index=False)

print("✅ Scanner Completed Successfully")
