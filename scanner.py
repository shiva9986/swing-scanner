import pandas as pd

# Load bhavcopy from GitHub data folder
df = pd.read_csv("data/bhavcopy.csv")

print("Rows Loaded:", len(df))

# Keep only EQ series
df = df[df["SERIES"] == "EQ"].copy()

# Convert required columns to numeric
numeric_cols = [
    "PREV_CLOSE",
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=numeric_cols)

# =========================
# CALCULATE PERCENT CHANGE
# =========================
df["PCT_CHANGE"] = (
    (df["CLOSE_PRICE"] - df["PREV_CLOSE"]) 
    / df["PREV_CLOSE"]
) * 100

# =========================
# MOMENTUM SCORE
# =========================
df["MOMENTUM_SCORE"] = (
    df["PCT_CHANGE"] * 50 +
    (df["TTL_TRD_QNTY"] / df["TTL_TRD_QNTY"].max()) * 50
)

# =========================
# ACCUMULATION SCORE
# =========================
df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 0.7 +
    (df["TTL_TRD_QNTY"] / df["TTL_TRD_QNTY"].max()) * 30
)

# =========================
# FINAL SCORE
# =========================
df["FINAL_SCORE"] = (
    df["MOMENTUM_SCORE"] * 0.6 +
    df["ACCUMULATION_SCORE"] * 0.4
)

# Sort by final score
df = df.sort_values("FINAL_SCORE", ascending=False)

# Select output columns
output = df[[
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY",
    "MOMENTUM_SCORE",
    "ACCUMULATION_SCORE",
    "FINAL_SCORE"
]].head(20)

# Save Excel properly
output.to_excel("swing_output.xlsx", index=False)

print("Scanner Completed Successfully")
