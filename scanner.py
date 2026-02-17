import pandas as pd

# Load file
df = pd.read_csv("data/bhavcopy.csv")

print("Rows loaded:", len(df))

# Clean column names
df.columns = df.columns.str.strip()

# Clean SERIES column
df["SERIES"] = df["SERIES"].astype(str).str.strip()

# Filter EQ only
df = df[df["SERIES"] == "EQ"]

print("EQ Rows:", len(df))

# Convert numeric columns safely
numeric_cols = [
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop rows with missing important values
df = df.dropna(subset=numeric_cols)

# Momentum Score
df["MOMENTUM_SCORE"] = (
    df["PCT_CHANGE"] * 100 +
    df["TTL_TRD_QNTY"] / 100000
)

# Accumulation Score
df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 50 +
    df["TTL_TRD_QNTY"] / 200000
)

# Final Score
df["FINAL_SCORE"] = (
    df["MOMENTUM_SCORE"] * 0.6 +
    df["ACCUMULATION_SCORE"] * 0.4
)

# Sort
df = df.sort_values("FINAL_SCORE", ascending=False)

# Select columns
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

# Save
output.to_excel("swing_output.xlsx", index=False)

print("File generated successfully!")
