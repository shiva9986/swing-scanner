import pandas as pd
import os

# =========================
# READ FILE
# =========================

file_path = "data/bhavcopy.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError("bhavcopy.csv not found inside data folder")

df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip()

# Keep only EQ series if SERIES column exists
if "SERIES" in df.columns:
    df = df[df["SERIES"] == "EQ"]

# Remove missing values
df = df.dropna()

# =========================
# BASIC CALCULATIONS
# =========================

# % Change
df["PCT_CHANGE"] = ((df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

# =========================
# MOMENTUM SCORE
# =========================

df["MOMENTUM_SCORE"] = (
    df["PCT_CHANGE"].abs() * 2
)

# =========================
# ACCUMULATION SCORE
# =========================

df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 1.5
)

# =========================
# FINAL SCORE
# =========================

df["FINAL_SCORE"] = df["MOMENTUM_SCORE"] + df["ACCUMULATION_SCORE"]

# =========================
# SORT & SAVE
# =========================

df = df.sort_values("FINAL_SCORE", ascending=False)

output_columns = [
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY",
    "MOMENTUM_SCORE",
    "ACCUMULATION_SCORE",
    "FINAL_SCORE"
]

df[output_columns].to_excel("swing_output.xlsx", index=False)

print("Scanner completed successfully ✅")
