import pandas as pd
import numpy as np

# ==============================
# 1. LOAD BHAVCOPY
# ==============================

df = pd.read_csv("data/bhavcopy.csv")

print("Rows Loaded:", len(df))

# Clean column names (important)
df.columns = df.columns.str.strip().str.upper()

# Keep only EQ series if column exists
if "SERIES" in df.columns:
    df = df[df["SERIES"] == "EQ"]

# ==============================
# 2. SAFE COLUMN HANDLING
# ==============================

# Rename common bhavcopy columns safely
column_map = {
    "SYMBOL": "SYMBOL",
    "CLOSE_PRICE": "CLOSE",
    "CLOSE": "CLOSE",
    "PREV_CLOSE": "PREV_CLOSE",
    "TTL_TRD_QNTY": "VOLUME",
    "DELIV_PER": "DELIV_PER"
}

df = df.rename(columns=column_map)

required_cols = ["SYMBOL", "CLOSE", "PREV_CLOSE", "VOLUME"]

for col in required_cols:
    if col not in df.columns:
        print(f"Missing Column: {col}")
        exit()

# Convert numeric safely
for col in ["CLOSE", "PREV_CLOSE", "VOLUME"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==============================
# 3. CALCULATE PERCENT CHANGE
# ==============================

df["PCT_CHANGE"] = ((df["CLOSE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

# ==============================
# 4. MOMENTUM SCORE
# ==============================

df["MOMENTUM_SCORE"] = (
    (df["PCT_CHANGE"].clip(lower=0) * 10) +
    (np.log1p(df["VOLUME"]) * 2)
)

# ==============================
# 5. ACCUMULATION SCORE
# ==============================

if "DELIV_PER" in df.columns:
    df["DELIV_PER"] = pd.to_numeric(df["DELIV_PER"], errors="coerce")
    df["ACCUMULATION_SCORE"] = (
        df["DELIV_PER"].fillna(0) * 5 +
        (np.log1p(df["VOLUME"]) * 1.5)
    )
else:
    df["ACCUMULATION_SCORE"] = np.log1p(df["VOLUME"]) * 1.5

# ==============================
# 6. FINAL SCORE
# ==============================

df["FINAL_SCORE"] = df["MOMENTUM_SCORE"] + df["ACCUMULATION_SCORE"]

# ==============================
# 7. SORT & OUTPUT
# ==============================

df = df.sort_values("FINAL_SCORE", ascending=False)

output_columns = [
    "SYMBOL",
    "CLOSE",
    "PCT_CHANGE",
    "VOLUME",
    "MOMENTUM_SCORE",
    "ACCUMULATION_SCORE",
    "FINAL_SCORE"
]

df[output_columns].to_excel("swing_output.xlsx", index=False)

print("Scanner Completed Successfully")
