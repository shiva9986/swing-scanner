import pandas as pd
import numpy as np
import os

print("Starting Scanner...")

# -----------------------------
# Load File
# -----------------------------
file_path = "data/bhavcopy.csv"

if not os.path.exists(file_path):
    print("Bhavcopy file not found!")
    exit()

df = pd.read_csv(file_path)

print("Rows Loaded:", len(df))

# -----------------------------
# Clean Column Names
# -----------------------------
df.columns = df.columns.str.strip().str.upper()

print("Columns Found:", df.columns.tolist())

# -----------------------------
# Filter Only EQ (if available)
# -----------------------------
if "SERIES" in df.columns:
    df = df[df["SERIES"].astype(str).str.upper() == "EQ"]
    print("EQ Rows:", len(df))
else:
    print("SERIES column not found — skipping filter")

# -----------------------------
# Required Columns Mapping
# -----------------------------
required_cols = {
    "SYMBOL": "SYMBOL",
    "CLOSE": "CLOSE_PRICE",
    "LAST": "LAST_PRICE",
    "PCT": "PCT_CHANGE",
    "DELIV": "DELIV_PER",
    "VOLUME": "TTL_TRD_QNTY"
}

# Try auto-detect close price
if "CLOSE_PRICE" in df.columns:
    close_col = "CLOSE_PRICE"
elif "LAST_PRICE" in df.columns:
    close_col = "LAST_PRICE"
else:
    print("No Close price column found")
    exit()

# Auto detect percentage change
pct_col = None
for col in df.columns:
    if "PCT" in col:
        pct_col = col
        break

# Auto detect volume
vol_col = None
for col in df.columns:
    if "QNTY" in col or "VOLUME" in col:
        vol_col = col
        break

# Auto detect delivery
deliv_col = None
for col in df.columns:
    if "DELIV" in col:
        deliv_col = col
        break

print("Using Columns:")
print("Close:", close_col)
print("Pct:", pct_col)
print("Volume:", vol_col)
print("Delivery:", deliv_col)

# -----------------------------
# Convert Numeric
# -----------------------------
for col in [close_col, pct_col, vol_col, deliv_col]:
    if col:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# Create Scores
# -----------------------------
df["MOMENTUM_SCORE"] = 0
df["ACCUMULATION_SCORE"] = 0

if pct_col:
    df["MOMENTUM_SCORE"] = df[pct_col].fillna(0) * 100

if vol_col and deliv_col:
    df["ACCUMULATION_SCORE"] = (
        df[vol_col].fillna(0) * df[deliv_col].fillna(0)
    ) / 1000000

df["FINAL_SCORE"] = df["MOMENTUM_SCORE"] + df["ACCUMULATION_SCORE"]

# -----------------------------
# Sort & Export
# -----------------------------
df = df.sort_values("FINAL_SCORE", ascending=False)

output_file = "swing_output.csv"
df.to_csv(output_file, index=False)

print("Scanner Completed Successfully")
print("Output Saved:", output_file)
