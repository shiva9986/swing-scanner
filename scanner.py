import pandas as pd

# Load bhavcopy safely
df = pd.read_csv("data/bhavcopy.csv", low_memory=False)

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

print("Columns Found:", df.columns.tolist())

# Filter only EQ series
df = df[df["SERIES"].str.strip() == "EQ"]

# Convert required columns safely
cols = ["CLOSE_PRICE", "PREV_CLOSE", "DELIV_PER", "TTL_TRD_QNTY"]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows with missing data
df = df.dropna(subset=cols)

# Calculate % change
df["PCT_CHANGE"] = (
    (df["CLOSE_PRICE"] - df["PREV_CLOSE"]) 
    / df["PREV_CLOSE"]
) * 100

# Create Score
df["SCORE"] = (
    df["PCT_CHANGE"] * 2 +
    df["DELIV_PER"] * 0.3 +
    (df["TTL_TRD_QNTY"] / 1000000)
)

# Sort
df = df.sort_values("SCORE", ascending=False)

# Take Top 10
top10 = df[[
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY",
    "SCORE"
]].head(10)

# Save
top10.to_excel("swing_output.xlsx", index=False)

print("Top 10 stocks generated successfully.")
