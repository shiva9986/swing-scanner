import pandas as pd

# Load bhavcopy
df = pd.read_csv("data/bhavcopy.csv")

# Keep only EQ series
df = df[df["SERIES"] == "EQ"]

# Convert numeric columns safely
numeric_cols = [
    "OPEN_PRICE",
    "HIGH_PRICE",
    "LOW_PRICE",
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Basic swing condition:
# 1. Close near day high
# 2. Good volume
# 3. Good delivery %

df["Close_vs_High"] = df["CLOSE_PRICE"] / df["HIGH_PRICE"]

swing_df = df[
    (df["Close_vs_High"] > 0.98) &
    (df["TTL_TRD_QNTY"] > 200000) &
    (df["DELIV_PER"] > 40)
]

# Sort by volume
swing_df = swing_df.sort_values("TTL_TRD_QNTY", ascending=False)

# Save output
swing_df.to_excel("swing_output.xlsx", index=False)

print("Scanner completed successfully")
