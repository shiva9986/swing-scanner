import pandas as pd

# Load bhavcopy
df = pd.read_csv("data/bhavcopy.csv")

# Filter only EQ series
df = df[df["SERIES"] == "EQ"]

# Convert required columns to numeric
cols = ["CLOSE_PRICE", "DELIV_PER", "TTL_TRD_QNTY"]
for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows with missing data
df = df.dropna(subset=cols)

# Calculate % change
df["PCT_CHANGE"] = ((df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

# Scoring system
df["SCORE"] = (
    df["PCT_CHANGE"] * 2 +
    df["DELIV_PER"] * 0.3 +
    (df["TTL_TRD_QNTY"] / 100000)
)

# Sort by score
df = df.sort_values("SCORE", ascending=False)

# Take Top 10 only
top10 = df[["SYMBOL", "CLOSE_PRICE", "PCT_CHANGE", "DELIV_PER", "TTL_TRD_QNTY", "SCORE"]].head(10)

# Save output
top10.to_excel("swing_output.xlsx", index=False)

print("Top 10 stocks generated successfully.")
