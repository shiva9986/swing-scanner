import pandas as pd
import os

print("Starting scanner...")

# =========================
# LOAD BHAVCOPY
# =========================

file_path = "data/bhavcopy.csv"

if not os.path.exists(file_path):
    print("ERROR: bhavcopy file not found!")
    exit()

df = pd.read_csv(file_path)

print("Columns found:", df.columns.tolist())
print("Rows loaded:", len(df))

# =========================
# CLEAN COLUMN NAMES
# =========================

df.columns = df.columns.str.strip().str.upper()

# Rename if needed
if "TOTTRDQTY" in df.columns:
    df.rename(columns={"TOTTRDQTY": "TTL_TRD_QNTY"}, inplace=True)

# Ensure required columns exist
required_cols = ["SYMBOL", "SERIES", "CLOSE", "TTL_TRD_QNTY"]

for col in required_cols:
    if col not in df.columns:
        print(f"ERROR: Missing column {col}")
        exit()

# Filter EQ series only
df = df[df["SERIES"] == "EQ"]

if df.empty:
    print("No EQ stocks found.")
    exit()

# =========================
# CALCULATIONS
# =========================

df["CLOSE"] = pd.to_numeric(df["CLOSE"], errors="coerce")
df["TTL_TRD_QNTY"] = pd.to_numeric(df["TTL_TRD_QNTY"], errors="coerce")

df = df.dropna()

# Momentum Score
df["MOMENTUM_SCORE"] = df["CLOSE"] * 0.6

# Accumulation Score
df["ACCUMULATION_SCORE"] = df["TTL_TRD_QNTY"] * 0.0001

# Final Score
df["FINAL_SCORE"] = df["MOMENTUM_SCORE"] + df["ACCUMULATION_SCORE"]

# Sort
df = df.sort_values("FINAL_SCORE", ascending=False)

# Keep top 50
df = df.head(50)

# =========================
# SAVE OUTPUT
# =========================

output_file = "swing_output.xlsx"

df.to_excel(output_file, index=False)

print("File saved successfully:", output_file)
