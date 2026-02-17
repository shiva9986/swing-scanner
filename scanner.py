import pandas as pd
import numpy as np

# ===============================
# LOAD BHAVCOPY
# ===============================
df = pd.read_csv("data/bhavcopy.csv")

print("Rows Loaded:", len(df))

# Keep only EQ series
df = df[df["SERIES"] == "EQ"]

# ===============================
# SAFE COLUMN HANDLING
# ===============================
df.columns = df.columns.str.strip()

# Convert required columns safely
numeric_cols = [
    "CLOSE_PRICE",
    "PREV_CLOSE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    else:
        print(f"Column missing: {col}")

# ===============================
# CALCULATIONS
# ===============================

# % Change
df["PCT_CHANGE"] = (
    (df["CLOSE_PRICE"] - df["PREV_CLOSE"]) /
    df["PREV_CLOSE"]
) * 100

# Volume Score (normalized)
df["VOL_SCORE"] = (
    df["TTL_TRD_QNTY"] /
    df["TTL_TRD_QNTY"].max()
) * 100

# ===============================
# MOMENTUM SCORE
# ===============================
df["MOMENTUM_SCORE"] = (
    (df["PCT_CHANGE"] * 0.6) +
    (df["VOL_SCORE"] * 0.4)
)

# ===============================
# ACCUMULATION SCORE
# ===============================
df["ACCUMULATION_SCORE"] = (
    (df["DELIV_PER"] * 0.7) +
    (df["VOL_SCORE"] * 0.3)
)

# ===============================
# FINAL SCORE
# ===============================
df["FINAL_SCORE"] = (
    df["MOMENTUM_SCORE"] * 0.6 +
    df["ACCUMULATION_SCORE"] * 0.4
)

# ===============================
# SORT
# ===============================
df = df.sort_values("FINAL_SCORE", ascending=False)

# ===============================
# SELECT OUTPUT COLUMNS
# ===============================
output = df[[
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY",
    "MOMENTUM_SCORE",
    "ACCUMULATION_SCORE",
    "FINAL_SCORE"
]]

# ===============================
# SAVE OUTPUT
# ===============================
output.to_excel("swing_output.xlsx", index=False)

print("Scanner Completed Successfully ✅")
