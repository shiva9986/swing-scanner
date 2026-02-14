import pandas as pd

print("Loading bhavcopy...")

# Read bhavcopy
df = pd.read_csv("data/bhavcopy.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Keep only EQ series
df["SERIES"] = df["SERIES"].astype(str).str.strip()
df = df[df["SERIES"] == "EQ"]

# Convert numeric columns
numeric_cols = [
    "PREV_CLOSE",
    "OPEN_PRICE",
    "HIGH_PRICE",
    "LOW_PRICE",
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Calculate % change
df["PCT_CHANGE"] = ((df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

# Create Strength Score
df["SCORE"] = (
    (df["PCT_CHANGE"] * 2) +                 # Momentum weight
    (df["DELIV_PER"] * 0.5) +                # Delivery weight
    (df["TTL_TRD_QNTY"] / df["TTL_TRD_QNTY"].max()) * 10  # Volume normalization
)

# Basic quality filter
filtered = df[
    (df["PCT_CHANGE"] > 0.5) &
    (df["DELIV_PER"] > 35)
]

# Sort by SCORE
filtered = filtered.sort_values(by="SCORE", ascending=False)

# Take Top 30
top30 = filtered.head(30)

# Select important columns
output_cols = [
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY",
    "SCORE"
]

top30 = top30[output_cols]

# Save output
top30.to_excel("swing_output.xlsx", index=False)

print("Top 30 Professional Swing List Created.")
print("Stocks found:", len(top30))
