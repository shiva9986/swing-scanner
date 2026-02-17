import pandas as pd
import os

# ===============================
# Load Bhavcopy
# ===============================

file_path = "data/bhavcopy.csv"

if not os.path.exists(file_path):
    print("❌ bhavcopy.csv not found inside data folder")
    exit()

df = pd.read_csv(file_path)

print("Rows Loaded:", len(df))

# ===============================
# Clean Column Names
# ===============================

df.columns = df.columns.str.strip().str.upper()

# Required Columns Check
required_cols = ["SYMBOL", "SERIES", "CLOSE", "TOTTRDQTY", "PCTCHG"]

for col in required_cols:
    if col not in df.columns:
        print(f"❌ Missing column: {col}")
        exit()

# ===============================
# Filter Only EQ Stocks
# ===============================

df = df[df["SERIES"] == "EQ"].copy()

# ===============================
# Convert Numeric Columns
# ===============================

df["CLOSE"] = pd.to_numeric(df["CLOSE"], errors="coerce")
df["TOTTRDQTY"] = pd.to_numeric(df["TOTTRDQTY"], errors="coerce")
df["PCTCHG"] = pd.to_numeric(df["PCTCHG"], errors="coerce")

df.dropna(inplace=True)

# ===============================
# MOMENTUM SCORE
# ===============================

df["MOMENTUM_SCORE"] = (
    (df["PCTCHG"] * 2) +
    (df["TOTTRDQTY"] / df["TOTTRDQTY"].mean())
)

# ===============================
# ACCUMULATION SCORE
# ===============================

df["ACCUMULATION_SCORE"] = (
    (df["TOTTRDQTY"] / df["TOTTRDQTY"].max()) * 100
)

# ===============================
# FINAL SCORE
# ===============================

df["FINAL_SCORE"] = df["MOMENTUM_SCORE"] + df["ACCUMULATION_SCORE"]

# ===============================
# Sort
# ===============================

df = df.sort_values("FINAL_SCORE", ascending=False)

# ===============================
# Save Output
# ===============================

output_file = "swing_output.xlsx"

df.to_excel(output_file, index=False)

print("✅ Output file created successfully:", output_file)
